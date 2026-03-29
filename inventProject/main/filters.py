import django_filters
from .models import Equipment, EquipmentType, Office, EquipmentStatus, Consumable, ConsumableType, Manufacturer, ModelName, MemoryType, StorageType, OperatingSystem

class EquipmentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Название:')
    accounting_name = django_filters.CharFilter(lookup_expr='icontains', label='Наименование по бухгалтерии:')
    serial_number = django_filters.CharFilter(lookup_expr='icontains', label='Серийный номер:')
    inventory_number = django_filters.CharFilter(lookup_expr='icontains', label='Инвентарный номер:')
    
    equipment_type = django_filters.ModelChoiceFilter(
        queryset=EquipmentType.objects.all(), 
        label='Тип оборудования:'
    )
    office = django_filters.ModelChoiceFilter(
        queryset=Office.objects.all(), 
        label='Площадка:'
    )
    status = django_filters.ModelChoiceFilter(
        queryset=EquipmentStatus.objects.all(), 
        label='Статус:'
    )
    memory_type = django_filters.ModelChoiceFilter(
        queryset=MemoryType.objects.all(), 
        label='Тип ОЗУ:'
    )
    memory_size = django_filters.NumberFilter(lookup_expr='icontains', label='Размер ОЗУ:')
    storage_type = django_filters.ModelChoiceFilter(
        queryset=StorageType.objects.all(), 
        label='Тип накопителя:'
    )
    storage_size = django_filters.NumberFilter(lookup_expr='icontains', label='Размер накопителя')
    operating_system = django_filters.ModelChoiceFilter(
        queryset=OperatingSystem.objects.all(), 
        label='ОС:'
    )
    room = django_filters.CharFilter(lookup_expr='icontains', label='Помещение:')

    def __init__(self, *args, **kwargs):
        request = kwargs.get('request')
        super(EquipmentFilter, self).__init__(*args, **kwargs)
        if request and request.user:
            user = request.user
            self.filters['office'].queryset = user.managed_offices.all()

    description = django_filters.CharFilter(lookup_expr='icontains', label='Описание:')

    class Meta:
        model = Equipment
        fields = [
            'name', 
            'accounting_name', 
            'serial_number', 
            'inventory_number', 
            'equipment_type', 
            'office', 
            'status',
            'description'
        ]


class ConsumableFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Название:')
    accounting_name = django_filters.CharFilter(lookup_expr='icontains', label='Наименование по бухгалтерии:')
    
    consumable_type = django_filters.ModelChoiceFilter(
        queryset=ConsumableType.objects.all(), 
        label='Тип расходника:'
    )
    manufacturer = django_filters.ModelChoiceFilter(
        queryset=Manufacturer.objects.all(), 
        label='Производитель:'
    )
    model = django_filters.ModelChoiceFilter(
        queryset=ModelName.objects.all(), 
        label='Модель:'
    )
    office = django_filters.ModelChoiceFilter(
        queryset=Office.objects.all(), 
        label='Площадка:'
    )
    room = django_filters.CharFilter(lookup_expr='icontains', label='Помещение:')
    description = django_filters.CharFilter(lookup_expr='icontains', label='Описание:')
    
    def __init__(self, *args, **kwargs):
        request = kwargs.get('request')
        super(ConsumableFilter, self).__init__(*args, **kwargs)
        if request and request.user:
            user = request.user
            self.filters['office'].queryset = user.managed_offices.all()

    
    class Meta:
        model = Consumable
        fields = [
            'name', 
            'accounting_name', 
            'consumable_type', 
            'manufacturer', 
            'model', 
            'office',
            'room',
            'description'
        ]