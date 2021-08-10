from django.contrib import admin

from .models import *

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'created_at')
    list_display_links = ('user', 'image')
    list_filter = ('user', 'created_at')
    search_fields = ('user',)
    list_per_page = 10

@admin.register(SubscriptionType)
class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('title','created_at')
    list_display_links = ('title',)
    list_filter = ('title', 'created_at')
    search_fields = ('title',)
    list_per_page = 10

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date', 'created_at')
    list_display_links = ('user', 'title', )
    list_filter = ('user', 'created_at')
    search_fields = ('user', 'title')
    list_per_page = 10

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subscription_type', 'day_limit', 'price', 'created_at')
    list_display_links = ('title', )
    list_filter = ('created_at',)
    search_fields = ('title',)
    list_per_page = 10

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_id', 'created_at')
    list_display_links = ('user', 'subscription_id', )
    list_filter = ('user', 'created_at')
    search_fields = ('user', 'subscription_id')
    list_per_page = 10