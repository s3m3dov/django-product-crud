from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import ProductForm
from .models import Product


# Create your views here.

def productListView(request):
    products = Product.objects.all()
    return render(request, "product-list.html", {'products': products})


def productCreateView(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect(reverse('product:product-list'))
            except Exception as e:
                print("Error: ", e)
    else:
        form = ProductForm()
    return render(request, 'product-create.html', {'form': form})


def productView(request, pk):
    product = Product.objects.get(uuid=pk)
    return render(request, 'product.html', {'product': product})


def productUpdateView(request, pk):
    product = Product.objects.get(uuid=pk)
    print("Product: ", product)
    form = ProductForm(request.POST, instance=product)
    if form.is_valid():
        form.save()
        return redirect(reverse('product:product-list'))
    return render(request, 'product-update.html', {'form': form})


def productUpdateView(request, pk):
    product = get_object_or_404(Product, uuid=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            # messages.success(request, f"{product.name} has been updated successfully!")
            return redirect(reverse('product:product-list'))
        else:
            # messages.error(request, "Failed to update product. Please correct the errors below.")
            print("Error: ", form.errors)
    else:
        form = ProductForm(instance=product)

    return render(request, 'product-update.html', {'form': form})


def productDeleteView(request, pk):
    product = get_object_or_404(Product, uuid=pk)
    product.delete()
    return redirect(reverse('product:product-list'))
