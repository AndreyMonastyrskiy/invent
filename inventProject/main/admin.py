from django.contrib import admin
from .models import Equipment, EquipmentStatus, EquipmentType, Office, Manufacturer, ModelName, СonsumableType, Consumable
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, DateWidget

class EquipmentResource(resources.ModelResource):
    equipment_type = fields.Field(
        column_name='equipment_type',
        attribute='equipment_type',
        widget=ForeignKeyWidget(EquipmentType, 'name')
    )
    office = fields.Field(
        column_name='office',
        attribute='office',
        widget=ForeignKeyWidget(Office, 'name')
    )
    status = fields.Field(
        column_name='status',
        attribute='status',
        widget=ForeignKeyWidget(EquipmentStatus, 'name')
    )
    in_work_date = fields.Field(
        column_name='in_work_date',
        attribute='in_work_date',
        widget=DateWidget(format='%d.%m.%Y')
    )
    warranty_date = fields.Field(
        column_name='warranty_date',
        attribute='warranty_date',
        widget=DateWidget(format='%d.%m.%Y')
    )
    manufacturer = fields.Field(
        column_name='manufacturer',
        attribute='manufacturer',
        widget=ForeignKeyWidget(Manufacturer, 'name')
    )
    model = fields.Field(
        column_name='model',
        attribute='model',
        widget=ForeignKeyWidget(ModelName, 'name')
    )
    class Meta:
        model = Equipment


class СonsumableResource(resources.ModelResource):
    consumable_type = fields.Field(
        column_name='consumable_type',
        attribute='consumable_type',
        widget=ForeignKeyWidget(СonsumableType, 'name')
    )
    manufacturer = fields.Field(
        column_name='manufacturer',
        attribute='manufacturer',
        widget=ForeignKeyWidget(Manufacturer, 'name')
    )
    model = fields.Field(
        column_name='model',
        attribute='model',
        widget=ForeignKeyWidget(ModelName, 'name')
    )
    office = fields.Field(
        column_name='office',
        attribute='office',
        widget=ForeignKeyWidget(Office, 'name')
    )
    in_work_date = fields.Field(
        column_name='in_work_date',
        attribute='in_work_date',
        widget=DateWidget(format='%d.%m.%Y')
    )
    warranty_date = fields.Field(
        column_name='warranty_date',
        attribute='warranty_date',
        widget=DateWidget(format='%d.%m.%Y')
    )
    

    class Meta:
        model = Consumable


class ManufacturerResource(resources.ModelResource):
    class Meta:
        model = Manufacturer


class ModelNameResource(resources.ModelResource):
    class Meta:
        model = ModelName

# Register your models here.
@admin.register(Equipment)
class EquipmentAdmin(ImportExportModelAdmin):
    resource_classes = [EquipmentResource]
    list_display = ('name', 'accounting_name', 'serial_number', 'inventory_number', 'equipment_type', 'manufacturer', 'model', 'office', 'status', 'in_work_date', 'warranty_date', 'description')
    list_filter = ('equipment_type', 'office', 'status')

@admin.register(Consumable)
class СonsumableAdmin(ImportExportModelAdmin):
    resource_classes = [СonsumableResource]
    list_display = ('name', 'accounting_name', 'consumable_type', 'manufacturer', 'model', 'office', 'room', 'in_work_date', 'warranty_date', 'count', 'write_off_count', 'description')
    list_filter = ('consumable_type', 'office')

@admin.register(EquipmentStatus)
class EquipmentStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(СonsumableType)
class СonsumableTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'adress')
    filter_horizontal = ('managers',)

@admin.register(Manufacturer)
class ManufacturerAdmin(ImportExportModelAdmin):
    resource_classes = [ManufacturerResource]
    list_display = ('name', 'description')

@admin.register(ModelName)
class ModelNameAdmin(ImportExportModelAdmin):
    resource_classes = [ModelNameResource]
    list_display = ('name', 'description')
'''
@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(ModelName)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
'''