import base64
import logging

from django.http import HttpResponseRedirect
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView

from apps.product.forms import ProductForm
from apps.product.models import Product
from apps.product.tasks import ImageUploadTask
from apps.product.utils import generate_unique_filename

logger = logging.getLogger(__name__)


class ProductListView(ListView):
    model = Product
    template_name = "product-list.html"
    context_object_name = "products"
    paginate_by = 10


class ProductCreateView(View):
    form_class = ProductForm
    template_name = "product-create.html"
    success_url = reverse_lazy("product:product-list")

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            logo_file = form.cleaned_data.get("logo_file")
            filename = generate_unique_filename(logo_file.name)
            encoded_file = base64.b64encode(logo_file.read()).decode("utf-8")
            data = {"file": encoded_file, "name": filename}

            try:
                product = form.save()
                ImageUploadTask().delay(product.uuid, data)
                return redirect(self.success_url)
            except Exception as e:
                logger.error(e)

        return render(request, self.template_name, {"form": form})


class ProductView(View):
    template_name = "product.html"

    def get(self, request, pk):
        product = get_object_or_404(Product, uuid=pk)
        return render(request, self.template_name, {"product": product})


class ProductUpdateView(View):
    form_class = ProductForm
    template_name = "product-update.html"
    success_url = reverse_lazy("product:product-list")

    def get(self, request, pk):
        product = get_object_or_404(Product, uuid=pk)
        form = self.form_class(instance=product)
        return render(request, self.template_name, {"form": form, "product": product})

    def post(self, request, pk):
        product = Product.objects.get(uuid=pk)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            try:
                form.save()
                return redirect(self.success_url)
            except Exception as e:
                logger.error(e)
        return render(request, self.template_name, {"form": form, "product": product})



def productDeleteView(request, pk):
    product = get_object_or_404(Product, uuid=pk)
    product.delete()
    return redirect(reverse('product:product-list'))
