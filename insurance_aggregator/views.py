from typing import Optional

from django.shortcuts import render
from django.templatetags.static import static

from .data_loader import (
    comparison_fields,
    filter_plans,
    get_unique_cities,
    load_plan_catalog,
    summarize_plans,
)

MEMBER_OPTIONS = [
    {'value': 'adult', 'label': 'Adult Student', 'description': 'Age 18–64 coverage', 'icon': '👤'},
    {'value': 'child', 'label': 'Child / Dependent', 'description': 'K-12 or dependent visa', 'icon': '🧒'},
    {'value': 'family', 'label': 'Family', 'description': 'Plans that cover both adults & kids', 'icon': '👨‍👩‍👦'},
    {'value': 'government', 'label': 'Gov & Public Programs', 'description': 'Medicaid, CHIP, TRICARE, etc.', 'icon': '🏛️'},
]

DEFAULT_AGE = 24


def home(request):
    universities = [
        {
            'name': 'Yale University',
            'logo': static('img/partners/yale.svg'),
            'url': 'https://www.yale.edu/',
            'campus': 'New Haven, CT',
        },
        {
            'name': 'Massachusetts Institute of Technology',
            'logo': static('img/partners/mit.svg'),
            'url': 'https://www.mit.edu/',
            'campus': 'Cambridge, MA',
        },
        {
            'name': 'Columbia University',
            'logo': static('img/partners/columbia.svg'),
            'url': 'https://www.columbia.edu/',
            'campus': 'New York, NY',
        },
        {
            'name': 'University of California, Los Angeles',
            'logo': static('img/partners/ucla.svg'),
            'url': 'https://www.ucla.edu/',
            'campus': 'Los Angeles, CA',
        },
        {
            'name': 'Rice University',
            'logo': static('img/partners/rice.svg'),
            'url': 'https://www.rice.edu/',
            'campus': 'Houston, TX',
        },
    ]

    for index, university in enumerate(universities):
        university['delay'] = f'{0.1 * index:.1f}s'

    context = {'partner_universities': universities}
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def _sanitize_member_choice(choice: str) -> str:
    valid = {option['value'] for option in MEMBER_OPTIONS}
    return choice if choice in valid else 'adult'


def _parse_age(raw_age: Optional[str]) -> int:
    if not raw_age:
        return DEFAULT_AGE
    try:
        value = int(raw_age)
    except (TypeError, ValueError):
        return DEFAULT_AGE
    return max(0, min(80, value))


def _build_comparison_rows(plans: list, specs: list) -> list:
    rows = []
    for spec in specs:
        values = []
        for plan in plans:
            raw_value = plan.get(spec['key'])
            if spec.get('type') == 'bool':
                value = 'Yes' if raw_value else 'No'
            else:
                value = raw_value or '—'
            values.append(value)
        rows.append({'label': spec['label'], 'values': values})
    return rows


def product(request):
    catalog = load_plan_catalog()
    cities = get_unique_cities(catalog) or ['New Haven, CT']

    selected_member = _sanitize_member_choice(request.GET.get('member', 'adult'))
    selected_age = _parse_age(request.GET.get('age'))
    selected_city = request.GET.get('city') or cities[0]
    if selected_city not in cities:
        selected_city = cities[0]

    filtered = filter_plans(catalog, selected_member, selected_age, selected_city)
    fallback_to_all = False
    if not filtered:
        filtered = catalog
        fallback_to_all = True

    featured_plans = filtered[:4]
    comparison_plans = filtered[:3]
    field_specs = comparison_fields()
    comparison_rows = _build_comparison_rows(comparison_plans, field_specs)
    summary = summarize_plans(filtered)
    city_label = 'city' if summary['city_count'] == 1 else 'cities'
    plan_summary = (
        f"{summary['plan_count']} plans · {summary['provider_count']} providers · "
        f"{summary['city_count']} {city_label}"
    )
    plan_summary_secondary = (
        f"{summary['child_ready']} cover dependents · {summary['adult_ready']} adult-ready"
    )

    context = {
        'member_options': MEMBER_OPTIONS,
        'cities': cities,
        'selected_member': selected_member,
        'selected_age': selected_age,
        'selected_city': selected_city,
        'featured_plans': featured_plans,
        'plan_summary': plan_summary,
        'plan_summary_secondary': plan_summary_secondary,
        'results_count': summary['plan_count'],
        'fallback_to_all': fallback_to_all,
        'comparison_plans': comparison_plans,
        'comparison_rows': comparison_rows,
    }
    return render(request, 'product.html', context)


def contact(request):
    submitted = request.method == 'POST'
    return render(request, 'contact.html', {'submitted': submitted})
