from django.urls import path
from .views import (
    ListUsersView,
    EditUserView,
    DeleteUserView,
    ListRequestsView
)


urlpatterns = (
    (path('requests/', ListRequestsView.as_view(), name='requests')),
    (path('users/', ListUsersView.as_view(), name='users')),
    (path('edit-user/<int:pk>', EditUserView.as_view(), name='edit-user')),
    (path('delete-user/<int:pk>', DeleteUserView.as_view(), name='delete-user')),
)