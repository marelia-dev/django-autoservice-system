from django.shortcuts import render

from .models import Service, Order, Car


def index(request):

    num_services = Service.objects.count()
    num_orders = Order.objects.count()
    num_cars = Car.objects.count()
    num_orders_completed = Order.objects.filter(status='done').count()


    context = {
        'num_services': num_services,
        'num_orders': num_orders,
        'num_cars': num_cars,
        'num_orders_completed': num_orders_completed,
    }
    return render(request, 'autoservice/index.html', context=context)

def automobiliai(request):
    automobiliai = Car.objects.all()
    context = {
        'automobiliai': automobiliai,
    }
    return render(request, 'autoservice/automobiliai.html', context=context)

def car(request, car_id):
    car = Car.objects.get(pk=car_id)
    return render(request, 'autoservice/car.html', {'car': car})

