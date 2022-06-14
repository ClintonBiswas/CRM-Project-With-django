from django.urls import path
from agents import views

app_name = 'agents'

urlpatterns = [
    path('', views.AgentListView.as_view(), name='agent-list'),
    path('agent-create/', views.AgentCreateView.as_view(), name='agent-create'),
    path('agent-detail/<int:pk>/', views.AgentDetailsView.as_view(), name='agent-detail'),
    path('agent-update/<int:pk>/', views.AgentUpdateView.as_view(), name='agent-update'),
    path('agent-delete/<int:pk>/', views.AgentDeleteView.as_view(), name='agent-delete'),
]