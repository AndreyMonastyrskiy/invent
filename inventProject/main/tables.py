import django_tables2 as tables
from django.utils.html import format_html
from django.urls import reverse
from .models import Equipment

class EquipmentTable(tables.Table):
    # Добавляем колонку с действиями (редактировать, удалить)
    actions = tables.Column(empty_values=(), orderable=False, verbose_name='Действия')

    class Meta:
        model = Equipment
        template_name = "django_tables2/bootstrap4.html" # Используйте подходящий шаблон
        fields = ('name', 'accounting_name', 'serial_number', 'inventory_number', 'equipment_type', 'office', 'status', 'description') # Поля для отображения
        attrs = {"class": "table table-striped table-bordered"} # Стили Bootstrap

    def render_actions(self, record):
        # Создаем ссылки для редактирования и удаления
        edit_url = reverse('main:equipment_update', args=[record.pk])
        delete_url = reverse('main:equipment_delete', args=[record.pk])
        return format_html(
            '<a href="{}"><button type="button" class="btn btn-sm btn-primary" aria-label="Редактировать"><i class="bi bi-pencil"></i></button></a>'
            '<a href="{}"><button type="button" class="btn btn-sm btn-danger" aria-label="Удалить"><i class="bi bi-trash-fill"></i></button></a>',
            edit_url,
            delete_url
        )