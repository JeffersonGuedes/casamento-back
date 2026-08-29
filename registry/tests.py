from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Gift


class GiftListViewTests(APITestCase):
	def test_list_gifts_returns_200(self):
		Gift.objects.create(
			name='Jogo de Taças',
			description='Conjunto com 6 taças',
			link='https://example.com/gifts/jogo-de-tacas',
			category='CASA',
			price='199.90',
		)

		response = self.client.get('/api/registry/gifts/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)
		self.assertIn('image_base64', response.data[0])
		self.assertIsNone(response.data[0]['image_base64'])


class ReserveGiftViewTests(APITestCase):
	def setUp(self):
		self.gift = Gift.objects.create(
			name='Jogo de Taças',
			description='Conjunto com 6 taças',
			link='https://example.com/gifts/jogo-de-tacas',
			category='CASA',
			price='199.90',
		)

	def test_reserve_gift_requires_all_fields(self):
		url = reverse('gift-reserve', kwargs={'gift_id': self.gift.id})

		response = self.client.post(
			url,
			data={
				'buyer_name': 'Maria',
			},
			format='multipart',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('buyer_email', response.data)
		self.assertIn('payment_proof_type', response.data)
		self.assertIn('payment_proof_file', response.data)

	def test_reserve_gift_with_pdf_proof(self):
		url = reverse('gift-reserve', kwargs={'gift_id': self.gift.id})
		proof_file = SimpleUploadedFile(
			'comprovante.pdf',
			b'%PDF-1.4 fake content',
			content_type='application/pdf',
		)

		response = self.client.post(
			url,
			data={
				'buyer_name': 'Maria da Silva',
				'buyer_email': 'maria@email.com',
				'payment_proof_type': 'PIX',
				'payment_proof_file': proof_file,
			},
			format='multipart',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.gift.refresh_from_db()
		self.assertEqual(self.gift.status, 'RESERVED')
		self.assertEqual(self.gift.buyer_name, 'Maria da Silva')
		self.assertEqual(self.gift.buyer_email, 'maria@email.com')
		self.assertEqual(self.gift.payment_proof_type, 'PIX')
		self.assertTrue(bool(self.gift.payment_proof_file))
		self.assertEqual(self.gift.link, 'https://example.com/gifts/jogo-de-tacas')
