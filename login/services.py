import httpx
import jwt
import os
from datetime import datetime, timedelta

class LoginService:
    @staticmethod
    def autenticar_y_generar_token(email, password):
        # 1. Ir a golpear la puerta de MS-Usuario
        ms_usuario_url = os.environ.get('MS_USUARIO_URL', 'http://127.0.0.1:8001')
        url_validacion = f"{ms_usuario_url}/api/usuario/validar-credenciales/"

        try:
            # Mandamos la solicitud al puerto 8001
            response = httpx.post(url_validacion, json={"email": email, "password": password})
        except Exception:
            raise RuntimeError("Error de comunicación interna con MS-Usuario")

        if response.status_code == 401:
            raise ValueError("Credenciales incorrectas")
        elif response.status_code != 200:
            raise RuntimeError("Error interno verificando credenciales")

        datos_usuario = response.json()

        # 2. Fabricar el JWT
        secret_key = os.environ.get('JWT_SECRET_KEY', 'default_secret')
        algorithm = os.environ.get('JWT_ALGORITHM', 'HS256')

        payload = {
            "rut": datos_usuario["rut_empresa"],
            "email": datos_usuario["email"],
            "rol": datos_usuario["rol"],
            "nombre": datos_usuario["nombre"],
            # Expira en 4 horas (muy estándar para sistemas de gestión)
            "exp": datetime.utcnow() + timedelta(hours=4), 
            "iat": datetime.utcnow() # Emitido en este instante
        }

        # Firmamos el token
        token = jwt.encode(payload, secret_key, algorithm=algorithm)

        return {
            "access_token": token,
            "token_type": "Bearer",
            "usuario": datos_usuario
        }