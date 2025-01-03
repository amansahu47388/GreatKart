from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                if key == 'csrfmiddlewaretoken':
                    continue
                    
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    # Check if item with same variations exists
    cart_items = CartItem.objects.filter(product=product, cart=cart)
    
    if cart_items.exists():
        # Check if current variation exists in cart items
        exists = False
        for cart_item in cart_items:
            if list(cart_item.variations.all()) == product_variation:
                cart_item.quantity += 1
                cart_item.save()
                exists = True
                break
        
        if not exists:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1,
            )
            if product_variation:
                cart_item.variations.add(*product_variation)
            cart_item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1,
        )
        if product_variation:
            cart_item.variations.add(*product_variation)
        cart_item.save()
    
    return redirect('cart')

@login_required(login_url='login')
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('product')
        
        # Group cart items by product and variations
        grouped_items = {}
        for cart_item in cart_items:
            variations = cart_item.get_variations()
            key = (cart_item.product.id, tuple(sorted(variations.items())))
            
            if key in grouped_items:
                grouped_items[key]['quantity'] += cart_item.quantity
                grouped_items[key]['sub_total'] += cart_item.sub_total()
            else:
                grouped_items[key] = {
                    'cart_item': cart_item,
                    'quantity': cart_item.quantity,
                    'sub_total': cart_item.sub_total(),
                    'variations': variations
                }
            
            total += cart_item.sub_total()
            quantity += cart_item.quantity
            
        tax = (2 * total)/100
        grand_total = total + tax
        
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': grouped_items.values(),
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)

def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def is_product_in_cart(request, product_id):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        return CartItem.objects.filter(product_id=product_id, cart=cart).exists()
    except Cart.DoesNotExist:
        return False