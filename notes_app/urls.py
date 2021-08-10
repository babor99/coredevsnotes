from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.conf.urls.static import static

from . import views

# Routes for api goes here..
router = routers.DefaultRouter()
router.register("profile", views.ProfileViewSet, basename="profile")
router.register("notes", views.NotesViewSet, basename="notes")
router.register("subscriptions", views.SubscriptionsViewSet, basename="subscriptions")
router.register("user_subscriptions", views.UserSubscriptionsViewSet, basename="user_subscriptions")
router.register("user_signup", views.SignupViewSet, basename="user_signup")

router.register("notes_for_calendar", views.NotesFullCalendarViewSet, basename="notes_for_calendar")

router.register("subscription_types", views.SubscriptionTypeViewSet, basename="subscription_types")



urlpatterns = [
    path('notes_app/', include(router.urls)),
    # path('notes_app/user_signup/', views.user_signup, name='user_signup'),
]

