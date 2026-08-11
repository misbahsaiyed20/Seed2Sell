from django.contrib import admin
from .models import Category, Product, FarmerProfile, Order, OrderItem
from accounts.models import CustomUser

# CATEGORY
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# PRODUCT
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'farmer', 'category', 'is_bestseller')
    list_filter = ('is_bestseller', 'farmer', 'category')
    search_fields = ('name', 'description')

    # 🔥 ONLY SHOW FARMERS IN DROPDOWN
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "farmer":
            kwargs["queryset"] = CustomUser.objects.filter(role='farmer')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# FARMER PROFILE
@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'location')
    search_fields = ('user__username', 'phone', 'location')


# ORDER ITEMS INLINE (VERY IMPORTANT - shows products inside order)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# ORDER
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'total_amount',
        'payment_method',
        'payment_status',
        'created_at'
    )
    list_filter = ('payment_method', 'payment_status', 'created_at')
    search_fields = ('customer__username', 'id')
    inlines = [OrderItemInline]


# ORDER ITEM (optional separate view)
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'farmer',
        'price',
        'quantity'
    )
    list_filter = ('farmer',)
    search_fields = ('product__name',)