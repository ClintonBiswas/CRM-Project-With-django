from django.urls import path
from leads import views

app_name = 'leads'

urlpatterns = [
    path('', views.LeadListView.as_view(), name='lead-list'),
    path('lead-create/',views.Lead_create, name='lead-create'),
    path('details/<int:pk>/', views.LeadDetailView.as_view(), name='details'),
    path('update/<int:pk>/', views.LeadUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.LeadDeleteView.as_view(), name='delete'),
    path('assign-agent/<int:pk>/', views.AssignAgentView.as_view(), name='assign-agent'),
    path('category/', views.CategoryListView.as_view(), name='category'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('category-update/<int:pk>/', views.leadCategoryUpdateView.as_view(), name='category-update'),
]