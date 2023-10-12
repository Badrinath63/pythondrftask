from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Log
from django.utils import timezone
from .serializers import UserSerializer, LogSerializer
from django.db import transaction, IntegrityError


from django.db import transaction

class CreateUserView(APIView):
    @transaction.atomic
    def post(self, request):
        user_data = request.data
        serializer = UserSerializer(data=user_data)

        if serializer.is_valid():
            try:
                user = serializer.save()

                return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'message': 'Username or email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUsersView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_active=True)


class UpdateUserView(APIView):
    def put(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        user_data = request.data
        serializer = UserSerializer(user, data=user_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User profile updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(APIView):
    def delete(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        user.is_active = False
        user.save()

        return Response({'message': 'User profile deactivated successfully'}, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if user.password == password:
                Log.objects.create(user=user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Login failed. Incorrect password.'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'message': 'Login failed. User not found.'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        username = request.data.get('username')

        try:
            user = User.objects.get(username=username)
            Log.objects.create(user=user, logout_time=timezone.now())
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'Logout failed. User not found.'}, status=status.HTTP_401_UNAUTHORIZED)

