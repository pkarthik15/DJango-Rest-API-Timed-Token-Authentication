
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.serializers import *
from account.authentication import token_expire_handler, expires_in

class Users(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        model = User.objects.all()
        user_serializer = UserSerializer(model, many=True)
        return Response(user_serializer.data, status.HTTP_200_OK)

    def post(self, request):
        user_serializer = UserSerializer(data=request.data, many=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status.HTTP_400_BAD_REQUEST)
    
class Userr(APIView):

    permission_classes = [IsAuthenticated]

    def get_not_found_error_message(self,user_id):
         message = {
                "message" : [
                    "User not found with id {}".format(user_id)
                ]
         }
         return message

    def get_user(self, user_id):
        try:
            model = User.objects.get(id = user_id)
            return model
        except User.DoesNotExist:
            return None

    def get(self, request, user_id):
        model = self.get_user(user_id)
        if model:       
            user_serializer = UserSerializer(model)
            return Response(user_serializer.data, status.HTTP_200_OK)
        else:
            return Response(self.get_not_found_error_message(user_id), status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        model = self.get_user(user_id)
        if model:       
            user_serializer = UserSerializer(model, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status.HTTP_200_OK)
            return Response(user_serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(self.get_not_found_error_message(user_id), status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        model = self.get_user(user_id)
        if model:
            model.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        else:
            return Response(self.get_not_found_error_message(user_id), status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_all_users(request):
#     model = User.objects.all()
#     user_serializer = UserSerializer(model, many=True)
#     return Response(user_serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
    login_serializer = LoginSerializer(data = request.data)
    if not login_serializer.is_valid():
        return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username = login_serializer.data['username'],password = login_serializer.data['password'])

    if not user:
        return Response({'detail': 'Invalid Credentials or activate account'}, status=status.HTTP_404_NOT_FOUND)
    
    token, _ = Token.objects.get_or_create(user = user)

    is_expired, token = token_expire_handler(token)
    
    authuserserializer = AuthUserSerializer(user)

    response = {
        'user' : authuserserializer.data,
        'expires_in' : expires_in(token),
        'token' : token.key
    }

    return Response(response, status=status.HTTP_200_OK)

        
    