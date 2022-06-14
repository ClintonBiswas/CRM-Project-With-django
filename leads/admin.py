from django.contrib import admin
from leads.models import Agent, Lead, UserProfile, User, Category
# Register your models here.
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'first_name', 'last_name', 'age')
admin.site.register(Agent)
admin.site.register(UserProfile)
admin.site.register(User)
admin.site.register(Category)

