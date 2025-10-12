from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from .models import Equipment
from .tables import EquipmentTable
from .filters import EquipmentFilter
from .forms import EquipmentForm
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Office, EquipmentType, EquipmentStatus, Equipment

# Create your views here.
def index(request):
    num_office = Office.objects.all().count()
    num_equipment_type = EquipmentType.objects.all().count()
    num_equipment_status = EquipmentStatus.objects.count
    equipment_used_status = EquipmentStatus.objects.get(name='Используется')
    num_equipment_in_use = Equipment.objects.filter(status=equipment_used_status).count()
    return render(request, 'index.html', context={
        'num_office':num_office,
        'num_equipment_type':num_equipment_type,
        'num_equipment_status':num_equipment_status,
        'num_equipment_in_use':num_equipment_in_use
    },)

def equipment_list(request):
    equipments = Equipment.objects.all()
    return render (
        request,
        'main/equipment_list.html',
        context={
            'equipment_list': equipments
        }
    )

def equipment_detail(request, id):
    equipment = get_object_or_404 (
        Equipment,
        id = id
    )
    return render(
        request,
        'main/equipment_detail.html',
        {'equipment': equipment}
    )

# Основное представление со списком оборудования (таблица + фильтры)
class EquipmentListView(FilterView, SingleTableView):
    model = Equipment
    table_class = EquipmentTable
    filterset_class = EquipmentFilter
    template_name = 'main/equipment_list.html'
    paginate_by = 3 # Пагинация

    def get_queryset(self):
        # Получаем отфильтрованный queryset
        qs = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем фильтр в контекст
        context['filter'] = self.filterset
        return context

# Представления для CRUD-операций
class EquipmentCreateView(CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'main/equipment_form.html'
    success_url = reverse_lazy('main:equipment_list') # Имя URL для списка оборудования

class EquipmentUpdateView(UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'main/equipment_form.html'
    success_url = reverse_lazy('main:equipment_list')

class EquipmentDeleteView(DeleteView):
    model = Equipment
    template_name = 'main/equipment_confirm_delete.html'
    success_url = reverse_lazy('main:equipment_list')