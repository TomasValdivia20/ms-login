from django.urls import path
from .views import LoginView

urlpatterns = [
    # Al llamar a /api/login/, entrará aquí
    path('', LoginView.as_view(), name='login'),
]