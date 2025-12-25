from django.urls import path
from . import views


urlpatterns = [
path('', views.login_view, name='login'),
path('dashboard/', views.dashboard),
path('add-medicine/', views.add_medicine),
path('medicines/', views.medicine_list),
path('edit/<int:id>/', views.edit_medicine),
path('delete/<int:id>/', views.delete_medicine),
path('sell/', views.sell_medicine),
path('sales/', views.sales),
path('logout/', views.logout_view, name='logout'),
]