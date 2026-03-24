from django.shortcuts import render, get_object_or_404

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

def uzsakymai(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, 'autoservice/uzsakymai.html', context=context)

def uzsakymas(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order = Order.objects.prefetch_related('order_lines__service').get(pk=order_id)
    return render(request, 'autoservice/uzsakymas.html', {'order': order})

def paslaugos(request):
    paslaugos = Service.objects.all().order_by('name')
    return render(request, 'autoservice/paslaugos.html', {'paslaugos': paslaugos})

