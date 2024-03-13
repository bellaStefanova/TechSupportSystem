from django.urls import path
from .views import SignupView, SignInView, SignOutView, UserHomeView, ProfileDetailsView

urlpatterns = (
    (path('signup/', SignupView.as_view(), name='signup')),
    (path('signin/', SignInView.as_view(), name='signin')),
    (path('signout/', SignOutView.as_view(), name='signout')),
    (path('home', UserHomeView.as_view(), name='user-home')),
    (path('profile/', ProfileDetailsView.as_view(), name='profile-details')),
)