from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import Product, CartItem, Cart
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import ProductForm
from .models import Product, Order, User
from django.db.models import F, Sum, FloatField
from .models import OrderItem, Product, Order
from django.utils.timezone import now, timedelta
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.views.decorators.http import require_POST
from .forms import UserForm
from .forms import CategoryForm, Category
from django.utils.text import slugify
from .forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail
from .forms import OrderForm
from django.db.models import Avg, Sum, Count, F, FloatField
from django.http import JsonResponse
from .models import Wishlist, Product





def index(request):
    item_name = request.GET.get('item_name', '')

    if item_name:
        products_list = Product.objects.filter(name__icontains=item_name)
    else:
        products_list = Product.objects.all()

    paginator = Paginator(products_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        for product in page_obj:
            product.is_liked = product.liked_by.filter(id=request.user.id).exists()
    else:
        for product in page_obj:
            product.is_liked = False

    total_cart_quantity = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        total_cart_quantity = sum(item.quantity for item in cart.cartitem_set.all())

    return render(request, 'shop/index.html', {
        'products': page_obj,
        'page_obj': page_obj,
        'total_cart_quantity': total_cart_quantity,
    })




def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
        try:
            send_mail(
                subject=f"[contact] {form.cleaned_data['subject']}", 
                message=form.cleaned_data['message'],
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['nguewawilliam@hotmail.com'],
                fail_silently=False
            )
        except Exception as e:
            print("Erreur d'envoi d'email :", e)
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'shop/contact.html', {'form': form})

def collections(request):
    return render(request, 'shop/collections.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'shop/products.html', {'products': products})


def search_results(request):
    item_name = request.GET.get('item_name', '')
    products = Product.objects.filter(name__icontains=item_name)

    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/search_results.html', {
        'products': page_obj,
        'item_name': item_name,
        'page_obj': page_obj,
    })



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
    else:
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        if product_id_str in cart:
            cart[product_id_str] += 1
        else:
            cart[product_id_str] = 1
        request.session['cart'] = cart

    messages.success(request, f"{product.name} ajouté au panier.")
    return redirect('index')




@login_required
def cart_view(request):
    items = []
    total = 0

    if request.user.is_authenticated:
        cart = request.user.cart
        cart_items = cart.cartitem_set.all()
        items = cart_items
        total = sum(item.get_total_price for item in cart_items)
    else:
        session_cart = request.session.get('cart', {})
        for product_id, qty in session_cart.items():
            product = get_object_or_404(Product, id=product_id)
            product.quantity = qty
            product.total_price = product.price * qty
            items.append(product)
            total += product.total_price

    return render(request, 'shop/cart.html', {
        'items': items,
        'total': total
    })


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart=request.user.cart)
    item.delete()
    messages.success(request, "Produit supprimé du panier.")
    return redirect('cart_view')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Bienvenue ! Votre compte a été créé avec succès.")
            return redirect('index')  # adapte 'index' si besoin
    else:
        form = CustomUserCreationForm()

    return render(request, 'shop/register.html', {'form': form})

@login_required
def update_cart(request):
    if request.method == 'POST':
        cart = request.user.cart
        for item in cart.cartitem_set.all():
            key = f"quantity_{item.id}"
            if key in request.POST:
                try:
                    qty = int(request.POST[key])
                    if qty > 0:
                        item.quantity = qty
                        item.save()
                    else:
                        # Si la quantité est 0 ou négative, supprimer l'item
                        item.delete()
                except ValueError:
                    pass  # Ignore si la quantité n'est pas un entier valide
    return redirect('cart_view')

@login_required
def clear_cart(request):
    if request.user.is_authenticated:
        cart = request.user.cart
        cart.cartitem_set.all().delete()
    else:
        request.session['cart'] = {}
    messages.success(request, "Votre panier a été vidé.")
    return redirect('cart_view')


def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
def dashboard_home(request):
    return render(request, 'shop/dashboard/dashboard_home.html')




@staff_member_required
def dashboard_home(request):
    return render(request, 'shop/dashboard/dashboard_base.html')



def dashboard_products(request):
    products = Product.objects.all()
    return render(request, 'shop/dashboard/products_list.html', {'products': products})

def dashboard_product_create(request):
    print("Execution de la vue de création d'un produit")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.cleaned_data['name'])  # Affiche la valeur du champ 'name'
            print(form.cleaned_data['description'])  # Affiche la description
            print(form.cleaned_data['price'])  # Affiche le prix
            return redirect('dashboard_products')

    else:
        form = ProductForm()
    return render(request, 'shop/dashboard/product_form.html', {'form': form})

def dashboard_product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('dashboard_products')
    return render(request, 'shop/dashboard/product_form.html', {'form': form})

def dashboard_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard_products')
    return render(request, 'shop/dashboard/product_confirm_delete.html', {'product': product})



def dashboard_users(request):
    users = User.objects.all()
    return render(request, 'shop/dashboard/dashboard_users.html', {'users': users})


def dashboard_orders(request):
    return render(request, 'shop/dashboard/orders.html') 


def dashboard_orders(request):
    orders = Order.objects.all()
    return render(request, 'shop/dashboard/orders.html', {'orders': orders})



