from django.urls import path
from .views import DepartmentListView, DepartmentCreateView, DepartmentDeleteView, DepartmentEditView

urlpatterns = (
    (path('departments/', DepartmentListView.as_view(), name='departments')),
    (path('create-department/', DepartmentCreateView.as_view(), name='create-department')),
    (path('edit-department/<int:pk>/', DepartmentEditView.as_view(), name='edit-department')),
    (path('delete-department/<int:pk>/', DepartmentDeleteView.as_view(), name='delete-department')),

)