from rest_framework import generics, status, views, permissions
from .serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from .utils import Util
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect
import os, random, string


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RegisterView(generics.GenericAPIView):
    """ Registro para novo usuários que desejam utilizar a API """
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):

        user = request.data
        chars = string.ascii_letters + string.digits + '!@#$%^&*'
        rnd = random.SystemRandom()
        senha = ''.join(rnd.choice(chars) for i in range(8))
        user['password'] = senha

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        token = str(token)
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token=" + token

        email_body = 'Olá ' + user.username + \
                     ',\n Seja bem vindo(a) a API de Informações do Comércio Exterior do Brasil \n' + \
                     ',\n Seu login de acesso é: ' + user.email + \
                     '\n Sua senha é: ' + senha +\
                     '\n\n Use o link abaixo para verificar seu e-mail \n\n' + absurl + \
                     '\n\n atenciosamente,' + \
                     '\n\n Diogo Santos' + \
                     '\n Desenvolvedor da API do Sistema Comex Stat'
        data = {'email_body': email_body, 'to_email': [user.email],
                'email_subject': 'Ative seu cadastro na API Comex Stat'}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    """ classe utlizada para veficar e ativar a conta do usuário """
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        token = token.strip()
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email': 'Ativado com sucesso'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Ativação expirada'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Token Inválido'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    """ classe utlizada para fazer login e fornecer o token de acesso ao usuário """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    """ classe para recuperação de senha do usuário """
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://' + current_site + relativeLink
            email_body = 'Olá, \n\n Use o link abaixo para redefinir sua senha  \n' + \
                         absurl + "?redirect_url=" + redirect_url

            data = {'email_body': email_body, 'to_email': [user.email],
                    'email_subject': 'Redefinição de senha - API Comex Stat'}
            Util.send_email(data)
        return Response({'success': 'Enviamos um link para redefinir sua senha'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    """ classe utilizada para chegar o token """
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):

                if len(redirect_url) > 3:

                    return CustomRedirect(redirect_url + '?token_valid=False')
                else:

                    return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

            if redirect_url and len(redirect_url) > 3:

                return CustomRedirect(
                    redirect_url + '/' + uidb64 + '/' + token)
                #return CustomRedirect(
                    #redirect_url + '?token_valid=True&message=Credentials Valid&uidb64=' + uidb64 + '&token=' + token)
            else:

                return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:

                if not PasswordResetTokenGenerator().check_token(user):

                    return CustomRedirect(redirect_url + '?token_valid=False')

            except UnboundLocalError as e:

                return Response({'error': 'O token não é válido, solicite um novo'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    """ Classe utlizada pora cadastrar nova senha """
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Senha redefinida com Sucesso'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    """ classe utilizada para logout e invalidação do token """
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPI(generics.RetrieveAPIView):
    """ classe para receber dados do atual usuário logado """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordAPIView(generics.GenericAPIView):
    """ classe para mudança de senha do usuário """
    serializer_class = ChancePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)