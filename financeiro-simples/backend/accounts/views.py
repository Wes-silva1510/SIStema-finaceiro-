from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account, Transaction
from .serializers import (
    AccountSerializer,
    TransactionSerializer,
    TransferSerializer,
)
from .services import TransferError, transfer


class AccountListCreate(generics.ListCreateAPIView):
    queryset = Account.objects.order_by("id")
    serializer_class = AccountSerializer


class AccountTransactions(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(account_id=self.kwargs["pk"])


class TransferView(APIView):
    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            processed = transfer(
                data["from_account"], data["to_account"],
                data["amount"], data["idempotency_key"],
            )
        except TransferError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        if not processed:
            return Response({"detail": "Transferência já processada."})
        return Response({"detail": "Transferência realizada."}, status=status.HTTP_201_CREATED)
