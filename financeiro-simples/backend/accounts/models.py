from decimal import Decimal

from django.db import models


class Account(models.Model):
    owner_name = models.CharField(max_length=100)
    balance = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )

    def __str__(self):
        return f"{self.owner_name} ({self.balance})"


class Transaction(models.Model):
    """Lançamento do extrato. Positivo = crédito, negativo = débito."""

    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    description = models.CharField(max_length=255)
    idempotency_key = models.CharField(max_length=80, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.description}: {self.amount}"
