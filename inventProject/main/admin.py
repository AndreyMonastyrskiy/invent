from django.contrib import admin
from .models import Equipment, EquipmentStatus, EquipmentType, Office
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class EquipmentResource(resources.ModelResource):
    class Meta:
        model = Equipment

# Register your models here.
@admin.register(Equipment)
class EquipmentAdmin(ImportExportModelAdmin):
    resource_classes = [EquipmentResource]
    list_display = ('name', 'accounting_name', 'serial_number', 'inventory_number', 'equipment_type', 'office', 'status', 'description')
    list_filter = ('equipment_type', 'office', 'status')
#class EquipmentAdmin(admin.ModelAdmin):
#    list_display = ('name', 'accounting_name', 'serial_number', 'inventory_number', 'equipment_type', 'office', 'status', 'description')
#    list_filter = ('equipment_type', 'office', 'status')


@admin.register(EquipmentStatus)
class EquipmentStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'adress')
    filter_horizontal = ('managers',)