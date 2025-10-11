from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__' # Используйте все поля модели. Или укажите конкретные: fields = ['name', ...]
        # Можно кастомизировать виджеты и labels
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Название оборудования',
            # ... остальные labels
        }