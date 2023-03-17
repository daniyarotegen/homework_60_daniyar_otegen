from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView
from market.forms import ProductForm, ProductSearchForm
from market.models import Product, CategoryChoice


class IndexView(ListView):
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


class CategoryView(ListView):
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


class AddView(CreateView):
    template_name = 'product_create.html'
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.pk})


def detailed_view(request: WSGIRequest, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', context={'product': product, 'categories': CategoryChoice.choices})


def update_view(request: WSGIRequest, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product.name = form.clean_name()
            product.description = form.cleaned_data['description']
            product.image = form.cleaned_data['image']
            product.category = form.cleaned_data['category']
            product.quantity = form.cleaned_data['quantity']
            product.price = form.cleaned_data['price']
            product.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(initial={
            'name': product.name,
            'description': product.description,
            'image': product.image,
            'category': product.category,
            'quantity': product.quantity,
            'price': product.price
        })
    return render(request, 'product_update.html', {'form': form, 'product': product})


def delete_view(request: WSGIRequest, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('index')
    context = {
        'product': product,
    }
    return render(request, 'product_delete.html', context)
