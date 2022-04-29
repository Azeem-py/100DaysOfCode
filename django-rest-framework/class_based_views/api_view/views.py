from re import S
from django.shortcuts import render

#APIView is the kinda class-based view we going to use here
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from knox.auth import AuthToken
from api_view import serializers


from api_view.serializers import SignUpSerializer


#DEF caching
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers



# Create your views here.


class Login(APIView):
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            _, token = AuthToken.objects.create(user)
            return Response(
                {
                    'user': str(user), 'token': str(token), '_': str(_),
                }
            )
        else: return Response(status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def Login(request):
#     serializer = AuthTokenSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     else: return Response(status=status.HTTP_400_BAD_REQUEST)

class UserList(APIView):
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization",))
    def get(self, request, format=None):
        content = {
            'user_feed': request.user.get_user_feed()
        }
        return Response(content)

    def post(self, request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
            )
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)