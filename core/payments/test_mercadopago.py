import yaml
from mercadopago import criar_cobranca_pix

def test_criar_cobranca_pix():
    # Carregar access_token do bot.yaml
    with open('config/bot.yaml', 'r', encoding='utf-8') as f:
        bot_config = yaml.safe_load(f)
        access_token = bot_config.get('mercadopago_access_token')
    if not access_token:
        print('Access token Mercado Pago não configurado.')
        return
    valor = 1.00
    descricao = 'Teste de cobrança PIX via Mercado Pago'
    codigo_pix = criar_cobranca_pix(valor, descricao, access_token)
    if codigo_pix:
        print('Código PIX gerado com sucesso:')
        print(codigo_pix)
    else:
        print('Falha ao gerar cobrança PIX.')

if __name__ == '__main__':
    test_criar_cobranca_pix() 