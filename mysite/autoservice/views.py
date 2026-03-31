from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from .models import Service, Order, Car
from .forms import OrderReviewForm, UserChangeForm

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

class MyOrderInstanceListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'autoservice/myorders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(reader=self.request.user)

def car(request, car_id):
    car = Car.objects.get(pk=car_id)
    return render(request, 'autoservice/car.html', {'car': car})

def uzsakymai(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, 'autoservice/uzsakymai.html', context=context)

# def uzsakymas(request, order_id):
#     order = get_object_or_404(Order, pk=order_id)
#     order = Order.objects.prefetch_related('order_lines__service').get(pk=order_id)
#     return render(request, 'autoservice/uzsakymas.html', {'order': order})

def paslaugos(request):
    paslaugos = Service.objects.all().order_by('name')
    return render(request, 'autoservice/paslaugos.html', {'paslaugos': paslaugos})

class OrderDetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Order
    template_name = 'autoservice/uzsakymas.html'
    context_object_name = 'order'
    form_class = OrderReviewForm

    def get_queryset(self):
        return Order.objects.prefetch_related('order_lines__service', 'reviews')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        review = form.save(commit=False)
        review.order = self.object
        review.reviewer = self.request.user
        review.save()
        return super().form_valid(form)


class OrderListView(FormMixin, generic.ListView):
    model = Order
    template_name = 'autoservice/uzsakymai.html'
    context_object_name = 'orders'
    form_class = OrderReviewForm
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

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'autoservice/signup.html'
    success_url = reverse_lazy('login')

class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = UserChangeForm
    template_name = "autoservice/profile.html"
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user