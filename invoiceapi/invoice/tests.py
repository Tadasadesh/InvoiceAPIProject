from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Invoice, InvoiceDetail

class InvoiceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.invoice = Invoice.objects.create(date='2023-01-01', customer_name='Test Customer')
        self.invoice_detail_data = {
            'description': 'Test Item',
            'quantity': 2,
            'unit_price': 10.00,
            'price': 20.00,
        }

    def test_create_invoice(self):
        data = {
            'date': '2023-01-02',
            'customer_name': 'New Customer',
            'details': [self.invoice_detail_data],
        }

        response = self.client.post('/invoices/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)
        self.assertEqual(InvoiceDetail.objects.count(), 1)

    def test_get_invoice_list(self):
        response = self.client.get('/invoices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_invoice_detail(self):
        response = self.client.get(f'/invoices/{self.invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], 'Test Customer')

    def test_update_invoice(self):
        data = {
            'customer_name': 'Updated Customer',
            'details': [self.invoice_detail_data],
        }

        response = self.client.put(f'/invoices/{self.invoice.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoice.objects.get(id=self.invoice.id).customer_name, 'Updated Customer')

    def test_delete_invoice(self):
        response = self.client.delete(f'/invoices/{self.invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(InvoiceDetail.objects.count(), 0)

