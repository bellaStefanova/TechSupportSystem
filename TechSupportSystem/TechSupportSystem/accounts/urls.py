from django.urls import path
from .views import (
    SignupView, 
    SignInView, 
    SignOutView, 
    UserHomeView, 
    ProfileDetailsView, 
    NextToFirstLoginView, 
    ProfileEditView,
    ChangePasswordView,
    # logout_view
)


urlpatterns = (
    (path('signup/', SignupView.as_view(), name='signup')),
    (path('signin/', SignInView.as_view(), name='signin')),
    (path('signout/', SignOutView.as_view(), name='signout')),
    # (path('signout/', logout_view, name='signout')),
    (path('home', UserHomeView.as_view(), name='user-home')),
    (path('profile/', ProfileDetailsView.as_view(), name='profile-details')),
    (path('add-profile-details', NextToFirstLoginView.as_view(), name='add-profile-details')),
    (path('edit-profile', ProfileEditView.as_view(), name='edit-profile')),
    (path('change-password', ChangePasswordView.as_view(), name='change-password')),
)