import uuid
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")

    class Meta:
        verbose_name_plural = "Danh mục sản phẩm"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Danh mục",
    )
    name = models.CharField(max_length=200, verbose_name="Tên bánh")
    price = models.DecimalField(
        max_digits=10, decimal_places=0, verbose_name="Giá bán (Đồng)"
    )
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        verbose_name="Hình ảnh bánh",
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Mô tả / Thành phần"
    )
    stock = models.PositiveIntegerField(
        default=10, verbose_name="Số lượng tồn kho (Số bánh sẵn có)"
    )
    is_ready_stock = models.BooleanField(
        default=True,
        verbose_name="Bánh có sẵn tại tủ (True) / Đặt trước (False)",
    )
    is_available = models.BooleanField(
        default=True, verbose_name="Còn hàng (Bật/Tắt công tắc)"
    )

    class Meta:
        verbose_name_plural = "Danh sách bánh"

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Chờ xác nhận"),
        ("PROCESSING", "Đang chuẩn bị bánh"),
        ("COMPLETED", "Hoàn thành / Đã giao"),
        ("CANCELLED", "Đã hủy"),
    )

    order_code = models.CharField(
        max_length=10, unique=True, editable=False, blank=True
    )
    customer_name = models.CharField(
        max_length=100, verbose_name="Tên khách hàng"
    )
    customer_phone = models.CharField(
        max_length=15, verbose_name="Số điện thoại"
    )
    shipping_address = models.TextField(
        blank=True, null=True, verbose_name="Địa chỉ giao hàng (Nếu ship)"
    )
    is_pickup = models.BooleanField(
        default=False, verbose_name="Tự đến tiệm lấy bánh"
    )
    note = models.TextField(
        blank=True, null=True, verbose_name="Ghi chú (Viết chữ lên bánh/Giờ lấy)"
    )
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=0, default=0, verbose_name="Tổng tiền"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
        verbose_name="Trạng thái",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Thời gian đặt"
    )

    class Meta:
        verbose_name_plural = "Quản lý Đơn hàng"

    def save(self, *args, **kwargs):
        if not self.order_code:
            self.order_code = f"LC-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_code} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
    price = models.DecimalField(
        max_digits=10, decimal_places=0, verbose_name="Giá lúc mua"
    )
    cake_size = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Kích thước bánh (14cm/16cm...)",
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"