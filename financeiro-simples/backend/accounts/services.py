from django.db import transaction

from .models import Account, Transaction


class TransferError(Exception):
    """Erro de regra de negócio na transferência."""


def transfer(from_id, to_id, amount, key):
    """Transfere `amount` (Decimal) de uma conta para outra.

    Retorna True se processou e False se a chave já havia sido usada
    (idempotência: repetir o pedido não duplica a transferência).
    """
    if amount <= 0:
        raise TransferError("O valor deve ser positivo.")
    if from_id == to_id:
        raise TransferError("As contas de origem e destino devem ser diferentes.")

    with transaction.atomic():  # tudo ou nada
        if Transaction.objects.filter(idempotency_key=f"{key}-out").exists():
            return False

        # Trava as linhas (sempre na mesma ordem, para evitar deadlock)
        accounts = {
            a.id: a
            for a in Account.objects.select_for_update()
            .filter(id__in=[from_id, to_id])
            .order_by("id")
        }
        if from_id not in accounts or to_id not in accounts:
            raise TransferError("Conta não encontrada.")

        origem, destino = accounts[from_id], accounts[to_id]
        if origem.balance < amount:
            raise TransferError("Saldo insuficiente.")

        origem.balance -= amount
        destino.balance += amount
        origem.save()
        destino.save()

        Transaction.objects.create(
            account=origem, amount=-amount,
            description=f"Transferência enviada para {destino.owner_name}",
            idempotency_key=f"{key}-out",
        )
        Transaction.objects.create(
            account=destino, amount=amount,
            description=f"Transferência recebida de {origem.owner_name}",
            idempotency_key=f"{key}-in",
        )
    return True
