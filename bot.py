import discord
import yaml
import asyncio
import os
import time
from core.logs.logger import logger, log_command
from core.utils.cleanup import start_cleanup, stop_cleanup

# Carregar configurações
with open('config/bot.yaml', 'r', encoding='utf-8') as f:
    bot_config = yaml.safe_load(f)

with open('config/squarecloud.yaml', 'r', encoding='utf-8') as f:
    squarecloud_config = yaml.safe_load(f)

BOT_TOKEN = bot_config.get('bot_token')
BOT_NAME = bot_config.get('bot_name', 'HyperDeploy')
BOT_VERSION = bot_config.get('version', '1.0.0')
GUILD_ID = bot_config.get('guild_id')

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

# Criar bot
bot = discord.Bot(intents=intents)

# Variável global para o gerenciador de limpeza
cleanup_manager = None

@bot.event
async def on_ready():
    """Evento executado quando o bot fica online"""
    global start_time
    start_time = time.time()
    
    logger.success(f"Bot online como {bot.user}")
    logger.info(f"Versão {BOT_VERSION} • {len(bot.guilds)} servidor(es)")
    
    # Inicializar módulos primeiro
    await initialize_modules()
    
    # Sincronizar comandos slash após inicializar módulos
    try:
        # Forçar sincronização completa para remover comandos antigos
        synced = await bot.sync_commands(force=True)
        if synced:
            logger.info(f"Comandos sincronizados ({len(synced)} total)")
        else:
            logger.info("Comandos sincronizados")
    except Exception as e:
        logger.warning(f"Erro ao sincronizar comandos: {e}")
    
    # Iniciar loops assíncronos após o bot estar online
    try:
        from core.payments.manager import payment_manager
        from core.payments.deploy_manager import deploy_manager
        from core.tickets.manager import ticket_manager
        
        # Iniciar loop de limpeza de pagamentos
        if payment_manager:
            bot.loop.create_task(payment_manager.cleanup_loop())
            logger.info("Loop de limpeza de pagamentos ativo")
        
        # Iniciar loop de deploy automático
        if deploy_manager:
            bot.loop.create_task(deploy_manager.start_deploy_loop())
            logger.info("Loop de deploy automático ativo")
        
        # Iniciar loop de limpeza de tickets
        if ticket_manager:
            bot.loop.create_task(ticket_manager.cleanup_expired_tickets())
            logger.info("Loop de limpeza de tickets ativo")
            
    except Exception as e:
        logger.error(f"Erro ao iniciar loops assíncronos: {e}")
    
    logger.success("Sistema HyperDeploy inicializado com sucesso")

async def initialize_modules():
    """Inicializa todos os módulos do sistema"""
    try:
        # Importar e configurar gerenciadores
        from core.payments.config_manager import setup as setup_config_manager
        setup_config_manager()
        
        from core.payments.manager import setup as setup_payment_manager
        setup_payment_manager()
        
        from core.squarecloud.client import setup as setup_squarecloud_manager
        api_key = squarecloud_config.get('api_key')
        if api_key and api_key != "SUA_API_KEY_AQUI":
            setup_squarecloud_manager(api_key)
        else:
            logger.warning("API Key Square Cloud não configurada")
        
        from core.squarecloud.user_keys import setup as setup_user_keys_manager
        setup_user_keys_manager()
        
        from core.payments.deploy_manager import setup as setup_deploy_manager
        setup_deploy_manager()
        
        from core.squarecloud.backup_manager import setup as setup_backup_manager
        setup_backup_manager()
        
        from core.squarecloud.domain_manager import setup as setup_domain_manager
        setup_domain_manager()
        
        # Inicializar sistema de tickets
        from core.tickets.manager import setup as setup_tickets
        setup_tickets(bot)
        
        # Inicializar sistema de uploads
        from core.tickets.uploads import setup as setup_uploads
        setup_uploads(bot)
        
        # Inicializar painéis de comando
        from core.commands.userpanel import setup as setup_userpanel
        from core.commands.admin_panel import setup as setup_admin_panel
        from core.logs.organized_logger import setup as setup_organized_logger

        setup_userpanel(bot, GUILD_ID)
        setup_admin_panel(bot, GUILD_ID)
        setup_organized_logger(bot)
        
        logger.info("Todos os módulos carregados com sucesso")
        
    except Exception as e:
        logger.error(f"Erro ao inicializar módulos: {e}")

@bot.event
async def on_guild_join(guild):
    """Evento executado quando o bot entra em um servidor"""
    logger.info(f"Bot adicionado ao servidor: {guild.name} (ID: {guild.id})")
    logger.info(f"Total de servidores: {len(bot.guilds)}")

