from django.urls import path, include, re_path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('aboutme', AdditionalModelViewSet)
router.register('wallet', WalletModelViewSet)
router.register('', UserModelViewSet)


urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forget/', ResetAPIView.as_view()),
    path('reset/<uuid:activation_code>/', NewPassAPIView.as_view()),
    path('home/', Home.as_view(), name='home'),
    path('', include(router.urls)),

]