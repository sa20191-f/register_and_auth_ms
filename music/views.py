from rest_framework_jwt.settings import api_settings
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import SongsSerializer, TokenSerializer, UserSerializer, UserAltSerializer, UserTokenInfoSerializer
from .models import Songs, UserTokenInfo
import ldap

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Baseline LDAP configuration.
# ldapHost = 'ldap://192.168.99.102'
ldapHost = 'ldap://35.232.68.151'
admin_dn = "cn=admin,dc=arqsoft,dc=unal,dc=edu,dc=co"
admin_password = "admin"

class ListCreateUTIView(generics.ListCreateAPIView):
    """
    GET tokenInfo/
    POST tokenInfo/
    """
    queryset = UserTokenInfo.objects.all()
    serializer_class = UserTokenInfoSerializer
    permission_classes = (permissions.AllowAny,) 

    #decorator goes here
    def post(self, request, *args, **kwargs):
        new_instance = UserTokenInfo.objects.create(
            userID=request.data["userID"],
            tokenType=request.data["tokenType"],
            token=request.data["token"],
        )
        return Response(
            data=UserTokenInfoSerializer(new_instance).data,
            status=status.HTTP_201_CREATED
        )

class UTIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET tokenInfo/:userID/
    """
    queryset = UserTokenInfo.objects.all()
    serializer_class = UserTokenInfoSerializer

    def get(self, request, *args, **kwargs):
        new_instance = self.queryset.filter(userID=kwargs["userID"])
        result_list = list(new_instance.values("id", "tokenType", "token"))
        if not result_list:
            return Response(
            data={
                "message": "Register with id: {} does not exist".format(kwargs["userID"])
            },
            status=status.HTTP_404_NOT_FOUND
            )

        return Response(result_list)

        # json_res = []
        # for record in new_instance: 
        #     json_obj = dict(userID=record.userID.pk, tokenType=record.tokenType, token=record.token)
        #     print(json_obj)
        #     json_res.append(json_obj)
        # return Response(json_res)

class UTIDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    DELETE tokenInfo/:pk/
    """
    queryset = UserTokenInfo.objects.all()
    serializer_class = UserTokenInfoSerializer
    permission_classes = (permissions.AllowAny,) 

    def delete(self, request, *args, **kwargs):
        try:
            to_delete = self.queryset.get(pk=kwargs["pk"])
            to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserTokenInfo.DoesNotExist:
            return Response(
                data={
                    "message": "Can't delete Register with id: {}. It does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class ListSongsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ListUsersView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = User.objects.all()
    serializer_class = UserAltSerializer

class RegisterUsersView(generics.CreateAPIView):
    
    #POST api/v1/register/
    
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        
        username = request.data.get("username", "")
        email = request.data.get("email", "")
        password = request.data.get("password", "")

        serialized = UserSerializer(data=request.data)
        if not username or not password or not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if serialized.is_valid(self):
            new_user = User.objects.create_user(
                username=username, email=email, password=password
            )
            new_user.save()
            print("1:  ", UserAltSerializer(new_user).data)
            return Response(
                data=UserSerializer(new_user).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

def connection(dn, password):
    try:
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT,0)
        con = ldap.initialize(ldapHost)
        con.set_option(ldap.OPT_PROTOCOL_VERSION, 3)        
        print("Connectado al servidor LDAP...")
    except ldap.INVALID_CREDENTIALS:
        print("Credenciales incorrectas en el servidor LDAP")
        return False
    except ldap.SERVER_DOWN:
        print("LDAP server down")
        return False
    #print("line 153 ok")
    return(con)

def validate(con, dn, password):
    try:
        con.simple_bind_s(dn, password)
        return True
    except (ldap.LDAPError):
        return False

class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        dn = "cn=" + email + ",ou=academy,dc=arqsoft,dc=unal,dc=edu,dc=co"

        ldapConnection = connection(dn, password)
        if ldapConnection == False:
            return Response(data={"message":"LDAP server down"})
        userVerify = validate(ldapConnection, dn, password)
        print("Se conectó al ldap")
        if userVerify == False:
            return Response(data={"message":"Error en la autenticación en el servidor LDAP"})
        user = authenticate(request, username=username, password=password)
        print("Se verifico el usuario")
        print(str(user))
        print("El de arriba es el usuario")
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            id_serializer = user.id
            print(id_serializer)
            return Response(
                data = {
                "token": serializer.data,
                "id": request.user.id
                }, status=status.HTTP_200_OK)
        return Response(data={
            "message":"Esa combinación de usuario y password no existe en la base de datos"
        }, status=status.HTTP_401_UNAUTHORIZED)

class IdView(generics.CreateAPIView):
    queryset = User.objects.all()
    def get(self, request, *args, **kwargs):
        current_user = request.user
        return Response(
            data={
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
            }, status=status.HTTP_200_OK)

class LogoutView(generics.CreateAPIView):
    queryset = User.objects.all()
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(
            data={
                "message": "Logged out succesfully."
            }, status=status.HTTP_200_OK)

class UserView(generics.RetrieveAPIView):
    model = User
    serializer_class = UserAltSerializer
    queryset = User.objects.all()
    def get(self, request, *args, **kwargs):
        return Response(UserAltSerializer(request.user).data)