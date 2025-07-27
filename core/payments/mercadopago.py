import requests
import logging
import uuid
from typing import Optional

# Função para criar cobrança PIX Mercado Pago

def criar_cobranca_pix(valor: float, descricao: str, access_token: str, payer_email: str = "comprador@email.com") -> Optional[str]:
    """
    Cria uma cobrança PIX no Mercado Pago e retorna o código para gerar QR Code.
    :param valor: Valor da cobrança (float)
    :param descricao: Descrição da cobrança
    :param access_token: Access token do Mercado Pago
    :param payer_email: E-mail do pagador (opcional)
    :return: Código PIX (str) ou None em caso de erro
    """
    # Validar valor
    if valor <= 0:
        logging.error(f"[MercadoPago] Valor inválido: {valor}. Deve ser maior que zero.")
        return None
    
    url = "https://api.mercadopago.com/v1/payments"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Idempotency-Key": str(uuid.uuid4())  # Header obrigatório para evitar duplicatas
    }
    payload = {
        "transaction_amount": float(valor),
        "description": descricao,
        "payment_method_id": "pix",
        "payer": {
            "email": payer_email
        }
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code == 201:
            data = response.json()
            return data["point_of_interaction"]["transaction_data"]["qr_code"]
        else:
            logging.error(f"[MercadoPago] Erro {response.status_code}: {response.text}")
            return None
    except Exception as e:
        logging.error(f"[MercadoPago] Exceção: {e}")
        return None 