def dashboard(request):
    # Statistiques globales
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    out_of_stock = Product.objects.filter(stock=0).count()

    # Revenu total
    total_revenue = OrderItem.objects.aggregate(
        total=Sum(F('product__price') * F('quantity'), output_field=FloatField())
    )['total'] or 0

    # Panier moyen
    average_cart = OrderItem.objects.aggregate(
        avg=Avg(F('product__price') * F('quantity'), output_field=FloatField())
    )['avg'] or 0

    # Statistiques des statuts de commande
    status_labels = ['Livrée', 'En attente', 'Annulée', 'Traitée']
    status_data = [
        Order.objects.filter(status='Livrée').count(),
        Order.objects.filter(status='En attente').count(),
        Order.objects.filter(status='Annulée').count(),
        Order.objects.filter(status='Traitée').count(),
    ]

    # Commandes des 7 derniers jours
    today = now().date()
    week_ago = today - timedelta(days=6)

    orders_last_week = (
        Order.objects.filter(created_at__date__gte=week_ago)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    dates = []
    counts = []
    for i in range(7):
        day = week_ago + timedelta(days=i)
        dates.append(day.strftime('%Y-%m-%d'))
        day_data = next((item for item in orders_last_week if item['date'] == day), None)
        counts.append(day_data['count'] if day_data else 0)

    # Produits les plus aimés (wishlist)
    most_liked_products = Product.objects.annotate(
        num_likes=Count('wishlist')
    ).order_by('-num_likes')[:10]

    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_revenue': total_revenue,
        'out_of_stock': out_of_stock,
        'average_cart': average_cart,

        'chart_labels': dates,
        'chart_data': counts,

        'status_labels': status_labels,
        'status_data': status_data,

        'most_liked_products': most_liked_products,  # ❤️
    }

    return render(request, 'shop/dashboard/dashboard.html', context)



def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'shop/dashboard/user_detail.html', {'user': user})

@staff_member_required
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard_users')  # ou vers la page détail user
    else:
        form = UserForm(instance=user)

    return render(request, 'shop/dashboard/user_edit.html', {'form': form, 'user': user})


@require_POST
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('dashboard_users')


@staff_member_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


 
def dashboard_category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.slug = slugify(category.name)  # Génère le slug automatiquement
            category.save()
            return redirect('dashboard_products')  # Redirige vers la liste des produits
    else:
        form = CategoryForm()

    return render(request, 'shop/dashboard/category_create.html', {'form': form})


def dashboard_category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/dashboard/category_list.html', {'categories': categories})


def dashboard_category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.slug = slugify(updated.name)
            updated.save()
            return redirect('dashboard_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'shop/dashboard/category_create.html', {'form': form})

def dashboard_category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('dashboard_categories')

@login_required
def create_order(request):
    # Récupérer le panier de l'utilisateur
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        # Pas de panier, redirige vers panier ou page d'accueil
        return redirect('cart_view')

    cart_items = cart.cartitem_set.all()

    if not cart_items:
        # Panier vide, on redirige
        return redirect('cart_view')

    # Créer une commande liée à l'utilisateur
    order = Order.objects.create(user=request.user)

    # Pour chaque item du panier, créer un OrderItem
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price  # si tu veux stocker prix au moment de la commande
        )

    # Vider le panier
    cart_items.delete()

    # Optionnel : tu peux vider aussi la session 'cart' si tu la gères
    if 'cart' in request.session:
        del request.session['cart']

    # Rediriger vers page de confirmation de commande
    return redirect('order_confirmation')



@login_required
def order_checkout(request):
    cart = request.user.cart
    cart_items = cart.cartitem_set.all()

    if not cart_items:
        messages.error(request, "Votre panier est vide.")
        return redirect('cart_view')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.status = 'En attente'  # statut par défaut
            order.save()

            # Création des OrderItems
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )

            # Vider le panier
            cart.cartitem_set.all().delete()

            messages.success(request, "Votre commande a été enregistrée avec succès.")
            return redirect('order_confirmation', order_id=order.id)

    else:
        form = OrderForm()

    return render(request, 'shop/order_checkout.html', {
        'form': form,
        'cart_items': cart_items
    })



@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = OrderItem.objects.filter(order=order)
    total_price = sum(item.product.price * item.quantity for item in items)

    return render(request, 'shop/commande_confirmee.html', {
        'order': order,
        'items': items,
        'total_price': total_price,
    })

def confirmation_page(request):
    return render(request, "shop/commande_confirmee.html")


@login_required
def dashboard_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'shop/dashboard/orders.html', {'orders': orders})



@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.orderitem_set.all()

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, "Statut mis à jour avec succès.")
        else:
            messages.error(request, "Statut invalide.")

        return redirect('order_detail', order_id=order_id)

    return render(request, 'shop/dashboard/order_detail.html', {
        'order': order,
        'items': items,
        'status_choices': Order.STATUS_CHOICES,
    })


@require_POST
def dashboard_update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    status = request.POST.get('status')
    
    # Optionnel : tu peux vérifier que le statut est bien dans les choix possibles
    valid_statuses = ['En attente', 'En cours', 'Livrée', 'Annulée']
    if status in valid_statuses:
        order.status = status
        order.save()
    
    return redirect('dashboard_order_detail', order_id=order_id)


@staff_member_required
@require_POST
def dashboard_order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, "Commande supprimée avec succès.")
    return redirect('dashboard_orders')




@login_required
@require_POST
def toggle_wishlist(request, product_id):
    user = request.user
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Produit non trouvé.'}, status=404)

    if product.liked_by.filter(id=user.id).exists():
        product.liked_by.remove(user)
        liked = False
    else:
        product.liked_by.add(user)
        liked = True

    return JsonResponse({'liked': liked})

@login_required
def wishlist_view(request):
    user = request.user
    wishlist_products = user.liked_products.all()  # produits aimés par l'utilisateur
    context = {
        'wishlist_products': wishlist_products,
    }
    return render(request, 'shop/wishlist.html', context)