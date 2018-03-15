from django.urls import path
from .import views

app_name = 'app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('csv_import/', views.csv_import, name='csv_import'),
    path('csv_export/', views.csv_export, name='csv_export'),

]



