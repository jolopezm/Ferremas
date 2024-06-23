from transbank.webpay.webpay_plus.transaction import Transaction, IntegrationApiKeys, IntegrationCommerceCodes
from transbank.common.integration_type import IntegrationType
from transbank.common.options import WebpayOptions

commerce_code = '597055555532'
api_key = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
options = WebpayOptions(
    commerce_code=commerce_code,
    api_key=api_key,
    integration_type=IntegrationType.TEST
)
transaction = Transaction(options)

async def init_transaction(data: dict):
    buy_order = data['buy_order']
    session_id = data['session_id']
    amount = data['amount']
    return_url = data['return_url']
    
    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    resp = tx.create(buy_order, session_id, amount, return_url)
    
    return {
        "url": resp['url'],
        "token": resp['token']
    }

async def commit_transaction(token):
    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    response = tx.commit(token)
    return response