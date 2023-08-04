
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.health_check, name='health_check'),
    path('health/', views.health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('react_api/', include('react_api.urls'))
]

