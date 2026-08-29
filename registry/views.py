from rest_framework import generics, status, filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

# Importações necessárias para o cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Gift
from .serializers import GiftSerializer, ReserveGiftSerializer
from .services import reserve_gift

class GiftListCreateView(generics.ListCreateAPIView):
    """
    GET: Lista todos os presentes (com suporte a ordenação por preço).
    POST: Cria um novo presente usando o GiftSerializer.
    """
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price']
    ordering = ['price']

    # Adicionando cache de 60 segundos apenas na requisição GET (Listagem)
    @method_decorator(cache_page(60)) 
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ReserveGiftView(APIView):
    """
    POST: Trava o item no banco (Pessimistic Locking) e reserva para o comprador.
    """
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, gift_id):
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
