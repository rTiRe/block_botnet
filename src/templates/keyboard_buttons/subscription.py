from types import MappingProxyType

from aiocryptopay.const import Assets, CurrencyType

currency_type = CurrencyType.CRYPTO
asset = Assets.USDT

invoice_const_data = {
    'currency_type': str(currency_type),
    'asset': str(asset),
    'hidden_message': 'Спасибо за оплату!',
    'paid_btn_name': 'openBot',
    'paid_btn_url': 'https://t.me/bot',
}

SUBSCRIPTIONS = MappingProxyType(
    {
        'one_week': {
            'name': 'Неделя',
            'duration': 7,
            'invoice': {
                'amount': 7,
                'description': 'Оплата подписки на неделю',
                **invoice_const_data,
            },
        },
        'one_month': {
            'name': 'Месяц',
            'duration': 30,
            'invoice': {
                'amount': 15,
                'description': 'Оплата подписки на месяц',
                **invoice_const_data,
            },
        },
        'forever': {
            'name': 'Навсегда',
            'duration': -1,
            'invoice': {
                'amount': 30,
                'description': 'Оплата бессрочной подписки',
                **invoice_const_data,
            },
        },
    },
)
