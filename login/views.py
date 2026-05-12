from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import LoginService

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Debe enviar email y password"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            resultado = LoginService.autenticar_y_generar_token(email, password)
            return Response(resultado, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except RuntimeError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)