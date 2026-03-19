from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from .models import Equipment, Consumable
from .tables import EquipmentTable, ConsumableTable
from .filters import EquipmentFilter, ConsumableFilter
from .forms import EquipmentForm, ConsumableForm
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.views import generic
from .models import Office, EquipmentType, EquipmentStatus, Equipment, Consumable
from constance import config

# Create your views here.
"""
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
"""

# Основное представление со списком оборудования (таблица + фильтры)
class EquipmentListView(LoginRequiredMixin, FilterView, SingleTableView):
    model = Equipment
    table_class = EquipmentTable
    filterset_class = EquipmentFilter
    template_name = 'main/equipment_list.html'
    #paginate_by = config.LINES_COUNT_PER_PAGE # Пагинация

    # Пагинация
    def get_paginate_by(self, queryset):
        return config.LINES_COUNT_PER_PAGE

    def get_queryset(self):
        # Получаем отфильтрованный queryset
        user_offices = self.request.user.managed_offices.all()
        qs = super().get_queryset().filter(office__in=user_offices).distinct()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем фильтр в контекст
        context['filter'] = self.filterset
        return context

# Представления для CRUD-операций
class EquipmentCreateView(LoginRequiredMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'main/equipment_form.html'
    success_url = reverse_lazy('main:equipment_list') # Имя URL для списка оборудования

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['office'].queryset = user.managed_offices.all()
        return form

    def form_valid(self, form):
        user = self.request.user
        selected_office = form.cleaned_data['office']
        if user not in selected_office.managers.all():
            form.add_error('office', 'У вас нет прав для добавления техники в этот офис.')
            return self.form_invalid(form)
        return super().form_valid(form)

class EquipmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'main/equipment_form.html'
    success_url = reverse_lazy('main:equipment_list')

    def get_queryset(self):
        user = self.request.user
        return Equipment.objects.filter(office__managers=user).distinct()

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['office'].queryset = user.managed_offices.all()
        return form

class EquipmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipment
    template_name = 'main/equipment_confirm_delete.html'
    success_url = reverse_lazy('main:equipment_list')

    def get_queryset(self):
        user = self.request.user
        return Equipment.objects.filter(office__managers=user).distinct()
    

# Представления для рассходников
class ConsumableListView(LoginRequiredMixin, FilterView, SingleTableView):
    model = Consumable
    table_class = ConsumableTable
    filterset_class = ConsumableFilter
    template_name = 'main/consumable_list.html'
    #paginate_by = config.LINES_COUNT_PER_PAGE # Пагинация

    # Пагинация
    def get_paginate_by(self, queryset):
        return config.LINES_COUNT_PER_PAGE

    def get_queryset(self):
        # Получаем отфильтрованный queryset
        user_offices = self.request.user.managed_offices.all()
        qs = super().get_queryset().filter(office__in=user_offices).distinct()
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        return self.filterset.qs
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем фильтр в контекст
        context['filter'] = self.filterset
        return context

# Представления для CRUD-операций
class ConsumableCreateView(LoginRequiredMixin, CreateView):
    model = Consumable
    form_class = ConsumableForm
    template_name = 'main/consumable_form.html'
    success_url = reverse_lazy('main:consumable_list') # Имя URL для списка оборудования

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['office'].queryset = user.managed_offices.all()
        return form

    def form_valid(self, form):
        user = self.request.user
        selected_office = form.cleaned_data['office']
        if user not in selected_office.managers.all():
            form.add_error('office', 'У вас нет прав для добавления расходника в этот офис.')
            return self.form_invalid(form)
        return super().form_valid(form)

class ConsumableUpdateView(LoginRequiredMixin, UpdateView):
    model = Consumable
    form_class = ConsumableForm
    template_name = 'main/consumable_form.html'
    success_url = reverse_lazy('main:consumable_list')

    def get_queryset(self):
        user = self.request.user
        return Consumable.objects.filter(office__managers=user).distinct()

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['office'].queryset = user.managed_offices.all()
        return form

class ConsumableDeleteView(LoginRequiredMixin, DeleteView):
    model = Consumable
    template_name = 'main/consumable_confirm_delete.html'
    success_url = reverse_lazy('main:consumable_list')

    def get_queryset(self):
        user = self.request.user
        return Consumable.objects.filter(office__managers=user).distinct()