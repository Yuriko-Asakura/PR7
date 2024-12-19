"""
URL configuration for Magaz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from zoo.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index2),

    path('page_employee.html/', index, name='about'),

    path('pageC_animal/', C_animal, name='C_a'),
    path('page_animal', Animal_page, name='animal_page'),
    path('pageU_animal/<int:animal_id>/', update_animal, name='U_a'),
    path('pageD_animal/<int:animal_id>/', delete_animal, name='D_a'),

    path('page_category/', Category_page, name='category_page'),
    path('pageC_category/', C_category, name='C_category'),
    path('pageD_category/<int:category_id>/', delete_category, name='delete_category'),
    path('pageU_category/<int:category_id>/', update_category, name='update_category'),
   
    path('page_customer/', Customer_page, name='customer_page'),
    path('pageC_customer/', C_customer, name='C_customer'),
    path('pageU_customer/<int:animal_id>/', delete_customer, name='delete_customer'),
    path('pageD_customer/<int:animal_id>/', update_customer, name='update_customer'),
    
    path('page_product/', Product_page, name='product_page'),
    path('pageC_product', C_product, name='C_product'),
    path('pageD_product/<int:product_id>/', delete_product, name='delete_product'),
    path('pageU_product/<int:product_id>/', update_product, name='update_product'),
    

    path('page_employee/', Customer_page, name='page_employee'),
    path('pageC_employee/', C_customer, name='C_em'),
    path('pageU_employee/<int:animal_id>/', update_customer, name='U_em'),
    path('pageD_employee/<int:animal_id>/', delete_customer, name='D_em'),

    path('page_order/', Order_page, name='order_page'),
    path('pageC_order/', C_order, name='C_order'),
    path('pageD_order/<int:order_id>/', delete_order, name='delete_order'),
    path('pageU_order/<int:order_id>/', update_order, name='update_order'),
    
    path('page_orderDetailAnimal/', OrderDetailAnimal_page, name='order_detail_animal_page'),
    path('pageC_orderDetailAnimal/', C_order_detail_animal, name='C_order_detail_animal'),
    path('pageD_orderDetailAnimal/<int:order_detail_id>/', delete_order_detail_animal, name='delete_order_detail_animal'),
    path('pageU_orderDetailAnimal/<int:order_detail_id>/', update_order_detail_animal, name='update_order_detail_animal'),
    
    path('page_orderDetailProduct/', OrderDetailProduct_page, name='order_detail_product_page'),
    path('pageC_orderDetailProduct/', C_order_detail_product, name='C_order_detail_product'),
    path('pageD_orderDetailProduct/<int:order_detail_id>/', delete_order_detail_product, name='delete_order_detail_product'),
    path('pageU_orderDetailProduct/<int:order_detail_id>/', update_order_detail_product, name='update_order_detail_product'),
    
    path('page_orderDetailProduct/', OrderDetailProduct_page, name='order_detail_product_page'),
    path('pageC_orderDetailProduct/', C_order_detail_product, name='C_order_detail_product'),
    path('pageD_orderDetailProduct/<int:order_detail_id>/', delete_order_detail_product, name='delete_order_detail_product'),
    path('pageU_orderDetailProduct/<int:order_detail_id>/', update_order_detail_product, name='update_order_detail_product'),
    
    path('page_supply/', Supply_page, name='supply_page'),
    path('pageC_supply/', C_supply, name='C_supply'),
    path('pageD_supply/<int:supply_id>/', delete_supply, name='delete_supply'),
    path('pageU_supply/<int:supply_id>/', update_supply, name='update_supply'),
    
]
