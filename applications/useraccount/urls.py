from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('forget/', ResetAPIView.as_view()),
    path('reset/<uuid:activation_code>/', NewPassAPIView.as_view()),
    path('', home)
]