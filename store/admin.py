from django.contrib import admin


from store.models import Store, Product, Location


admin.site.register(Product)
admin.site.register(Location)


@admin.action(description='Обнулить задолженность')
def cancel_debt(queryset):
    queryset.update(debt=0.00)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'debt')
    list_filter = ('location__city',)
    actions = [cancel_debt]