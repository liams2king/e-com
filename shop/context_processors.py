from .models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            # Somme des quantités de chaque produit dans le panier
            count = sum(item.quantity for item in cart.cartitem_set.all())
        except Cart.DoesNotExist:
            count = 0
    else:
        # Pour utilisateur non connecté, on peut lire le panier en session
        session_cart = request.session.get('cart', {})
        count = sum(session_cart.values()) if session_cart else 0
    return {'cart_item_count': count}


def cart_totals(request):
    total_cart_price = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            # total_price est un champ ou une méthode qui retourne le prix total de l'item
            total_cart_price = sum(item.get_total_price for item in cart.cartitem_set.all())
        except Cart.DoesNotExist:
            total_cart_price = 0
    else:
        # Pour les non connectés, on calcule le total à partir du panier en session
        from .models import Product
        session_cart = request.session.get('cart', {})
        if session_cart:
            for product_id, qty in session_cart.items():
                try:
                    product = Product.objects.get(id=product_id)
                    total_cart_price += product.price * qty
                except Product.DoesNotExist:
                    pass
    return {'total_cart_price': total_cart_price}
