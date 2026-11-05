import urllib.parse
from django.shortcuts import get_object_or_404, redirect, render
from .cart import Cart
from .models import Category, Order, OrderItem, Product


def home_view(request):
    categories = Category.objects.all()

    # ⚡ Tủ bánh có sẵn: chỉ lấy những bánh có is_ready_stock = True
    ready_products = Product.objects.filter(
        is_ready_stock=True, is_available=True
    )

    # 🎂 Bánh đặt riêng (Custom): chỉ lấy những bánh có is_ready_stock = False
    custom_products = Product.objects.filter(
        is_ready_stock=False, is_available=True
    )

    cart = Cart(request)

    return render(
        request,
        "bakery/home.html",
        {
            "categories": categories,
            "ready_products": ready_products,
            "custom_products": custom_products,
            "cart": cart,
        },
    )
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect("cart_detail")


# ➕ Thêm hàm xử lý tăng giảm số lượng bánh trong giỏ hàng
# Sửa lại hàm update_cart chuẩn xác thế này:
def update_cart(request, product_id):
    cart = Cart(request)
    action = request.GET.get("action")  # Nhận hành động tăng (+) hay giảm (-)
    product = get_object_or_404(Product, id=product_id)
    product_id_str = str(product_id)

    if product_id_str in cart.cart:
        current_qty = cart.cart[product_id_str]["quantity"]
        if action == "increase":
            if current_qty < product.stock:
                cart.update(product_id, current_qty + 1)
        elif action == "decrease":
            cart.update(product_id, current_qty - 1)

    return redirect("cart_detail")


def cart_detail(request):
    cart = Cart(request)
    cart_items = []
    for product_id, item in cart.cart.items():
        product = Product.objects.get(id=product_id)
        cart_items.append(
            {
                "product": product,
                "quantity": item["quantity"],
                "total_price": int(item["price"]) * item["quantity"],
            }
        )
    return render(
        request,
        "bakery/cart.html",
        {"cart_items": cart_items, "total_price": cart.get_total_price()},
    )


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart_detail")


def checkout(request):
    cart = Cart(request)
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        customer_phone = request.POST.get("customer_phone")
        fulfillment_type = request.POST.get("fulfillment_type")

        if fulfillment_type == "pickup":
            is_pickup = True
            shipping_address = ""
            pickup_time = request.POST.get("pickup_time", "")
            note = f"[Đến lấy lúc: {pickup_time}] " + request.POST.get(
                "note", ""
            )
        else:
            is_pickup = False
            shipping_address = request.POST.get("shipping_address", "")
            note = request.POST.get("note", "")

        order = Order.objects.create(
            customer_name=customer_name,
            customer_phone=customer_phone,
            shipping_address=shipping_address,
            is_pickup=is_pickup,
            note=note,
            total_amount=cart.get_total_price(),
        )

        # ➕ TẠO ORDER ITEM VÀ TRỪ TRỰC TIẾP SỐ LƯỢNG TỒN KHO (STOCK)
        for product_id, item in cart.cart.items():
            product = Product.objects.get(id=product_id)
            qty = item["quantity"]

            # Lưu chi tiết đơn hàng
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                price=product.price,
                cake_size=item.get("cake_size", ""),
            )

            # Giảm số lượng tồn kho trong kho của quán
            if product.stock >= qty:
                product.stock -= qty
            else:
                product.stock = 0  # Tránh bị âm kho
            product.save()

        # Xóa giỏ hàng sau khi đặt thành công
        cart.clear()

        # Nếu chọn Ship -> Chuyển hướng sang Zalo
        if not is_pickup:
            zalo_phone = "0834420122"
            zalo_msg = (
                f"Chào Leila Cake, mình vừa đặt đơn hàng mã {order.order_code} "
                f"(Tên: {customer_name} - SĐT: {customer_phone}).\n"
                f"📍 Địa chỉ nhận: {shipping_address}\n"
                f"👉 Shop check khoảng cách và báo phí ship giúp mình nhé!"
            )
            encoded_msg = urllib.parse.quote(zalo_msg)
            zalo_url = f"https://zalo.me/{zalo_phone}?text={encoded_msg}"
            return redirect(zalo_url)

        return redirect("order_success", order_code=order.order_code)

    return render(
        request,
        "bakery/checkout.html",
        {"cart": cart, "total_price": cart.get_total_price()},
    )


def order_success(request, order_code):
    order = get_object_or_404(Order, order_code=order_code)
    bank_id = "MB"
    account_no = "0834420122"
    account_name = "LEILA CAKE"

    qr_url = f"https://img.vietqr.io/image/{bank_id}-{account_no}-compact2.png?amount={order.total_amount}&addInfo={order.order_code}&accountName={account_name}"

    return render(
        request,
        "bakery/success.html",
        {"order": order, "qr_url": qr_url},
    )
def lookup_order(request):
    order = None
    order_code = request.GET.get("code", "").strip()
    if order_code:
        try:
            order = Order.objects.get(order_code__iexact=order_code)
        except Order.DoesNotExist:
            order = None
    return render(
        request,
        "bakery/lookup.html",
        {"order": order, "searched_code": order_code},
    )