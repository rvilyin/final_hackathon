from rest_framework import serializers
from django.contrib.auth import get_user_model
from .send_email import send_activation_code, send_reset_code
from django.contrib.auth.hashers import make_password
from .models import *

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        required=True,
        min_length=6,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')


    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password2')
        if p1 != p2:
            raise serializers.ValidationError('Password did not match!')
        
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code(user.email, user.activation_code)

        return user
    


class ResetSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

    def validate(self, attrs):
        user = attrs.get('username')
        if User.objects.filter(username=user).exists():
            return attrs
        raise serializers.ValidationError('Пользователь не найден')
    
    def create(self, validated_data):
        user = User.objects.get(username=validated_data['username'])
        user.create_activation_code()
        user.save()
        send_reset_code(user.email, user.activation_code)

        return user
    

class NewPassSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True,
        min_length=6,
        write_only=True
    )
    password2 = serializers.CharField(
        required=True,
        min_length=6,
        write_only=True
    )

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password2')
        if p1 != p2:
            raise serializers.ValidationError('Password did not match!')
        user = self.context
        user.password = make_password(p1)
        user.activation_code = ''
        user.save()
        return attrs

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = ('avatar',)


class UserSerializer(serializers.ModelSerializer):
    additional = AvatarSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'additional')
        # fields = '__all__'
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['avatar'] = instance.additional.avatar

    #     return representation

class Follow1Serializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='following.username')
    class Meta:
        model = Follow
        fields = ('user',)

class Follow2Serializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Follow
        fields = ('user',)

class U2(serializers.ModelSerializer):
    following = Follow1Serializer(many=True, read_only=True)
    followers = Follow2Serializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('following', 'followers')


class AdditionalSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = AdditionalInfo
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # serializer = FollowSerializer
        # representation['following'] = instance.user.followers.filter(is_follow=True).count()
        serializer = U2(instance.user)
        representation.update(serializer.data)

        return representation
        # serializer = FollowSerializer(instance.user.followers)

        # return serializer.data


class WalletSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.usernmae')
    class Meta:
        model = Wallet
        fields = '__all__'
