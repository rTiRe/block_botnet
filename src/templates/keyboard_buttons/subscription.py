from aiocryptopay.const import Assets
from aiocryptopay.const import CurrencyType

currency_type = CurrencyType.CRYPTO
asset = Assets.TON

invoice_const_data = {
    'currency_type': str(currency_type),
    'asset': str(asset),
    'hidden_message': 'Спасибо за оплату!',
    'paid_btn_name': 'openBot',
}

SUBSCRIPTIONS = {
    'one_week': {
        'name': '1 неделя',
        'duration': 7,
        'invoice': {
            'amount': 2,
            'description': 'Оплата подписки на 1 неделю',
            **invoice_const_data,
        },
    },
    'two_weeks': {
        'name': '2 недели',
        'duration': 14,
        'invoice': {
            'amount': 5,
            'description': 'Оплата подписки на 2 недели',
            **invoice_const_data,
        },
    },
    'one_month': {
        'name': '1 месяц',
        'duration': 30,
        'invoice': {
            'amount': 10,
            'description': 'Оплата подписки на 1 месяц',
            **invoice_const_data,
        },
    },
}