@bot.event
async def on_guild_remove(guild):
    """Evento executado quando o bot sai de um servidor"""
    logger.info(f"Bot removido do servidor: {guild.name} (ID: {guild.id})")
    logger.info(f"Total de servidores: {len(bot.guilds)}")

@bot.event
async def on_message(message):
    """Evento executado quando uma mensagem é enviada"""
    # Ignorar mensagens do próprio bot
    if message.author == bot.user:
        return
    
    # Processar uploads em tickets
    if message.channel.name.startswith('ticket-'):
        from core.tickets.uploads import upload_manager
        if upload_manager:
            await upload_manager.process_upload(message)
    
    # Processar seleção de aplicações
    if hasattr(bot, 'app_selections') and message.author.id in bot.app_selections:
        await process_app_selection(message)

@bot.event
async def on_command_error(ctx, error):
    """Evento executado quando ocorre erro em comando"""
    if isinstance(error, discord.ApplicationCommandInvokeError):
        logger.error(f"Erro no comando {ctx.command}: {error.original}")
    else:
        logger.error(f"Erro no comando {ctx.command}: {error}")

async def process_app_selection(message):
    """Processa seleção de aplicação via mensagem"""
    try:
        user_id = message.author.id
        selection_data = bot.app_selections.get(user_id)
        
        if not selection_data:
            return
        
        # Tentar converter para número
        try:
            selection = int(message.content.strip())
        except ValueError:
            await message.channel.send("❌ Digite apenas o número da aplicação.", delete_after=5)
            return
        
        # Verificar se o número é válido
        apps = selection_data.get('apps', [])
        if selection < 1 or selection > len(apps):
            await message.channel.send(f"❌ Número inválido. Digite um número entre 1 e {len(apps)}.", delete_after=5)
            return
        
        # Obter aplicação selecionada
        selected_app = apps[selection - 1]
        action = selection_data.get('action', 'unknown')
        
        # Executar ação
        await execute_app_action(message, selected_app, action)
        
        # Limpar seleção
        del bot.app_selections[user_id]
        
    except Exception as e:
        logger.error(f"Erro ao processar seleção de aplicação: {e}")

async def execute_app_action(message, app, action):
    """Executa ação na aplicação selecionada"""
    try:
        from core.squarecloud.client import squarecloud_client
        
        if not squarecloud_client:
            await message.channel.send("❌ Cliente Square Cloud não disponível.", delete_after=5)
            return
        
        app_id = app.get('id')
        app_name = app.get('name', 'Aplicação')
        
        if action == 'delete':
            success = await squarecloud_client.delete_app(app_id)
            if success:
                await message.channel.send(f"✅ Aplicação **{app_name}** deletada com sucesso!", delete_after=10)
            else:
                await message.channel.send(f"❌ Erro ao deletar aplicação **{app_name}**.", delete_after=10)
        
        elif action == 'start':
            success = await squarecloud_client.start_app(app_id)
            if success:
                await message.channel.send(f"▶️ Aplicação **{app_name}** iniciada!", delete_after=10)
            else:
                await message.channel.send(f"❌ Erro ao iniciar aplicação **{app_name}**.", delete_after=10)
        
        elif action == 'stop':
            success = await squarecloud_client.stop_app(app_id)
            if success:
                await message.channel.send(f"⏹️ Aplicação **{app_name}** parada!", delete_after=10)
            else:
                await message.channel.send(f"❌ Erro ao parar aplicação **{app_name}**.", delete_after=10)
        
        elif action == 'restart':
            success = await squarecloud_client.restart_app(app_id)
            if success:
                await message.channel.send(f"🔄 Aplicação **{app_name}** reiniciada!", delete_after=10)
            else:
                await message.channel.send(f"❌ Erro ao reiniciar aplicação **{app_name}**.", delete_after=10)
        
        else:
            await message.channel.send(f"❌ Ação desconhecida: {action}", delete_after=5)
            
    except Exception as e:
        logger.error(f"Erro ao executar ação na aplicação: {e}")
        await message.channel.send("❌ Erro interno ao executar ação.", delete_after=5)

# Configurar start_time para cálculo de uptime
bot.start_time = discord.utils.utcnow()

# Inicializar seleções de aplicações
bot.app_selections = {}

# Executar bot
if __name__ == "__main__":
    try:
        logger.info("Iniciando HyperDeploy...")
        bot.run(BOT_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot interrompido pelo usuário")
        if cleanup_manager:
            asyncio.run(stop_cleanup(cleanup_manager))
    except Exception as e:
        logger.critical(f"Erro fatal ao iniciar bot: {e}")
        if cleanup_manager:
            asyncio.run(stop_cleanup(cleanup_manager))
