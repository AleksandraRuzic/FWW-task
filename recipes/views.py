from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Hello there</h1>')

class signUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class logInView(APIView):
    def post(self, request):
        username = request.data['username']
        pswd = request.data['password']
        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('No user with given username!')

        if not user.check_password(pswd):
            raise AuthenticationFailed('Wrong password!')

        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        res = Response()
        res.set_cookie(key='jwt', value=token, httponly=True)
        res.data = {
            'jwt' : token
        }

        return res


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

###############################################################################################################################

class userRecipesView(APIView):
    def get(self, request):
        pass

class makeRecipeView(APIView):
    def post(self, request):
        pass

class editRecipeView(APIView):
    def post(self, request):
        pass
    

class scoreRecipeView(APIView):
    def post(self, request):
        pass

class editScoreView(APIView):
    def post(self, request):
        pass