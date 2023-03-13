from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *

class RegisterAPIView(APIView):
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
    def post(self, request):
        serializer = ResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Вам на почту отправлено письмо с ссылкой для сброса пароля', status=200)
    
class NewPassAPIView(APIView):
    def post(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
        except User.DoesNotExist:
            return Response({'msg': 'Отказано!'}, status=400)
        serializer = NewPassSerializer(data=request.data, context=user)
        serializer.is_valid(raise_exception=True)
            
        return Response({'msg': 'Успешно!'}, status=200)

        