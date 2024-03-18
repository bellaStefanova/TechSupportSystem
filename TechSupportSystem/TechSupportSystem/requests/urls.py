from django.urls import path
from .views import CreateRequestView, DeleteRequestView, DetailsRequestView, TakeRequestView

urlpatterns = (
    (path('create-request/', CreateRequestView.as_view(), name='create-request')),
    (path('delete-request/<int:pk>/', DeleteRequestView.as_view(), name='delete-request')),
    (path('view-request/<int:pk>/', DetailsRequestView.as_view(), name='view-request')),
    (path('take-request/<int:request_id>/', TakeRequestView.as_view(), name='take-request')),
    # (path('signin/', SignInView.as_view(), name='signin')),
    # (path('signout/', SignOutView.as_view(), name='signout')),
    # (path('home', UserHomeView.as_view(), name='user-home')),
)