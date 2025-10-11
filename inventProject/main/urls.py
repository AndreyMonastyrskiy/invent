from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.EquipmentListView.as_view(), name='equipment_list'),
    path('create/', views.EquipmentCreateView.as_view(), name='equipment_create'),
    path('<int:pk>/update/', views.EquipmentUpdateView.as_view(), name='equipment_update'),
    path('<int:pk>/delete/', views.EquipmentDeleteView.as_view(), name='equipment_delete'),
    #path('',views.index, name='index'),
    #path('equipments/', views.equipment_list, name='equipments_list'),
    #path('equipments/<int:id>', views.equipment_detail, name='equipment_detail'),
    ##path('equipments/<int:id>', views.EquipmentDetailView.as_view(), name='equipments_detail'),
    ##path('equipments/', views.EquipmentListView.as_view(), name='equipments'),
    ##path('equipment/<int:pk>/', views.EquipmentDetailView.as_view(), name='equipment-detail'),
]
