from django.urls import path
from .views import (
    DepartmentListView, 
    DepartmentCreateView, 
    DepartmentDeleteView, 
    DepartmentEditView, 
    RoleCreateView,
    RoleListView,
    RoleEditView,
    RoleDeleteView,
)

urlpatterns = (
    (path('departments/', DepartmentListView.as_view(), name='departments')),
    (path('create-department/', DepartmentCreateView.as_view(), name='create-department')),
    (path('edit-department/<int:pk>/', DepartmentEditView.as_view(), name='edit-department')),
    (path('delete-department/<int:pk>/', DepartmentDeleteView.as_view(), name='delete-department')),
    (path('create-role/', RoleCreateView.as_view(), name='create-role')),
    (path('roles/', RoleListView.as_view(), name='roles')),
    (path('edit-role/<int:pk>/', RoleEditView.as_view(), name='edit-role')),
    (path('delete-role/<int:pk>/', RoleDeleteView.as_view(), name='delete-role')),

)