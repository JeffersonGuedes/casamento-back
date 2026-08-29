from rest_framework import generics, status
from rest_framework.response import Response
from django.conf import settings
import requests

from .models import Guest
from .serializers import GuestSerializer

class GuestCreateView(generics.CreateAPIView):
    """
    Endpoint para o Next.js enviar o formulário de confirmação.
    Método permitido: POST
    """
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def create(self, request, *args, **kwargs):
        turnstile_token = request.data.get('turnstile_token')
        
        if not turnstile_token:
            return Response({"erro": "Validação de segurança ausente."}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica com o Cloudflare se é humano
        verify_url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
        cloudflare_response = requests.post(verify_url, data={
            'secret': settings.TURNSTILE_SECRET_KEY,
            'response': turnstile_token,
        }).json()

        if not cloudflare_response.get('success'):
            return Response({"erro": "Falha na verificação de robô."}, status=status.HTTP_400_BAD_REQUEST)

        # Se passou na verificação, continua o processo normal do Django de salvar o dado
        return super().create(request, *args, **kwargs)