from django.urls import path
from . import views

app_name = 'skill_gap'

urlpatterns = [
    path('', views.home, name='home'),
    path('analyze/', views.analyze, name='analyze'),
    path('roles/', views.roles_list, name='roles_list'),
    path('roles/<int:pk>/', views.role_detail, name='role_detail'),
    path('profiles/', views.profiles_list, name='profiles_list'),
    path('profiles/create/', views.profile_create, name='profile_create'),
    path('profiles/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('skills/', views.skills_list, name='skills_list'),
]
