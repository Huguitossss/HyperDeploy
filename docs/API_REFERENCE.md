# 📚 Referência da API - HyperDeploy

Documentação completa das APIs e integrações utilizadas no HyperDeploy.

## 🔗 APIs Integradas

### Discord API
- **Biblioteca**: discord.py 2.6.1
- **Documentação**: [discordpy.readthedocs.io](https://discordpy.readthedocs.io)
- **Versão**: v10 (mais recente)

### Square Cloud API
- **Biblioteca**: squarecloud-api 3.7.3
- **Documentação**: [docs.squarecloud.app](https://docs.squarecloud.app)
- **Versão**: v2

### Mercado Pago API
- **Biblioteca**: aiohttp (requisições customizadas)
- **Documentação**: [developers.mercadopago.com](https://developers.mercadopago.com)
- **Versão**: v1

## 🤖 Discord API

### Configuração
```python
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='/', intents=intents)
```

### Comandos Slash
```python
@bot.slash_command(name="admin", description="Painel administrativo")
async def admin(ctx):
    # Implementação do comando
    pass
```

### Interações
```python
@discord.ui.button(label="Botão", style=discord.ButtonStyle.primary)
async def button_callback(self, button, interaction):
    await interaction.response.send_message("Resposta", ephemeral=True)
```

### Permissões Necessárias
- **Send Messages** - Enviar mensagens
- **Manage Channels** - Criar/gerenciar canais
- **Manage Messages** - Gerenciar mensagens
- **Attach Files** - Anexar arquivos
- **Embed Links** - Usar embeds
- **Use Slash Commands** - Usar comandos slash

## ☁️ Square Cloud API

### Configuração
```python
from squarecloud import SquareCloud

client = SquareCloud(api_key="SUA_API_KEY")
```

### Métodos Principais

#### Aplicações
```python
# Listar aplicações
apps = await client.get_applications()

# Obter aplicação específica
app = await client.get_application(app_id)

# Criar aplicação
app = await client.create_application(
    name="Minha App",
    main_file="main.py",
    memory=512
)

# Deletar aplicação
await client.delete_application(app_id)
```

#### Status e Controle
```python
# Status da aplicação
status = await client.get_application_status(app_id)

# Iniciar aplicação
await client.start_application(app_id)

# Parar aplicação
await client.stop_application(app_id)

# Reiniciar aplicação
await client.restart_application(app_id)
```

#### Logs
```python
# Obter logs
logs = await client.get_application_logs(app_id)

# Logs em tempo real
async for log in client.get_application_logs_stream(app_id):
    print(log)
```

#### Backups
```python
# Listar backups
backups = await client.get_application_backups(app_id)

# Criar backup
backup = await client.create_application_backup(app_id)

# Baixar backup
await client.download_application_backup(app_id, backup_id, "backup.zip")
```

#### Domínios
```python
# Listar domínios
domains = await client.get_application_domains(app_id)

# Adicionar domínio
domain = await client.add_application_domain(app_id, "meu-site.com")

# Remover domínio
await client.remove_application_domain(app_id, domain_id)
```

### Códigos de Status
- **200** - Sucesso
- **401** - Token inválido
- **403** - Sem permissão
- **404** - Aplicação não encontrada
- **429** - Rate limit excedido
- **500** - Erro interno do servidor

## 💳 Mercado Pago API

### Configuração
```python
import aiohttp

MERCADOPAGO_ACCESS_TOKEN = "SEU_ACCESS_TOKEN"
BASE_URL = "https://api.mercadopago.com"
```

### Métodos Principais

#### Criar Pagamento PIX
```python
async def create_pix_payment(amount: float, description: str):
    url = f"{BASE_URL}/v1/payments"
    headers = {
        "Authorization": f"Bearer {MERCADOPAGO_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "transaction_amount": amount,
        "description": description,
        "payment_method_id": "pix",
        "payer": {
            "email": "payer@email.com"
        }
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            return await response.json()
```

#### Verificar Status do Pagamento
```python
async def check_payment_status(payment_id: str):
    url = f"{BASE_URL}/v1/payments/{payment_id}"
    headers = {
        "Authorization": f"Bearer {MERCADOPAGO_ACCESS_TOKEN}"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()
```

#### Webhook de Pagamento
```python
@app.route('/webhook', methods=['POST'])
async def webhook_handler():
    data = request.json
    
    if data['type'] == 'payment':
        payment_id = data['data']['id']
        payment_info = await check_payment_status(payment_id)
        
        if payment_info['status'] == 'approved':
            # Processar pagamento aprovado
            await process_approved_payment(payment_info)
    
    return {'status': 'ok'}, 200
```

### Status de Pagamento
- **pending** - Aguardando pagamento
- **approved** - Pagamento aprovado
- **authorized** - Pagamento autorizado
- **in_process** - Em processamento
- **in_mediation** - Em mediação
- **rejected** - Pagamento rejeitado
- **cancelled** - Pagamento cancelado
- **refunded** - Pagamento reembolsado
- **charged_back** - Pagamento contestado

## 🔧 APIs Internas

### ConfigManager
```python
from core.payments.config_manager import config_manager

# Obter configurações
price = config_manager.get_fresh_deploy_price()
max_size = config_manager.get_max_file_size_mb()
ticket_timeout = config_manager.get_ticket_timeout_minutes()

# Definir configurações
config_manager.set_deploy_price(25.00)
config_manager.set_max_file_size_mb(150)
config_manager.set_ticket_timeout_minutes(30)
```

### PaymentManager
```python
from core.payments.manager import payment_manager

# Criar pagamento
payment_id = payment_manager.create_payment(
    user_id=123456789,
    amount=25.00,
    description="Deploy HyperDeploy"
)

# Verificar pagamento
payment = payment_manager.get_payment(payment_id)

# Limpar pagamentos expirados
payment_manager.cleanup_expired_payments()
```

### TicketManager
```python
from core.tickets.manager import ticket_manager

# Criar ticket
channel = await ticket_manager.create_ticket(
    user_id=123456789,
    guild_id=987654321,
    channel_id=111222333
)

# Fechar ticket
success = await ticket_manager.close_ticket(
    user_id=123456789,
    reason="Deploy concluído"
)

# Limpar tickets expirados
await ticket_manager.cleanup_expired_tickets()
```

### UploadManager
```python
from core.tickets.uploads import upload_manager

# Processar upload
file_info = await upload_manager.process_upload(message)

# Validar arquivo
is_valid = upload_manager.is_valid_file(filename)

# Obter tamanho máximo
max_size = upload_manager.get_max_file_size()
```

## 📊 Sistema de Logs

### OrganizedLogger
```python
from core.logs.organized_logger import log_action, log_admin, log_payment, log_deploy

# Log de ação do usuário
await log_action(
    user_id=123456789,
    action="Deploy Iniciado",
    details="Arquivo: app.zip | Tamanho: 15.2 MB",
    success=True
)

# Log administrativo
await log_admin(
    admin_id=987654321,
    action="Alterou preço",
    details="De R$ 10,00 para R$ 25,00"
)

# Log de pagamento
await log_payment(
    user_id=123456789,
    payment_id="pix_123_456",
    amount=25.00,
    status="approved",
    details="Deploy automático iniciado"
)

# Log de deploy
await log_deploy(
    user_id=123456789,
    app_id="app_123",
    success=True,
    details="Aplicação implantada com sucesso"
)
```

## 🔐 Autenticação e Segurança

### Tokens e Chaves
```python
# Discord Bot Token
DISCORD_TOKEN = "SEU_TOKEN_DISCORD_AQUI"

# Square Cloud API Key
SQUARECLOUD_API_KEY = "sua_api_key_aqui"

# Mercado Pago Access Token
MERCADOPAGO_ACCESS_TOKEN = "SEU_ACCESS_TOKEN_MERCADOPAGO_AQUI"
```

### Validação de Permissões
```python
def is_admin(ctx):
    return ctx.author.guild_permissions.administrator

@bot.slash_command(name="admin")
async def admin(ctx):
    if not is_admin(ctx):
        await ctx.respond("❌ Você não tem permissão para usar este comando.", ephemeral=True)
        return
    # Comando administrativo
```

### Rate Limiting
```python
from discord.ext import commands

@commands.cooldown(1, 5, commands.BucketType.user)  # 1 uso a cada 5 segundos
async def command_with_rate_limit(ctx):
    # Comando com rate limiting
    pass
```

## 🐛 Tratamento de Erros

### Discord API Errors
```python
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Comando não encontrado.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão para usar este comando.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏰ Aguarde {error.retry_after:.2f} segundos.")
    else:
        await ctx.send(f"❌ Erro: {error}")
```

### Square Cloud API Errors
```python
try:
    app = await client.get_application(app_id)
except Exception as e:
    if "401" in str(e):
        logger.error("Token da Square Cloud inválido")
    elif "404" in str(e):
        logger.error("Aplicação não encontrada")
    elif "429" in str(e):
        logger.error("Rate limit excedido")
    else:
        logger.error(f"Erro na Square Cloud API: {e}")
```

### Mercado Pago API Errors
```python
try:
    payment = await create_pix_payment(amount, description)
except aiohttp.ClientError as e:
    logger.error(f"Erro na API do Mercado Pago: {e}")
except Exception as e:
    logger.error(f"Erro inesperado: {e}")
```

## 📈 Métricas e Monitoramento

### Health Check
```python
async def health_check():
    checks = {
        "discord": await check_discord_connection(),
        "squarecloud": await check_squarecloud_api(),
        "mercadopago": await check_mercadopago_api(),
        "database": await check_database_connection()
    }
    
    return {
        "status": "healthy" if all(checks.values()) else "unhealthy",
        "checks": checks,
        "timestamp": datetime.now().isoformat()
    }
```

### Performance Metrics
```python
import time

async def measure_performance(func, *args, **kwargs):
    start_time = time.time()
    try:
        result = await func(*args, **kwargs)
        duration = time.time() - start_time
        logger.info(f"Função {func.__name__} executada em {duration:.2f}s")
        return result
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Erro em {func.__name__} após {duration:.2f}s: {e}")
        raise
```

## 🔄 Webhooks e Eventos

### Discord Webhooks
```python
async def send_webhook_message(webhook_url, content, embeds=None):
    async with aiohttp.ClientSession() as session:
        data = {"content": content}
        if embeds:
            data["embeds"] = embeds
        
        async with session.post(webhook_url, json=data) as response:
            return response.status == 204
```

### Mercado Pago Webhooks
```python
@app.route('/mercadopago-webhook', methods=['POST'])
async def mercadopago_webhook():
    data = request.json
    
    # Verificar assinatura (recomendado)
    signature = request.headers.get('X-Signature')
    if not verify_signature(data, signature):
        return {'error': 'Invalid signature'}, 400
    
    # Processar evento
    if data['type'] == 'payment':
        await process_payment_event(data['data'])
    
    return {'status': 'ok'}, 200
```

## 📚 Recursos Adicionais

### Documentação Oficial
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Square Cloud API Documentation](https://docs.squarecloud.app/)
- [Mercado Pago API Documentation](https://developers.mercadopago.com/)

### Comunidades
- [Discord.py Community](https://discord.gg/dpy)
- [Square Cloud Discord](https://discord.gg/squarecloud)
- [Mercado Pago Developers](https://developers.mercadopago.com/community)

### Ferramentas de Desenvolvimento
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Square Cloud Dashboard](https://squarecloud.app/dashboard)
- [Mercado Pago Dashboard](https://www.mercadopago.com.br/developers)

---

**HyperDeploy API Reference - Documentação completa e atualizada** 📚
