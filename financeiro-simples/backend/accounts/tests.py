from decimal import Decimal

from django.test import TestCase

from .models import Account, Transaction
from .services import TransferError, transfer


class TransferTests(TestCase):
    def setUp(self):
        self.a = Account.objects.create(owner_name="Ana", balance=Decimal("100.00"))
        self.b = Account.objects.create(owner_name="Bruno", balance=Decimal("0.00"))

    def test_transfer_moves_money(self):
        transfer(self.a.id, self.b.id, Decimal("30.00"), "k1")
        self.a.refresh_from_db()
        self.b.refresh_from_db()
        self.assertEqual(self.a.balance, Decimal("70.00"))
        self.assertEqual(self.b.balance, Decimal("30.00"))
        self.assertEqual(Transaction.objects.count(), 2)

    def test_insufficient_balance(self):
        with self.assertRaises(TransferError):
            transfer(self.a.id, self.b.id, Decimal("500.00"), "k2")
        self.a.refresh_from_db()
        self.assertEqual(self.a.balance, Decimal("100.00"))
        self.assertEqual(Transaction.objects.count(), 0)

    def test_same_key_does_not_duplicate(self):
        transfer(self.a.id, self.b.id, Decimal("10.00"), "k3")
        repeated = transfer(self.a.id, self.b.id, Decimal("10.00"), "k3")
        self.a.refresh_from_db()
        self.assertFalse(repeated)
        self.assertEqual(self.a.balance, Decimal("90.00"))

    def test_invalid_amount_and_same_account(self):
        with self.assertRaises(TransferError):
            transfer(self.a.id, self.b.id, Decimal("0"), "k4")
        with self.assertRaises(TransferError):
            transfer(self.a.id, self.a.id, Decimal("5.00"), "k5")
