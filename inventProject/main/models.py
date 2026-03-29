from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class MemoryType(models.Model):
    name = models.CharField(max_length=256, help_text="Тип ОЗУ")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тип ОЗУ"
        verbose_name_plural = "Типы ОЗУ"


class StorageType(models.Model):
    name = models.CharField(max_length=256, help_text="Тип накопителя")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тип накопителя"
        verbose_name_plural = "Типы накопителей"


class OperatingSystem(models.Model):
    name = models.CharField(max_length=256, help_text="Операционная система")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Операционная система"
        verbose_name_plural = "Операционные системы"


class Office(models.Model):
    name = models.CharField(max_length=256, help_text="Краткое название площадки")
    adress = models.TextField(help_text="Полный адрес нахождения площадки")
    managers = models.ManyToManyField(User, related_name='managed_offices')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Площадка"
        verbose_name_plural = "Площадки"


class EquipmentType(models.Model):
    name = models.CharField(max_length=256, help_text="Название типа оборудования")
    description = models.TextField(help_text="Описание", blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тип оборудования"
        verbose_name_plural = "Типы оборудования"

class ConsumableType(models.Model):
    name = models.CharField(max_length=256, help_text="Название типа расходника")
    description = models.TextField(help_text="Описание", blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тип расходного материала"
        verbose_name_plural = "Типы расходных материалов"

class Manufacturer(models.Model):
    name = models.CharField(max_length=256, help_text="Производитель")
    description = models.TextField(help_text="Описание", blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
    
class ModelName(models.Model):
    name = models.CharField(max_length=256, help_text="Модель")
    description = models.TextField(help_text="Описание", blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Модель"
        verbose_name_plural = "Модели"


class EquipmentStatus(models.Model):
    name = models.CharField(max_length=256, help_text="Статус оборудования")
    description = models.TextField(help_text="Описание", blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Статус оборудования"
        verbose_name_plural = "Статусы оборудования"
     

class Equipment(models.Model):
    name = models.CharField(max_length=256, help_text="Название оборудования", verbose_name="Название оборудования")
    accounting_name = models.TextField(help_text="Наименование по бухгалтерии", verbose_name="Наименование по бухгалтерии")
    serial_number = models.CharField(max_length=256, help_text="Серийный или заводской номер", verbose_name="Серийный номер")
    inventory_number = models.CharField(max_length=256, help_text="Инвентарный номер", verbose_name="Инвентарный номер")
    equipment_type = models.ForeignKey('EquipmentType', on_delete=models.PROTECT, help_text="Выберите тип оборудования", verbose_name="Тип оборудования")
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.PROTECT, help_text="Выберите производителя", verbose_name="Производитель оборудования", blank=True, null=True)
    model = models.ForeignKey('ModelName', on_delete=models.PROTECT, help_text="Выберите модель", verbose_name="Модель оборудования", blank=True, null=True)
    office = models.ForeignKey('Office', on_delete=models.PROTECT, help_text="Выберите площадку размещения оборудования", verbose_name="Площадка")
    room = models.CharField(max_length=256, help_text="В каком помещении находится оборудование", verbose_name="Помещение", blank=True)
    status = models.ForeignKey('EquipmentStatus', on_delete=models.PROTECT, help_text="Выберите статус оборудования", verbose_name="Статус")
    memory_type = models.ForeignKey('MemoryType', on_delete=models.PROTECT, help_text="Выберите тип ОЗУ", verbose_name="Тип ОЗУ", blank=True, null=True)
    memory_size = models.PositiveIntegerField(default=0, verbose_name="Объем ОЗУ")
    storage_type = models.ForeignKey('StorageType', on_delete=models.PROTECT, help_text="Выберите тип накопителя", verbose_name="Тип накопителя", blank=True, null=True)
    storage_size = models.PositiveIntegerField(default=0, verbose_name="Объем накопителя")
    operating_system = models.ForeignKey('OperatingSystem', on_delete=models.PROTECT, help_text="Выберите тип ОС", verbose_name="Тип ОС", blank=True, null=True)
    in_work_date = models.DateField(help_text="Дата ввода в эксплуатацию", blank=True, verbose_name="Дата ввода в эксплуатацию", default=date(1987,8,11))
    warranty_date = models.DateField(help_text="Дата окончания гарантии", blank=True, verbose_name="Дата окончания гарантии", default=date(1987,8,11))
    additional_equipment = models.TextField(help_text="Дополнительное оборудование в комплекте", blank=True, verbose_name="Дополнительное оборудование")
    description = models.TextField(help_text="Описание", blank=True, verbose_name="Описание")

    class Meta:
        ordering = ["name"]
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
   
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("equipment-detail", args=[str(self.id)])


class Consumable(models.Model):
    name = models.CharField(max_length=256, help_text="Название расходника", verbose_name="Название расходника")
    accounting_name = models.TextField(help_text="Наименование по бухгалтерии", verbose_name="Наименование по бухгалтерии")
    consumable_type = models.ForeignKey('ConsumableType', on_delete=models.PROTECT, help_text="Выберите тип расходника", verbose_name="Тип расходника", blank=True, null=True)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.PROTECT, help_text="Выберите производителя", verbose_name="Производитель расходника", blank=True, null=True)
    model = models.ForeignKey('ModelName', on_delete=models.PROTECT, help_text="Выберите модель", verbose_name="Модель расходника", blank=True, null=True)
    office = models.ForeignKey('Office', on_delete=models.PROTECT, help_text="Выберите площадку размещения расходника", verbose_name="Площадка")
    room = models.CharField(max_length=256, help_text="В каком помещении находится расходник", verbose_name="Помещение", blank=True)
    in_work_date = models.DateField(help_text="Дата ввода в эксплуатацию", blank=True, verbose_name="Дата ввода в эксплуатацию", default=date(1987,8,11))
    warranty_date = models.DateField(help_text="Дата окончания гарантии", blank=True, verbose_name="Дата окончания гарантии", default=date(1987,8,11))
    count = models.PositiveIntegerField(default=0, verbose_name="Количество")
    write_off_count = models.PositiveIntegerField(default=0, verbose_name="Количество списанного")
    description = models.TextField(help_text="Описание", blank=True, verbose_name="Описание",null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Расходник"
        verbose_name_plural = "Расходники"
   
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("consumable-detail", args=[str(self.id)])