import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Recipe, Ingredient, Rating
from .serializers import UserSerializer, RecipeSerializer
from rest_framework.response import Response



def checkIfLogedIn(request):

    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Log in first!')
    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except:
        raise jwt.ExpiredSignatureError

    return User.objects.filter(id=payload['id']).first()


def createCookie(userId):
    payload = {
            'id' : userId,
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


def isRecipeCreator(userObj, recipeObj):
    uSerializer = UserSerializer(userObj)
    user = uSerializer.data
    rSerializer = RecipeSerializer(recipeObj.first())
    recipe = rSerializer.data
    print(recipe['creator'], user['username'])
    return recipe['creator']['username'] == user['username']


def aggregate(classObj, groupByField, aggregationFunc, aggregationField):
    return classObj.objects.values(groupByField).annotate(aggregation=(aggregationFunc(aggregationField)))


def sortAndReturnN(listObj, criteria, n):
    scored_recipes = sorted(listObj, key=criteria)
    return scored_recipes[:n]

def addFieldAndCollectData(classSerializer, classObj, id, field, value):
    newData = classSerializer(classObj.objects.get(id=id)).data
    newData[field] = value
    return newData