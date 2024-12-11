from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView

from fitnessEcommerceApp.orders.models import Cart, CartItem
from fitnessEcommerceApp.products.forms import CreateProductForm, EditProductForm
from fitnessEcommerceApp.products.models import Product


# Create your views here.
class ProductsView(ListView):
    template_name = 'products/products.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 6


class ProductInformation(DetailView):
    template_name = 'products/product-info.html'
    model = Product
    context_object_name = 'product'


class AddProductToCart(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        user = request.user

        # Ensure the user has a cart otherwise creates one
        cart, created = Cart.objects.get_or_create(user=user)

        product = Product.objects.get(id=pk)

        cart_item = CartItem.objects.filter(cart=cart, product=product).first()

        if cart_item:
            cart_item.quantity += 1

            cart_item.save()
        else:
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=1
            )

        return redirect('all-products')


class AddProduct(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'products/add-product.html'
    form_class = CreateProductForm
    success_url = reverse_lazy('all-products')
    model = Product
    permission_required = 'products.add_product'


class EditProduct(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'products/edit-product.html'
    form_class = EditProductForm
    model = Product
    permission_required = 'products.change_product'

    def get_success_url(self):
        return reverse_lazy(
            'product-info',
            kwargs={'pk': self.object.pk}
        )


class DeleteProduct(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'products/delete-product.html'
    success_url = reverse_lazy('all-products')
    model = Product
    permission_required = 'products.delete_product'