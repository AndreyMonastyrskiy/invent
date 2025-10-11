import django_filters
from .models import Equipment, EquipmentType, Office, EquipmentStatus

class EquipmentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Название содержит')
    accounting_name = django_filters.CharFilter(lookup_expr='icontains', label='Бухг. наименование содержит')
    serial_number = django_filters.CharFilter(lookup_expr='icontains', label='Серийный номер содержит')
    inventory_number = django_filters.CharFilter(lookup_expr='icontains', label='Инвентарный номер содержит')
    
    equipment_type = django_filters.ModelChoiceFilter(
        queryset=EquipmentType.objects.all(), 
        label='Тип оборудования'
    )
    office = django_filters.ModelChoiceFilter(
        queryset=Office.objects.all(), 
        label='Площадка'
    )
    status = django_filters.ModelChoiceFilter(
        queryset=EquipmentStatus.objects.all(), 
        label='Статус'
    )

    class Meta:
        model = Equipment
        fields = [
            'name', 
            'accounting_name', 
            'serial_number', 
            'inventory_number', 
            'equipment_type', 
            'office', 
            'status'
        ]