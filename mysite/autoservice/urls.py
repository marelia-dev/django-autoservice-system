from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliai, name='automobiliai'),
    path('car/<int:car_id>/', views.car, name='car'),
    path('uzsakymai/', views.OrderListView.as_view(), name='uzsakymai'),
    path('uzsakymas/<int:pk>/', views.OrderDetailView.as_view(), name='order'),
    path('paslaugos/', views.paslaugos, name='paslaugos'),
    path('search/', views.search, name='search'),
    path('myorders/', views.MyOrderInstanceListView.as_view(), name='my_orders'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('order/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('order/<int:pk>/lines/', views.OrderLinesUpdateView.as_view(), name='order_lines_update'),
]