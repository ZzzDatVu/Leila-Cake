from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "cart/update/<int:product_id>/",
        views.update_cart,
        name="update_cart",
    ),  # ➕ Thêm route này
    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("checkout/", views.checkout, name="checkout"),
    path(
        "success/<str:order_code>/",
        views.order_success,
        name="order_success",
    ),
    path("lookup/", views.lookup_order, name="lookup_order"),
]