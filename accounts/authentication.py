from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.core.cache import cache
from rest_framework import serializers
from rest_framework import status

UserModel = get_user_model()

class BlockedUser(Exception):
    pass

class CustomAuthentication(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        cache_key = f"login_attempt:{username}"
        count = cache.get(cache_key, 0)
        
        if count >= 3:
            raise serializers.ValidationError(detail={"message":"Sorry,We prevent you to login since you used all attempts. Try After 30 minutes"})

        user = UserModel.objects.filter(username=username).first()
        if user and user.check_password(password):
            print(user)
            cache.delete(cache_key)
            return user

        cache.set(cache_key, count + 1, timeout=30*60)  # Cache login attempt for 30 minutes
        return None
