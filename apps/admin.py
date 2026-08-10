from django.contrib import admin
from django.utils.html import format_html

from .models import Item, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price_display',
        'description_short',
    )

    search_fields = (
        'name',
        'description',
    )

    list_filter = (
        'price',
    )

    readonly_fields = (
        'id',
    )

    ordering = (
        '-id',
    )

    fieldsets = (
        ('Product Information', {
            'fields': (
                'id',
                'name',
                'description',
                'price',
            )
        }),
    )

    @admin.display(description='Price', ordering='price')
    def price_display(self, obj):
        return f'${obj.price}'

    @admin.display(description='Description')
    def description_short(self, obj):
        if len(obj.description) > 50:
            return obj.description[:50] + '...'

        return obj.description

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm(
            'apps.delete_item'
        )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'order_id',
        'get_items_display',
        'total_price_display',
        'status_badge',
        'created_at_display',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'order_id',
        'stripe_session_id',
        'items__name',
    )

    readonly_fields = (
        'order_id',
        'stripe_session_id',
        'created_at',
        'get_items_list',
    )

    filter_horizontal = (
        'items',
    )

    date_hierarchy = 'created_at'

    ordering = (
        '-created_at',
    )

    fieldsets = (
        ('Order Details', {
            'fields': (
                'order_id',
                'total_price',
                'status',
            )
        }),

        ('Items', {
            'fields': (
                'items',
                'get_items_list',
            )
        }),

        ('Payment Information', {
            'fields': (
                'stripe_session_id',
            )
        }),

        ('Timestamps', {
            'fields': (
                'created_at',
            ),
            'classes': (
                'collapse',
            )
        }),
    )

    actions = (
        'mark_as_paid',
        'mark_as_pending',
        'mark_as_cancelled',
    )

    @admin.display(description='Items')
    def get_items_display(self, obj):
        items = obj.items.all()

        if not items.exists():
            return '-'

        names = [item.name for item in items[:2]]

        result = ', '.join(names)

        if items.count() > 2:
            result += f' +{items.count() - 2} more'

        return result

    @admin.display(description='Items List')
    def get_items_list(self, obj):
        items = obj.items.all()

        if not items.exists():
            return 'No items'

        return format_html(
            '<br>'.join(
                f'• {item.name} — ${item.price}'
                for item in items
            )
        )

    @admin.display(
        description='Total Price',
        ordering='total_price',
    )
    def total_price_display(self, obj):
        return f'${obj.total_price}'

    @admin.display(
        description='Status',
        ordering='status',
    )
    def status_badge(self, obj):

        colors = {
            'paid': '#22c55e',
            'pending': '#f59e0b',
            'cancelled': '#ef4444',
            'failed': '#dc2626',
        }

        color = colors.get(
            obj.status,
            '#6b7280',
        )

        return format_html(
            '<span style="'
            'background:{};'
            'color:white;'
            'padding:5px 12px;'
            'border-radius:6px;'
            'font-weight:600;'
            'font-size:12px;'
            'display:inline-block;'
            '">'
            '{}'
            '</span>',
            color,
            obj.get_status_display(),
        )

    @admin.display(
        description='Created',
        ordering='created_at',
    )
    def created_at_display(self, obj):
        return obj.created_at.strftime(
            '%d %b %Y, %H:%M'
        )

    @admin.action(description='Mark selected orders as Paid')
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(
            status=Order.Status.PAID
        )

        self.message_user(
            request,
            f'{updated} order(s) marked as paid.'
        )

    @admin.action(description='Mark selected orders as Pending')
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(
            status=Order.Status.PENDING
        )

        self.message_user(
            request,
            f'{updated} order(s) marked as pending.'
        )

    @admin.action(description='Mark selected orders as Cancelled')
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(
            status=Order.Status.CANCELLED
        )

        self.message_user(
            request,
            f'{updated} order(s) marked as cancelled.'
        )

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm(
            'apps.delete_order'
        )