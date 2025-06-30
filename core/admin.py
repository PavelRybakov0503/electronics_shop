from django.contrib import admin
from django.utils.html import format_html
from .models import Contact, Product, NetworkNode, Employee


class ContactInline(admin.StackedInline):
    model = Contact
    extra = 0


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


class NetworkNodeProductsInline(admin.TabularInline):
    model = NetworkNode.products.through
    extra = 0
    verbose_name = "Продукт"
    verbose_name_plural = "Продукты"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'country', 'city', 'street', 'house_number')
    search_fields = ('email', 'country', 'city')
    list_filter = ('country', 'city')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'release_date')
    search_fields = ('name', 'model')
    list_filter = ('release_date',)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'node_type_display',
        'hierarchy_level',
        'supplier_link',
        'debt',
        'created_at',
        'is_active'
    )
    list_filter = ('contact__city', 'contact__country', 'node_type', 'created_at')
    search_fields = ('name', 'contact__city', 'contact__country')
    inlines = [NetworkNodeProductsInline]
    actions = ['clear_debt']
    readonly_fields = ('created_at', 'hierarchy_level')
    exclude = ('products',)

    def node_type_display(self, obj):
        return obj.get_node_type_display()
    node_type_display.short_description = 'Тип звена'

    def supplier_link(self, obj):
        if obj.supplier:
            return format_html(
                '<a href="{}">{}</a>',
                f'/admin/core/networknode/{obj.supplier.id}/change/',
                obj.supplier.name
            )
        return "-"
    supplier_link.short_description = 'Поставщик'

    @admin.action(description="Очистить задолженность перед поставщиком")
    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0)
        self.message_user(request, f"Задолженность очищена для {updated} объектов")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('contact', 'supplier')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'network_node', 'is_active')
    list_filter = ('is_active', 'network_node__node_type')
    search_fields = ('user__username', 'network_node__name')
    raw_id_fields = ('user', 'network_node')
