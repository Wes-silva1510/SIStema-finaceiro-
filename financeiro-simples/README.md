# Mini Sistema Financeiro (Django + React)

Projeto de estudo: contas, transferências e extrato.

## O que demonstra
- **Decimal** (nunca float) para valores em dinheiro
- **transaction.atomic**: débito e crédito acontecem juntos ou nenhum acontece
- **select_for_update**: trava as contas contra concorrência
- **Chave de idempotência**: reenviar a mesma transferência não duplica
- **Lançamentos imutáveis** (extrato) para rastreabilidade
- API REST com Django REST Framework + interface em React
- Testes automatizados das regras de transferência

## Como rodar

### Back-end
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations accounts
python manage.py migrate
python manage.py test           # roda os testes
python manage.py runserver      # http://localhost:8000
```

### Front-end (outro terminal)
```bash
cd frontend
npm install
npm run dev                     # http://localhost:5173
```

## Endpoints
| Método | Rota | Descrição |
|---|---|---|
| GET/POST | `/api/accounts/` | Lista / cria contas |
| GET | `/api/accounts/<id>/transactions/` | Extrato da conta |
| POST | `/api/transfers/` | Transfere entre contas |

## Limitações (próximos passos)
- Sem autenticação (próximo passo: JWT e permissão por dono da conta)
- SQLite no desenvolvimento (em produção: PostgreSQL, onde o lock de linha funciona)
- Sem integração com gateway de pagamento / Pix
