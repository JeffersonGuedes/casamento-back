from rest_framework import generics, status, filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.conf import settings
import requests

# Importações necessárias para o cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Gift
from .serializers import GiftSerializer, ReserveGiftSerializer
from .services import reserve_gift

class GiftListCreateView(generics.ListCreateAPIView):
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price']
    ordering = ['price']

    @method_decorator(cache_page(60)) 
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ReserveGiftView(APIView):
    """
    POST: Trava o item no banco (Pessimistic Locking) e reserva para o comprador.
    """
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, gift_id):
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

        # O código segue normalmente se for humano
        serializer = ReserveGiftSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            gift = reserve_gift(
                gift_id=gift_id,
                buyer_name=serializer.validated_data['buyer_name'],
                buyer_email=serializer.validated_data['buyer_email'],
                payment_proof_type=serializer.validated_data['payment_proof_type'],
                payment_proof_file=serializer.validated_data['payment_proof_file'],
            )
            response_serializer = GiftSerializer(gift)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e.message)}, status=status.HTTP_409_CONFLICT)
        except Gift.DoesNotExist:
            return Response({"error": "Presente não encontrado."}, status=status.HTTP_404_NOT_FOUND)