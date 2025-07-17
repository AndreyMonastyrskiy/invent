from django.db import models
from django.urls import reverse


class Office(models.Model):
    name = models.CharField(max_length=256, help_text="Краткое название площадки")
    adress = models.TextField(help_text="Полный адрес нахождения площадки")

    def __str__(self):
        return self.name


class EquipmentType(models.Model):
    name = models.CharField(max_length=256, help_text="Название типа оборудования")
    description = models.TextField(help_text="Описание", blank=True)

    def __str__(self):
        return self.name


class EquipmentStatus(models.Model):
    name = models.CharField(max_length=256, help_text="Статус оборудования")
    description = models.TextField(help_text="Описание", blank=True)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=256, help_text="Название оборудования")
    accounting_name = models.TextField(help_text="Наименование по бухгалтерии")
    serial_number = models.CharField(max_length=256, help_text="Серийный или заводской номер")
    inventory_number = models.CharField(max_length=256, help_text="Инвентарный номер")
    equipment_type = models.ForeignKey('EquipmentType', on_delete=models.PROTECT, help_text="Выберите тип оборудования")
    office = models.ForeignKey('Office', on_delete=models.PROTECT, help_text="Выберите площадку размещения оборудования")
    status = models.ForeignKey('EquipmentStatus', on_delete=models.PROTECT, help_text="Выберите статус оборудования")
    description = models.TextField(help_text="Описание", blank=True)

    class Meta:
        ordering = ["name"]
   
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("equipment-detail", args=[str(self.id)])
    