from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('bio', BioModelViewSet)
router.register('', UserModelViewSet)


def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('github/', home),
    path('forget/', ResetAPIView.as_view()),
    path('reset/<uuid:activation_code>/', NewPassAPIView.as_view()),
    path('', include(router.urls)),

]