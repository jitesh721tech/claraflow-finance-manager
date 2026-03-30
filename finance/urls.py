from . import views
from django.urls import path
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-income/', views.add_income, name='add_income'),
    path('add-expense/', views.add_expense, name='add_expense'),

    path('edit-income/<int:pk>/', views.edit_income, name='edit_income'),
    path('delete-income/<int:pk>/', views.delete_income, name='delete_income'),
    path('edit-expense/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete-expense/<int:pk>/', views.delete_expense, name='delete_expense'),
]
