from django.contrib import admin

from autopark.models import (
    Vehicle,
    Brand,
    Enterprise,
    Driver,
    Manager,
    Routes,
    RoutePoint,
)
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user

# Register your models here.
# admin.site.register(Vehicle)
# |date:"Y-m-d H:i:s"


@admin.register(RoutePoint)
class RoutePointAdmin(admin.ModelAdmin):
    pass


class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "brand",
        "owner",
        "year_manufacture",
        "mileage_value",
        "condition",
        "price_currency",
        "date",
    )
    list_per_page = 50
    actions_on_bottom = True
    search_fields = ("type", "price")


admin.site.register(Vehicle, VehicleAdmin)


class RoutesAdmin(admin.ModelAdmin):
    list_display = ("car", "route", "timestamp")


admin.site.register(Routes, RoutesAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "brand_name",
        "type",
        "tank_volume",
        "seats_number",
        "load_capacity",
    )
    list_per_page = 10
    search_fields = ("brand_name", "type")


admin.site.register(Brand, BrandAdmin)


@admin.register(Enterprise)
class EnterpriseAdmin(GuardedModelAdmin):
    list_display = ("id", "name", "address", "num_of_employee", "zoner")

    def has_module_permission(self, request):
        if super().has_module_permission(request):
            return True
        return self.get_model_objects(request).exists()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        data = self.get_model_objects(request)
        return data

    def has_permission(self, request, obj, action):
        opts = self.opts
        code_name = f"{action}_{opts.model_name}"
        if obj:
            return request.user.has_perm(f"{opts.app_label}.{code_name}", obj)
        else:
            return self.get_model_objects(request).exists()

    def get_model_objects(self, request, action=None, klass=None):
        opts = self.opts
        actions = [action] if action else ["view", "edit", "change", "delete"]
        klass = klass if klass else opts.model
        model_name = klass._meta.model_name
        return get_objects_for_user(
            user=request.user,
            perms=[f"{perm}_{model_name}" for perm in actions],
            klass=klass,
            any_perm=True,
        )

    def has_view_permission(self, request, obj=None):
        return self.has_permission(request, obj, "view")

    def has_change_permission(self, request, obj=None):
        return self.has_permission(request, obj, "change")

    def has_delete_permission(self, request, obj=None):
        return self.has_permission(request, obj, "delete")

    # def has_add_permission(self, request):
    #     return self.has_permission(request, obj , 'add')


# class ReadOnlyAdminMixin:
#     def has_add_permission(self, request):
#         return True
#
#     def has_change_permission(self, request, obj=None):
#         return True
#
#     def has_delete_permission(self, request, obj=None):
#         return True
#
#     def has_view_permission(self, request, obj=None):
#         return True
#
# class EnterpriseAdmin(ReadOnlyAdminMixin,admin.ModelAdmin):
#     list_display = ('name','address','num_of_employee')

# def get_form(self, request, obj=None, change=False, **kwargs): # таким образом мы  не даем право пользователям менять поле
#     form = super().get_form(request, obj, **kwargs)
#     is_superuser = request.user.is_superuser
#
#     if not is_superuser:
#         form.base_fields['name'].disabled = True
#     return form

#
# admin.site.register(Enterprise,EnterpriseAdmin)


class DriverAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "residential_address",
        "phone",
        "job",
        "car",
        "status",
    )


admin.site.register(Driver, DriverAdmin)


class ManagerAdmin(admin.ModelAdmin):
    list_display = ("id",)

    # def get_form(self, request, obj=None, change=False, **kwargs): # таким образом мы  не даем право пользователям менять поле
    #     form = super().get_form(request, obj, **kwargs)
    #     is_superuser = request.user.is_superuser
    #
    #     if not is_superuser:
    #         form.base_fields['name'].disabled = True
    #     return form
    # def get_form(self, request, obj=None, change=False, **kwargs): # таким образом мы  не даем право пользователям менять поле
    #     form = super().get_form(request, obj, **kwargs)
    #     is_superuser = request.user.is_superuser
    #     queryset = super().get_queryset(request)
    #
    #     if not is_superuser and request.user.has_perm('auto_park.change_enterprise'):
    #         return queryset.filter(manager = Manager.indexes)


admin.site.register(Manager, ManagerAdmin)
