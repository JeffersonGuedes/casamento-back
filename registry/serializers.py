import base64

from rest_framework import serializers
from .models import Gift

class GiftSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Gift
        fields = [
            'id', 
            'name', 
            'description', 
            'link',
            'category', 
            'price', 
            'image',
            'status', 
            'buyer_name',
            'buyer_email',
            'payment_proof_type',
            'payment_proof_file',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'status',
            'buyer_name',
            'buyer_email',
            'payment_proof_type',
            'payment_proof_file',
            ]            


class ReserveGiftSerializer(serializers.Serializer):
    buyer_name = serializers.CharField(max_length=255)
    buyer_email = serializers.EmailField()
    payment_proof_type = serializers.ChoiceField(choices=Gift.PAYMENT_PROOF_CHOICES)
    payment_proof_file = serializers.FileField()

    def validate_payment_proof_file(self, value):
        allowed_content_types = {'application/pdf'}
        content_type = getattr(value, 'content_type', '')

        if content_type and (content_type in allowed_content_types or content_type.startswith('image/')):
            return value

        raise serializers.ValidationError('Envie um arquivo PDF ou imagem para o comprovante.')
