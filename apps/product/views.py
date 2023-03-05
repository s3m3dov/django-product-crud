import logging

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView, DetailView

from apps.product.forms import ProductForm
from apps.product.models import Product
from apps.product.tasks import ImageUploadTask
from apps.product.utils import prep_file_data

logger = logging.getLogger(__name__)


class ProductListView(ListView):
    model = Product
    template_name = "product-list.html"
    context_object_name = "products"
    paginate_by = settings.PAGINATION_PAGE_SIZE

    def get_queryset(self):
        queryset = super().get_queryset()
        modified = self.request.GET.get("modified", None)
        if modified is not None:
            queryset = queryset.filter(modified=(modified.lower() == "true"))
        return queryset


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
            data = prep_file_data(logo_file)

            try:
                product = form.save()
                ImageUploadTask().delay(product.uuid, data)
                return redirect(self.success_url)
            except Exception as e:
                logger.error(e)

        return render(request, self.template_name, {"form": form})


class ProductDetailView(DetailView):
    model = Product
    template_name = "product-detail.html"


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
        if product.modified:
            return HttpResponse("Product has already been modified")

        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            logo_file = form.cleaned_data.get("logo_file")
            data = prep_file_data(logo_file)

            try:
                form.save()
                product.modified = True
                product.save()
                ImageUploadTask().delay(product.uuid, data)
                return redirect(self.success_url)
            except Exception as e:
                logger.error(e)

        return render(request, self.template_name, {"form": form, "product": product})


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("product:product-list")
