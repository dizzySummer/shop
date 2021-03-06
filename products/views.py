from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.http import JsonResponse
from django.db import models
from cart.views import *
from cart.forms import CartAddProductForm
from django.conf import settings

from .models import Category, Product,ProductAttribute
from django.contrib.auth.decorators import login_required

from django.db.models import Max,Min,Count,Avg

from django.shortcuts import get_object_or_404,redirect
from django.views.generic.list import ListView

from .forms import NewUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.contrib import messages

from itertools import chain
from django.db.models import Q

#import django_filters



# def index(request):

#     return render(request,'products/index.html')


def index(request):

	cart = request.session.get(settings.CART_SESSION_ID, None)
	
	if cart:
		cart = sum(item['quantity'] for item in cart.values())
		context = {
			"data":cart
		}
		#print(cart)
		return render(request,'products/index.html',context)
	else:
		#print(cart)
		return render(request,'products/index.html')






# def product_list(request):

# 	products=Product.objects.order_by('id')[:10]
# 	categories=Category.objects.all()
# 	min_price=ProductAttribute.objects.aggregate(Min('price'))


# 	return render(request, 'products/product_list.html',  {'products':products,'categories':categories,'min_price':min_price})



def product_list(request):

	products=Product.objects.order_by('id')[:10]
	categories=Category.objects.all()
	min_price=ProductAttribute.objects.aggregate(Min('price'))
	cart = request.session.get(settings.CART_SESSION_ID,None)
	if cart:
		cart = sum(item['quantity'] for item in cart.values())
	return render(request, 'products/product_list.html', {'data':cart,'products':products,'categories':categories,'min_price':min_price})



#product detail 


def product_detail(request, id):

	try:
		product = get_object_or_404(Product, id=id)
		
		#sizes=ProductAttribute.objects.filter(product=product).values('size__id','size__name').distinct()
		#bases=ProductAttribute.objects.filter(product=product).values('base_id','base__name','price','size__id').distinct()
		sizes=ProductAttribute.objects.filter(product=product).values('size__id','size__name').distinct()
		bases=ProductAttribute.objects.filter(product=product).values('base_id','base__name').distinct()
		
		sauces=ProductAttribute.objects.filter(product=product).values('sauce_id','sauce__name').distinct()
		category=Category.objects.get(id=id)
		cart_product_form = CartAddProductForm()

		context = {
	        'product': product,
	        'category':category,
	        'sizes':sizes,
	        'bases':bases,
	        'sauces':sauces,
			'cart_product_form': cart_product_form,
	        }
	
	except Product.DoesNotExist:
		
		raise Http404 ("this product id does not exit")
	return render(request, 'products/product_detail.html', context)


def search_result(request):

	q=request.GET['q']
	if not q:
		return HttpResponse("please input some texts")
	else:
		product_result=Product.objects.filter( Q(name__icontains=q)|Q(code__icontains=q)).order_by('name', 'price') #filter product results by search word
		category_result=Category.objects.filter(name__icontains=q).order_by('name') #filter category results by search word

		data = chain(product_result, category_result) #from itertools import chain
		return render(request,'products/search_result.html',{'data':data})



def error_404_view(request, exception):
	return render(request, 'products/404.html')