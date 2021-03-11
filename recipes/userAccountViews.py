from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
from .helperFunctions import createCookie
import jwt, datetime

class signUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return createCookie(serializer.data['id'])


class logInView(APIView):
    def post(self, request):
        username = request.data['username']
        pswd = request.data['password']
        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('No user with given username!')

        #if not user.check_password(pswd):
        #    raise AuthenticationFailed('Wrong password!')

        return createCookie(user.id)


class logOutView(APIView):
    def post(self, request):
        res = Response()
        res.delete_cookie('jwt')
        res.data = {
            'msg' : 'Succussesfully loged out'
        }

        return res

class userView(APIView):
    def get(self, request):
        
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Log in first!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except:
            raise jwt.ExpiredSignatureError

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        print(serializer.data)

        return Response(serializer.data)