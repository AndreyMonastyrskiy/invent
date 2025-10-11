import django_tables2 as tables
from django.utils.html import format_html
from django.urls import reverse
from .models import Equipment

class EquipmentTable(tables.Table):
    # Добавляем колонку с чекбоксами для выбора записей (опционально)
    selection = tables.CheckBoxColumn(accessor='pk', attrs={"th__input": {"onclick": "toggle(this)"}}, orderable=False)
    # Добавляем колонку с действиями (редактировать, удалить)
    actions = tables.Column(empty_values=(), orderable=False, verbose_name='Действия')

    class Meta:
        model = Equipment
        template_name = "django_tables2/bootstrap4.html" # Используйте подходящий шаблон
        fields = ('name', 'accounting_name', 'serial_number', 'inventory_number', 'equipment_type', 'office', 'status') # Поля для отображения
        attrs = {"class": "table table-striped table-bordered"} # Стили Bootstrap

    def render_actions(self, record):
        # Создаем ссылки для редактирования и удаления
        edit_url = reverse('main:equipment_update', args=[record.pk])
        delete_url = reverse('main:equipment_delete', args=[record.pk])
        return format_html(
            '<a class="btn btn-sm btn-warning" href="{}">✏️</a> '
            '<a class="btn btn-sm btn-danger" href="{}">❌</a>',
            edit_url,
            delete_url
        )