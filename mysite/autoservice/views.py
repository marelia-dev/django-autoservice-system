from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import Service, Order, Car, CustomUser
from .forms import (
    OrderReviewForm, CustomUserChangeForm, CustomUserCreateForm,
    OrderCreateForm, OrderUpdateForm, OrderLineFormSet
)


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
        'num_visits': num_visits,
    }
    return render(request, 'autoservice/index.html', context=context)


# ==================== MY ORDERS ====================
class MyOrderInstanceListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'autoservice/myorders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(reader=self.request.user)


# ==================== CAR DETAIL ====================
def car(request, car_id):
    car_obj = get_object_or_404(Car, pk=car_id)
    return render(request, 'autoservice/car.html', {'car': car_obj})


# ==================== ALL ORDERS ====================
def uzsakymai(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'autoservice/uzsakymai.html', context=context)


# ==================== SERVICES ====================
def paslaugos(request):
    paslaugos = Service.objects.all().order_by('name')
    return render(request, 'autoservice/paslaugos.html', {'paslaugos': paslaugos})


# ==================== ORDER DETAIL ====================
class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'autoservice/uzsakymas.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.prefetch_related('order_lines__service', 'reviews')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderReviewForm()
        context['line_formset'] = OrderLineFormSet(instance=self.object)
        return context


# ==================== CARS LIST ====================
def automobiliai(request):
    automobiliai_list = Car.objects.all().order_by('make', 'model')
    paginator = Paginator(automobiliai_list, 20)
    page_number = request.GET.get('page')
    automobiliai = paginator.get_page(page_number)

    context = {'automobiliai': automobiliai}
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

    paginator = Paginator(results, 20)
    page_number = request.GET.get('page')
    paged_results = paginator.get_page(page_number)

    context = {
        'query': query,
        'automobiliai': paged_results,
    }
    return render(request, 'autoservice/search.html', context=context)


# ==================== AUTH & PROFILE ====================
class SignUpView(generic.CreateView):
    form_class = CustomUserCreateForm
    template_name = 'autoservice/signup.html'
    success_url = reverse_lazy('login')


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'autoservice/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


# ==================== ORDER VIEWS ====================
class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'autoservice/order_create.html'
    success_url = reverse_lazy('my_orders')

    def form_valid(self, form):
        form.instance.reader = self.request.user
        form.instance.status = 'new'
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Order
    form_class = OrderUpdateForm
    template_name = 'autoservice/order_update.html'
    success_url = reverse_lazy('my_orders')

    def test_func(self):
        order = self.get_object()
        return order.reader == self.request.user


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    template_name = 'autoservice/order_delete.html'
    success_url = reverse_lazy('my_orders')

    def test_func(self):
        order = self.get_object()
        return order.reader == self.request.user


class OrderLinesUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.View):
    template_name = 'autoservice/order_lines_update.html'

    def test_func(self):
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        return order.reader == self.request.user

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        formset = OrderLineFormSet(instance=order)
        return render(request, self.template_name, {
            'order': order,
            'formset': formset
        })

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        formset = OrderLineFormSet(request.POST, instance=order)

        if formset.is_valid():
            formset.save()
            messages.success(request, _("Services have been successfully saved."))
            return redirect('order', pk=order.pk)

        return render(request, self.template_name, {
            'order': order,
            'formset': formset
        })