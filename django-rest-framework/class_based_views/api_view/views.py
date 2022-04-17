from re import S
from django.shortcuts import render

#APIView is the kinda class-based view we going to use here
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User

from api_view.serializers import SignUpSerializer

# Create your views here.

class UserList(APIView):
    def get(self, request, format=None):
        user = User.objects.all()
        serializer = SignUpSerializer(user)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
            )
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)