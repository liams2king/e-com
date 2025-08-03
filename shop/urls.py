from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import dashboard_home
from .views import (
    dashboard_category_list,
    dashboard_category_create,
    dashboard_category_edit,
    dashboard_category_delete,
)





urlpatterns = [
    # Page d'accueil
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('toggle-wishlist/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('product/<int:product_id>/toggle_wishlist/', views.toggle_wishlist, name='toggle_wishlist'),



    # Produits
    path('products/', views.products, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.search_results, name='search_results'),
    path('admin-dashboard/categories/add/', views.dashboard_category_create, name='dashboard_category_create'),


    # Collections
    path('collections/', views.collections, name='collections'),

    # Panier
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('commander/', views.order_checkout, name='order_checkout'),
    path('commande/confirmee/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('commande/confirmee/<int:order_id>/', views.order_confirmation, name='order_confirmation'),


    path('panier/', views.cart_view, name='cart'),



        
   # Authentification
    path('accounts/login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('admin-dashboard/', views.dashboard_home, name='dashboard_home'),
    path('admin-dashboard/products/', views.dashboard_products, name='dashboard_products'),
    path('admin-dashboard/products/add/', views.dashboard_product_create, name='dashboard_product_create'),
    path('admin-dashboard/products/<int:pk>/edit/', views.dashboard_product_update, name='dashboard_product_update'),
    path('admin-dashboard/products/<int:pk>/delete/', views.dashboard_product_delete, name='dashboard_product_delete'),
    path('admin-dashboard/users/', views.dashboard_users, name='dashboard_users'),
    path('admin-dashboard/orders/', views.dashboard_orders, name='dashboard_orders'),
    path('admin-dashboard/dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/users/', views.dashboard_users, name='dashboard_users'),
    path('admin-dashboard/users/<int:user_id>/', views.user_detail, name='dashboard_user_detail'),
    path('admin-dashboard/users/<int:user_id>/edit/', views.user_edit, name='dashboard_user_edit'),
    path('admin-dashboard/users/<int:user_id>/delete/', views.user_delete, name='dashboard_user_delete'),
    path('admin-dashboard/orders/', views.dashboard_orders, name='dashboard_orders'),

    #categorie
    path('admin-dashboard/categories/add/', views.dashboard_category_create, name='dashboard_categories_add'),
    
    path('admin-dashboard/categories/', dashboard_category_list, name='dashboard_categories'),
    path('admin-dashboard/categories/add/', dashboard_category_create, name='dashboard_categories_add'),
    path('admin-dashboard/categories/<int:category_id>/edit/', dashboard_category_edit, name='dashboard_category_edit'),
    path('admin-dashboard/categories/<int:category_id>/delete/', dashboard_category_delete, name='dashboard_category_delete'),
    # dashboard
    path('admin-dashboard/orders/<int:order_id>/', views.order_detail, name='dashboard_order_detail'),
     path('dashboard/commandes/<int:order_id>/delete/', views.dashboard_order_delete, name='dashboard_order_delete'),
    path('dashboard/commandes/<int:order_id>/update-status/', views.dashboard_update_order_status, name='dashboard_update_order_status'),



    #renitialiser le mot de pass
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
] 
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

