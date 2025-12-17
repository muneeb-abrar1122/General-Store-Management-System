from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .models import *
from .forms import *
@login_required
def dashboard(request):
    # Today's stats
    today = timezone.now().date()
    today_sales = Sale.objects.filter(created_at__date=today)
    
    # Debugging - Check what's in database
    print(f"Today's sales count: {today_sales.count()}")
    for sale in today_sales:
        print(f"Sale #{sale.id}: Total Rs{sale.total_amount}, Cost Rs{sale.total_cost}, Profit Rs{sale.total_profit}")
    
    today_revenue = today_sales.aggregate(total=Sum('final_amount'))['total'] or Decimal('0')
    today_profit = today_sales.aggregate(total=Sum('total_profit'))['total'] or Decimal('0')
    today_sales_count = today_sales.count()
    
    # Low stock products
    low_stock_products = Product.objects.filter(quantity__lte=models.F('min_stock_level'))
    
    # Recent sales
    recent_sales = Sale.objects.all().order_by('-created_at')[:5]
    
    # Total products and customers
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()
    
    context = {
        'today_revenue': today_revenue,
        'today_profit': today_profit,
        'today_sales_count': today_sales_count,
        'low_stock_products': low_stock_products,
        'recent_sales': recent_sales,
        'total_products': total_products,
        'total_customers': total_customers,
    }
    
    print(f"Dashboard Context - Revenue: Rs{today_revenue}, Profit: Rs{today_profit}")
    return render(request, 'dashboard.html', context)
@login_required
def products(request):
    return render(request, 'products.html')

@login_required
def product_list(request):
    products = Product.objects.all().select_related('category', 'supplier')
    low_stock = request.GET.get('low_stock')
    
    if low_stock:
        products = products.filter(quantity__lte=models.F('min_stock_level'))
    
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form, 'product': product})

@login_required
def pos_system(request):
    products = Product.objects.filter(quantity__gt=0)
    customers = Customer.objects.all()
    
    if request.method == 'POST':
        try:
            # Get form data
            customer_id = request.POST.get('customer')
            payment_method = request.POST.get('payment_method', 'CASH')
            bag_charge = Decimal(request.POST.get('bag_charge', 0))
            delivery_charge = Decimal(request.POST.get('delivery_charge', 0))
            other_charge = Decimal(request.POST.get('other_charge', 0))
            
            customer = None
            if customer_id:
                customer = Customer.objects.get(id=customer_id)
            
            # Process sale items
            product_ids = request.POST.getlist('product_id')
            quantities = request.POST.getlist('quantity')
            
            total_amount = Decimal('0')
            total_cost = Decimal('0')
            
            for product_id, quantity in zip(product_ids, quantities):
                if product_id and quantity and int(quantity) > 0:
                    product = Product.objects.get(id=product_id)
                    quantity = int(quantity)
                    
                    if product.quantity >= quantity:
                        item_total = Decimal(str(quantity)) * product.selling_price
                        item_cost = Decimal(str(quantity)) * product.cost_price
                        total_amount += item_total
                        total_cost += item_cost
            
            # Calculate final amount
            extra_charges = bag_charge + delivery_charge + other_charge
            final_amount = total_amount + extra_charges
            total_profit = final_amount - total_cost
            
            # Create sale
            sale = Sale.objects.create(
                customer=customer,
                total_amount=total_amount,
                total_cost=total_cost,
                total_profit=total_profit,
                tax_amount=0,
                bag_charge=bag_charge,
                delivery_charge=delivery_charge,
                other_charge=other_charge,
                final_amount=final_amount,
                payment_method=payment_method
            )
            
            # Create sale items
            for product_id, quantity in zip(product_ids, quantities):
                if product_id and quantity and int(quantity) > 0:
                    product = Product.objects.get(id=product_id)
                    quantity = int(quantity)
                    
                    if product.quantity >= quantity:
                        item_total = Decimal(str(quantity)) * product.selling_price
                        
                        SaleItem.objects.create(
                            sale=sale,
                            product=product,
                            quantity=quantity,
                            price=product.selling_price,
                            total=item_total
                        )
                        
                        # Update product stock
                        product.quantity -= quantity
                        product.save()
            
            return redirect('invoice', sale_id=sale.id)
            
        except Exception as e:
            print(f"POS Error: {e}")
            return render(request, 'sales/pos.html', {
                'products': products,
                'customers': customers,
                'error': str(e)
            })
    
    return render(request, 'sales/pos.html', {
        'products': products,
        'customers': customers
    })

@login_required
def invoice(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, 'sales/invoice.html', {'sale': sale})

@login_required
def sales_list(request):
    sales = Sale.objects.all().select_related('customer').prefetch_related('items__product').order_by('-created_at')
    return render(request, 'sales/sales_list.html', {'sales': sales})

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})

@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/add_customer.html', {'form': form})

@login_required
def sales_report(request):
    # Default to last 30 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Get date range from request
    if request.GET.get('start_date'):
        start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
    if request.GET.get('end_date'):
        end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
    
    sales = Sale.objects.filter(created_at__date__range=[start_date, end_date])
    total_revenue = sales.aggregate(total=Sum('final_amount'))['total'] or Decimal('0')
    total_profit = sales.aggregate(total=Sum('total_profit'))['total'] or Decimal('0')
    total_sales = sales.count()
    
    context = {
        'sales': sales,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'total_sales': total_sales,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'reports/sales_report.html', context)

@login_required
def stock_report(request):
    products = Product.objects.all()
    low_stock_count = products.filter(quantity__lte=models.F('min_stock_level')).count()
    out_of_stock_count = products.filter(quantity=0).count()
    
    context = {
        'products': products,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
    }
    return render(request, 'reports/stock_report.html', context)