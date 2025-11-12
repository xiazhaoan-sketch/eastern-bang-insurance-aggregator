from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def product(request):
    context = {
        'member_options': ['Self', 'Spouse', 'Child', 'Parent'],
        'cities': ['New Haven', 'Cambridge', 'New York'],
        'plan_summary': '92+ plans found, 18 insurers, from $25/mo',
        'plans': [
            {
                'name': 'SafeVoyage Plus',
                'category': 'Comprehensive',
                'price': 32,
                'perks': ['$500k medical coverage', 'Emergency evacuation', 'Virtual doctor visits'],
            },
            {
                'name': 'CampusCare Elite',
                'category': 'Value',
                'price': 41,
                'perks': ['Sports injury coverage', 'Prescription savings', 'Worldwide assistance'],
            },
        ],
        'comparison_plans': [
            {'name': 'SafeVoyage Plus'},
            {'name': 'CampusCare Elite'},
            {'name': 'Atlas Explorer'},
        ],
        'comparison_rows': [
            {'benefit': 'Medical Coverage', 'values': ['$500k', '$250k', '$750k']},
            {'benefit': 'Emergency Evacuation', 'values': ['Included', '$100 deductible', 'Included']},
            {'benefit': 'Accident Support', 'values': ['24/7 Team', 'Business hours', 'Dedicated rep']},
            {'benefit': 'Adventure & Sports', 'values': ['Recreational', 'Limited', 'Extreme sports']},
        ],
    }
    return render(request, 'product.html', context)


def contact(request):
    submitted = request.method == 'POST'
    return render(request, 'contact.html', {'submitted': submitted})
