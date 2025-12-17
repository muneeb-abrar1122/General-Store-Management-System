from django.urls import path
from . import views

urlpatterns = [
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    
    # Sales
    path('pos/', views.pos_system, name='pos_system'),
    path('sales/', views.sales_list, name='sales_list'),
    path('invoice/<int:sale_id>/', views.invoice, name='invoice'),
    
    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.add_customer, name='add_customer'),
    
    # Reports
    path('reports/sales/', views.sales_report, name='sales_report'),
    path('reports/stock/', views.stock_report, name='stock_report'),

]