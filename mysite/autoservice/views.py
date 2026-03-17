from django.shortcuts import render

def index(request):
    context = {
        'paslauga': 'Automobilių diagnostika',
        'kaina': 'Nuo 30 €',
        'miestas': 'Vilnius',
    }
    return render(request, 'autoservice/index.html', context)