from django.db import models
from django.core.validators import FileExtensionValidator

class Gift(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Disponível'),
        ('RESERVED', 'Reservado (Aguardando Pagamento)'),
        ('PURCHASED', 'Comprado'),
    ]

    CATEGORY_CHOICES = [
        ('CASA', 'Casa'),
        ('CRIATIVO', 'Criativo'),
    ]

    PAYMENT_PROOF_CHOICES = [
        ('PIX', 'Comprovante Pix'),
        ('PURCHASE', 'Comprovante de Compra'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    link2 = models.CharField(max_length=500, blank=True, null=True)
    link3 = models.CharField(max_length=500, blank=True, null=True)
    link4 = models.CharField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(
        upload_to='gifts/images/', 
        blank=True, 
        null=True, 
        help_text="Faça o upload da imagem do presente"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    buyer_name = models.CharField(max_length=255, blank=True, null=True)
    buyer_email = models.EmailField(blank=True, null=True)
    payment_proof_type = models.CharField(max_length=20, choices=PAYMENT_PROOF_CHOICES, blank=True, null=True)
    payment_proof_file = models.FileField(
        upload_to='gift_proofs/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'webp'])],
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
