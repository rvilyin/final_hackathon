from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from drf_yasg.utils import swagger_auto_schema


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
    

class UserModelViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_superuser=False)
    #     return queryset


        