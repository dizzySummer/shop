from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'cart'

urlpatterns = [
 
    path('add/id', views.cart_add, name='card_add'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove/id',views.cart_remove, name='cart_remove'),

]
#handler404='cart.views.error_404_view'





