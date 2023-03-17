from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from market.forms import ProductForm, ProductSearchForm
from market.models import Product, CategoryChoice


class ProductIndex(ListView):
    template_name = 'index.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        form = ProductSearchForm(self.request.GET)

        if form.is_valid():
            search = form.cleaned_data.get('search')
            products = Product.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search),
                quantity__gt=0
            ).order_by('name')
        else:
            products = Product.objects.filter(quantity__gt=0).order_by('name')

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = []
        for category_value, category_label in CategoryChoice.choices:
            products_in_category = Product.objects.filter(category=category_value, quantity__gt=0)
            if products_in_category.exists():
                categories.append((category_value, category_label))

        context['form'] = ProductSearchForm(self.request.GET)
        context['categories'] = categories

        return context


class CategoryIndex(ListView):
    template_name = 'products_by_category.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        category_code = self.kwargs['category_code']
        form = ProductSearchForm(self.request.GET)

        if form.is_valid():
            search = form.cleaned_data.get('search')
            products = Product.objects.filter(
                category=category_code,
                quantity__gt=0
            ).filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            ).order_by('name')
        else:
            products = Product.objects.filter(category=category_code, quantity__gt=0).order_by('name')

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_code = self.kwargs['category_code']
        category_name = ''

        for category_value, category_label in CategoryChoice.choices:
            if category_value == category_code:
                category_name = category_label

        context['form'] = ProductSearchForm(self.request.GET)
        context['category_code'] = category_code
        context['category_name'] = category_name
        context['categories'] = CategoryChoice.choices

        return context


class ProductAdd(CreateView):
    template_name = 'product_create.html'
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.pk})


class ProductDetail(DetailView):
    template_name = 'product_detail.html'
    model = Product


class ProductUpdate(UpdateView):
    template_name = 'product_update.html'
    form_class = ProductForm
    model = Product

    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.pk})


class ProductDelete(DeleteView):
    template_name = 'product_delete.html'
    model = Product
    success_url = reverse_lazy('index')

