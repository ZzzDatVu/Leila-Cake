from .models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product, quantity=1, cake_size=""):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
                "name": product.name,
                "cake_size": cake_size,
            }
        self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session["cart"]
        self.save()

    def get_total_price(self):
        return sum(
            int(item["price"]) * item["quantity"] for item in self.cart.values()
        )

from .models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product, quantity=1, cake_size=""):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
                "name": product.name,
                "cake_size": cake_size,
            }

        # Kiểm tra nếu vượt quá tồn kho thì gạt lại hoặc cộng dồn trong giới hạn
        self.cart[product_id]["quantity"] += quantity
        self.save()

    # ➕ Thêm hàm cập nhật số lượng cụ thể (dùng cho nút tăng giảm trong giỏ hàng)
    def update(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            if quantity > 0:
                self.cart[product_id]["quantity"] = int(quantity)
            else:
                del self.cart[product_id]
            self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session["cart"]
        self.save()

    def get_total_price(self):
        return sum(
            int(item["price"]) * item["quantity"] for item in self.cart.values()
        )