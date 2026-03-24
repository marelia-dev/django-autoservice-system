from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliai, name='automobiliai'),
    path('car/<int:car_id>/', views.car, name='car'),
    path('uzsakymai/', views.OrderListView.as_view(), name='uzsakymai'),
    path('uzsakymas/<int:order_id>/', views.uzsakymas, name='order'),
    path('paslaugos/', views.paslaugos, name='paslaugos'),
]