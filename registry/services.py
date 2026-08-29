from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Gift

@transaction.atomic
def reserve_gift(gift_id, buyer_name, buyer_email, payment_proof_type, payment_proof_file):
    # O select_for_update trava a linha no banco até a transação acabar.
    # Se outra requisição tentar acessar, ela aguardará a liberação.
    gift = Gift.objects.select_for_update().get(id=gift_id)

    if gift.status != 'AVAILABLE':
        raise ValidationError("Este presente não está mais disponível.")

    gift.status = 'RESERVED'
    gift.buyer_name = buyer_name
    gift.buyer_email = buyer_email
    gift.payment_proof_type = payment_proof_type
    gift.payment_proof_file = payment_proof_file
    gift.save()
    
    return gift