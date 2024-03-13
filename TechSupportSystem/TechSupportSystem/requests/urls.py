from django.urls import path
from .views import CreateRequestView, DeleteRequestView, ListRequestView, ListNotificationView

urlpatterns = (
    (path('create-request/', CreateRequestView.as_view(), name='create-request')),
    (path('delete-request/<int:pk>/', DeleteRequestView.as_view(), name='delete-request')),
    (path('view-request/<int:pk>/', ListRequestView.as_view(), name='view-request')),
    (path('view-notifications/', ListNotificationView.as_view(), name='view-notifications')),
    # (path('signin/', SignInView.as_view(), name='signin')),
    # (path('signout/', SignOutView.as_view(), name='signout')),
    # (path('home', UserHomeView.as_view(), name='user-home')),
)