from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOwner
import django
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100000



class RegisterAPIView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Вы Успешно зарегистрировались. Вам отправлено письмо с активацией', status=201)
    

class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            AdditionalInfo.objects.create(user=user)
            Wallet.objects.create(user=user)
            user.save()
            return Response({'msg': 'Успешно!'}, status=200)
        except User.DoesNotExist:
            return Response({'msg': 'Отказано!'}, status=400)
        

class ResetAPIView(APIView):
    @swagger_auto_schema(request_body=ResetSerializer)
    def post(self, request):
        serializer = ResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Вам на почту отправлено письмо с ссылкой для сброса пароля', status=200)
    

class NewPassAPIView(APIView):
    @swagger_auto_schema(request_body=NewPassSerializer)
    def post(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
        except User.DoesNotExist:
            return Response({'msg': 'Отказано!'}, status=400)
        serializer = NewPassSerializer(data=request.data, context=user)
        serializer.is_valid(raise_exception=True)
            
        return Response({'msg': 'Успешно!'}, status=200)
    

@method_decorator(cache_page(60 * 15), name='dispatch')
class UserModelViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username']
    ordering_fields = ['username']

    @action(methods=['POST'], detail=True)  # asiastream.space/api/v1/account/<user_id>/follow/
    def follow(self, request, pk, *args, **kwargs):
        user = request.user
        follow_obj, created = Follow.objects.get_or_create(user=user, following_id=pk)
        if created:
            status = 'following'
            follow_obj.save()
        else:
            status = 'unfollowing'
            Follow.objects.filter(user=user, following_id=pk).delete()

        return Response({'status':status})
    
    @action(methods=['POST'], detail=True)  # asiastream.space/api/v1/account/<user_id>/subscribe/
    def subscribe(self, request, pk, *args, **kwargs):
        user = request.user
        subscribe_obj, created = Subscribe.objects.get_or_create(subscriber=user, streamer_id=pk)
        if created:
            my_wallet_money = Wallet.objects.get(user=user).money
            if my_wallet_money < 100:
                status = 'insufficient funds'
                Subscribe.objects.filter(subscriber=user, streamer_id=pk).delete()
            else:
                Wallet.objects.filter(user=user).update(money=my_wallet_money-100)
                streamer_wallet_money = Wallet.objects.get(user_id=pk).money
                Wallet.objects.filter(user_id=pk).update(money=streamer_wallet_money+90)
                admin_wallet_money = Wallet.objects.get(user_id=1).money
                Wallet.objects.filter(user_id=1).update(money=admin_wallet_money+10)
                subscribe_obj.save()
                status = 'subscribed'
        else:
            status = 'already subscribed'

        return Response({'status':status})


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_superuser=False)
        return queryset

@method_decorator(cache_page(60 * 15), name='dispatch')
class AdditionalModelViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             GenericViewSet):
    queryset = AdditionalInfo.objects.all()
    serializer_class = AdditionalSerializer
    permission_classes = [IsOwner]

    # def perform_create(self, serializer):
    #     return serializer.save(user=self.request.user)
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(user=self.request.user)
    #     return queryset

class WalletModelViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         GenericViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset



class Home(TemplateView):
    template_name = 'home.html'