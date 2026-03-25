from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Service, Order, Car

# ==================== INDEX ====================
def index(request):

    num_services = Service.objects.count()
    num_orders = Order.objects.count()
    num_cars = Car.objects.count()
    num_orders_completed = Order.objects.filter(status='done').count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1


    context = {
        'num_services': num_services,
        'num_orders': num_orders,
        'num_cars': num_cars,
        'num_orders_completed': num_orders_completed,
        'num_visits': num_visits
    }
    return render(request, 'autoservice/index.html', context=context)



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

class OrderListView(generic.ListView):
    model = Order
    template_name = 'autoservice/uzsakymai.html'
    context_object_name = 'orders'
    paginate_by = 3

    def get_queryset(self):
        return Order.objects.select_related('car').prefetch_related('order_lines__service')

# ==================== AUTOMOBILIAI ====================
def automobiliai(request):
    automobiliai_list = Car.objects.all().order_by('make', 'model')
    paginator = Paginator(automobiliai_list, 20)
    page_number = request.GET.get('page')
    automobiliai = paginator.get_page(page_number)
    context = {
        'automobiliai': automobiliai,
    }
    return render(request, 'autoservice/automobiliai.html', context=context)

# ==================== SEARCH ====================
def search(request):
    query = request.GET.get('query', '').strip()

    if query:
        results = Car.objects.filter(
        Q(make__icontains=query) |
        Q(model__icontains=query) |
        Q(license_plate__icontains=query) |
        Q(vin_code__icontains=query) |
        Q(client_name__icontains=query)
        ).order_by('make', 'model')
    else:
        results = Car.objects.none()

# Paginacija
    paginator = Paginator(results, 20)
    page_number = request.GET.get('page')
    paged_results = paginator.get_page(page_number)

    context = {
        'query': query,
        'automobiliai': paged_results,
    }
    return render(request, 'autoservice/search.html', context=context)
