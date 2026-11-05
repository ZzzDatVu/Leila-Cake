from django.contrib import admin
from .models import Category, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "is_ready_stock",
        "is_available",
    )
    list_filter = ("category", "is_ready_stock", "is_available")
    list_editable = (
        "price",
        "is_ready_stock",
        "is_available",
    )  # Bật/tắt công tắc ngay trên danh sách
    search_fields = ("name",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_code",
        "customer_name",
        "customer_phone",
        "total_amount",
        "status",
        "created_at",
    )
    list_filter = ("status", "is_pickup", "created_at")
    list_editable = ("status",)  # Đổi trạng thái đơn cực nhanh
    search_fields = ("order_code", "customer_name", "customer_phone")
    inlines = [OrderItemInline]