import discord
import yaml
import json
import asyncio
from squarecloud import Client
from datetime import datetime
from core.logs.logger import logger

with open('config/bot.yaml', 'r', encoding='utf-8') as f:
    bot_config = yaml.safe_load(f)

BOT_NAME = bot_config.get('bot_name', 'HyperDeploy')
BOT_VERSION = bot_config.get('version', '1.0.0')

# Configuração do Mercado Pago já está no bot.yaml
with open('config/squarecloud.yaml', 'r', encoding='utf-8') as f:
    squarecloud_config = yaml.safe_load(f)

PAYMENTS_FILE = "data/payments.json"

# Dicionário para armazenar seleções de aplicação por usuário
user_app_selections = {}

class UserMainPanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.ctx = ctx

    @discord.ui.button(label="🚀 Deploy", style=discord.ButtonStyle.primary, custom_id="deploy_btn")
    async def deploy_btn(self, button, interaction):
        await interaction.response.send_message(embed=embed_deploy_panel(), view=DeployPanel(self.ctx), ephemeral=True)

    @discord.ui.button(label="🗑️ Deletar", style=discord.ButtonStyle.danger, custom_id="delete_btn")
    async def delete_btn(self, button, interaction):
        await interaction.response.send_message(embed=embed_delete_panel(), view=DeletePanel(self.ctx), ephemeral=True)

    @discord.ui.button(label="🔑 Chave", style=discord.ButtonStyle.secondary, custom_id="key_btn")
    async def key_btn(self, button, interaction):
        await interaction.response.send_message(embed=embed_key_panel(), view=KeyPanel(self.ctx), ephemeral=True)

    @discord.ui.button(label="💳 Pagamentos", style=discord.ButtonStyle.secondary, custom_id="payments_btn")
    async def payments_btn(self, button, interaction):
        await interaction.response.send_message(embed=embed_payments_panel(), view=UserPaymentsPanel(self.ctx), ephemeral=True)

    @discord.ui.button(label="📊 Status", style=discord.ButtonStyle.success, custom_id="status_btn")
    async def status_btn(self, button, interaction):
        await interaction.response.send_message(embed=embed_status_panel(), view=UserStatusPanel(self.ctx), ephemeral=True)

    @discord.ui.button(label="🗂️ Backups", style=discord.ButtonStyle.secondary, custom_id="backup_btn")
    async def backup_btn(self, button, interaction):
        await interaction.response.send_message(embed=embed_backup_panel(), view=UserBackupPanel(self.ctx), ephemeral=True)

    @discord.ui.button(label="🌐 Domínios", style=discord.ButtonStyle.secondary, custom_id="domain_btn")
    async def domain_btn(self, button, interaction):
        await interaction.response.send_message(embed=embed_domain_panel(), view=UserDomainPanel(self.ctx), ephemeral=True)

    @discord.ui.button(label="ℹ️ Info", style=discord.ButtonStyle.secondary, custom_id="info_btn")
    async def info_btn(self, button, interaction):
        await interaction.response.send_message(embed=embed_info_panel(), view=InfoPanel(self.ctx), ephemeral=True)

# Embeds de cada painel
def embed_user_main_panel():
    embed = discord.Embed(
        title="🎮 Painel de Usuário HyperDeploy",
        description="Gerencie suas aplicações e configurações em um único painel interativo.",
        color=0x5865F2,
        timestamp=discord.utils.utcnow()
    )
    embed.add_field(name="🚀 Deploy", value="Fazer deploy de aplicações via ticket", inline=False)
    embed.add_field(name="🗑️ Deletar", value="Remover aplicações da Square Cloud", inline=False)
    embed.add_field(name="🔑 Chave", value="Verificar status da chave da Square Cloud", inline=False)
    embed.add_field(name="💳 Pagamentos", value="Ver histórico de pagamentos", inline=False)
    embed.add_field(name="📊 Status", value="Ver status e controlar aplicações", inline=False)
    embed.add_field(name="🗂️ Backups", value="Gerenciar backups das aplicações", inline=False)
    embed.add_field(name="🌐 Domínios", value="Gerenciar domínios personalizados", inline=False)
    embed.add_field(name="ℹ️ Info", value="Informações do bot e comandos", inline=False)
    embed.set_footer(text="HyperDeploy • Painel de Usuário")
    return embed

def embed_deploy_panel():
    return discord.Embed(title="🚀 Deploy", description="Faça deploy de suas aplicações via ticket.", color=0x00ff00)

def embed_delete_panel():
    return discord.Embed(title="🗑️ Deletar", description="Remova aplicações da Square Cloud.", color=0xff0000)

def embed_key_panel():
    embed = discord.Embed(
        title="🔑 Status da Chave Square Cloud",
        description="Verifique o status da sua chave da Square Cloud.",
        color=0xffff00
    )
    embed.add_field(name="ℹ️ Como obter", value="1. Acesse [Square Cloud](https://squarecloud.app)\n2. Vá em 'Minha Conta' > 'API'\n3. Copie sua chave de API", inline=False)
    embed.add_field(name="🔒 Segurança", value="Sua chave é armazenada localmente e nunca compartilhada.", inline=False)
    embed.add_field(name="⚙️ Configuração", value="As chaves devem ser configuradas pelo administrador.", inline=False)
    return embed

def embed_payments_panel():
    return discord.Embed(title="💳 Pagamentos", description="Veja seu histórico de pagamentos.", color=0x00ffff)

def embed_status_panel():
    return discord.Embed(title="📊 Status", description="Veja status e controle aplicações.", color=0x00ff00)

def embed_backup_panel():
    return discord.Embed(title="🗂️ Backups", description="Gerencie backups das aplicações.", color=0x2ecc71)

def embed_domain_panel():
    return discord.Embed(title="🌐 Domínios", description="Gerencie domínios personalizados.", color=0x9b59b6)

def embed_info_panel():
    embed = discord.Embed(
        title="ℹ️ Informações do HyperDeploy",
        description="Sistema completo de gerenciamento de aplicações Square Cloud",
        color=0x3498db
    )
    embed.add_field(name="🚀 Funcionalidades", value="• Deploy automático\n• Pagamentos PIX\n• Gerenciamento completo\n• Backups e domínios", inline=False)
    embed.add_field(name="💳 Pagamentos", value="• Mercado Pago integrado\n• QR Code automático\n• Verificação instantânea", inline=False)
    embed.add_field(name="🔧 Comandos", value="• `/admin` - Painel administrativo\n• `/userpanel` - Painel de usuário", inline=False)
    embed.set_footer(text="HyperDeploy • Sistema Avançado")
    return embed

# DeployPanel
class DeployPanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx
    
    @discord.ui.button(label="Abrir Ticket", style=discord.ButtonStyle.primary)
    async def open_ticket(self, button, interaction):
        try:
            # Importar o sistema de tickets
            from core.tickets.manager import ticket_manager
            
            if not ticket_manager:
                await interaction.response.send_message("❌ Sistema de tickets não disponível.", ephemeral=True, delete_after=5)
                return
            
            # Verificar se usuário já tem ticket ativo
            user_id = interaction.user.id
            existing_ticket = ticket_manager.get_ticket_info(user_id)
            
            if existing_ticket:
                await interaction.response.send_message("❌ Você já tem um ticket ativo. Aguarde o fechamento ou contate um administrador.", ephemeral=True, delete_after=10)
                return
            
            # Criar ticket
            guild_id = interaction.guild.id
            channel_id = interaction.channel.id
            
            ticket_channel = await ticket_manager.create_ticket(user_id, guild_id, channel_id)
            ticket_info = ticket_manager.get_ticket_info(user_id)
            created_at = ticket_info["created_at"] if ticket_info else None
            ts = None
            if created_at:
                try:
                    dt = datetime.fromisoformat(created_at)
                    ts = int(dt.timestamp())
                except Exception:
                    ts = None
            if ticket_channel:
                from core.payments.config_manager import config_manager
                price = config_manager.get_fresh_deploy_price() if config_manager else 10.00
                embed = discord.Embed(title="🎫 Ticket de Deploy Criado", color=0x00ff00)
                embed.add_field(name="Status", value="✅ Ticket criado com sucesso!", inline=True)
                embed.add_field(name="Canal", value=f"<#{ticket_channel.id}>", inline=True)
                embed.add_field(name="Preço", value=f"R$ {price:.2f}", inline=True)
                embed.add_field(name="Próximo Passo", value="Envie o arquivo ZIP no canal do ticket", inline=False)
                if ts:
                    embed.add_field(name="⏰ Tempo", value=f"<t:{ts}:R>", inline=True)
                embed.set_footer(text="HyperDeploy • Sistema de Deploy")
                await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=15)
            else:
                await interaction.response.send_message("❌ Erro ao criar ticket. Tente novamente.", ephemeral=True, delete_after=5)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao abrir ticket: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Ver Preço", style=discord.ButtonStyle.secondary)
    async def view_price(self, button, interaction):
        try:
            from core.payments.config_manager import config_manager
            
            # Obter preço dinâmico da configuração
            price = config_manager.get_fresh_deploy_price() if config_manager else 10.00
            
            embed = discord.Embed(title="💰 Preço do Deploy", color=0xffff00)
            embed.add_field(name="Valor", value=f"R$ {price:.2f}", inline=True)
            embed.add_field(name="Método", value="PIX via Mercado Pago", inline=True)
            embed.add_field(name="Processo", value="1. Abrir ticket\n2. Enviar ZIP\n3. Gerar PIX\n4. Confirmar pagamento\n5. Deploy automático", inline=False)
            embed.add_field(name="ℹ️ Info", value="Preço configurado pelo administrador", inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=15)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao ver preço: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.danger)
    async def close(self, button, interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.delete_original_response()

# DeletePanel
class DeletePanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx
        self.selected_app = None
    
    @discord.ui.button(label="Selecionar App", style=discord.ButtonStyle.primary)
    async def select_app(self, button, interaction):
        try:
            client = Client(squarecloud_config["api_key"])
            apps = await client.all_apps()
            if not apps:
                await interaction.response.send_message("❌ Nenhuma aplicação encontrada.", ephemeral=True, delete_after=5)
                return
            
            # Mostrar lista de apps para seleção
            app_list = "\n".join([f"`{i+1}.` {getattr(app, 'tag', app.id)} (ID: {app.id})" for i, app in enumerate(apps[:10])])
            embed = discord.Embed(title="📱 Selecione uma Aplicação", description=app_list, color=0xff0000)
            embed.set_footer(text="Digite o número da aplicação desejada")
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=30)
            
            # Armazenar apps para seleção posterior
            user_id = str(interaction.user.id)
            user_app_selections[user_id] = {
                'apps': apps[:10],
                'panel': 'delete',
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao carregar aplicações: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Deletar App", style=discord.ButtonStyle.danger)
    async def delete_app(self, button, interaction):
        user_id = str(interaction.user.id)
        selected_app = user_app_selections.get(user_id, {}).get('selected_app')
        
        if not selected_app:
            await interaction.response.send_message("❌ Selecione uma aplicação primeiro.", ephemeral=True, delete_after=5)
            return
        
        try:
            client = Client(squarecloud_config["api_key"])
            await client.delete_app(selected_app)
            await interaction.response.send_message(f"✅ Aplicação {selected_app} deletada com sucesso!", ephemeral=True, delete_after=10)
            
            # Limpar seleção
            if user_id in user_app_selections:
                del user_app_selections[user_id]
                
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao deletar aplicação: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.danger)
    async def close(self, button, interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.delete_original_response()

# KeyPanel
class KeyPanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx
    
    @discord.ui.button(label="Ver Chave", style=discord.ButtonStyle.primary)
    async def view_key(self, button, interaction):
        try:
            from core.squarecloud.user_keys import user_keys_manager
            
            user_id = interaction.user.id
            has_key = user_keys_manager.has_user_key(user_id)
            
            if has_key:
                embed = discord.Embed(
                    title="✅ Chave Configurada",
                    description="Você tem uma chave da Square Cloud configurada.",
                    color=0x00ff00
                )
                embed.add_field(name="Status", value="✅ Configurada", inline=True)
                embed.add_field(name="Próximo Passo", value="Agora você pode fazer deploy de aplicações", inline=False)
            else:
                embed = discord.Embed(
                    title="❌ Chave Não Configurada",
                    description="Você não tem uma chave da Square Cloud configurada.",
                    color=0xff9900
                )
                embed.add_field(name="Status", value="❌ Não configurada", inline=True)
                embed.add_field(name="Ação", value="Entre em contato com um administrador para configurar sua chave", inline=False)
            
            embed.set_footer(text="HyperDeploy • Sistema de Chaves")
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao verificar chave: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Testar Chave", style=discord.ButtonStyle.secondary)
    async def test_key(self, button, interaction):
        try:
            from core.squarecloud.user_keys import user_keys_manager
            
            user_id = interaction.user.id
            has_key = user_keys_manager.has_user_key(user_id)
            
            if not has_key:
                embed = discord.Embed(
                    title="❌ Chave Não Configurada",
                    description="Você não tem uma chave configurada para testar.",
                    color=0xff9900
                )
                await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)
                return
            
            # Obter chave
            api_key = user_keys_manager.get_user_key(user_id)
            if not api_key:
                embed = discord.Embed(
                    title="❌ Erro",
                    description="Chave não encontrada no sistema.",
                    color=0xff0000
                )
                await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)
                return
            
            # Testar chave com Square Cloud
            try:
                client = Client(api_key)
                apps = await client.all_apps()
                
                embed = discord.Embed(
                    title="✅ Chave Válida",
                    description="Sua chave da Square Cloud está funcionando corretamente!",
                    color=0x00ff00
                )
                embed.add_field(name="Status", value="✅ Válida", inline=True)
                embed.add_field(name="Aplicações", value=f"{len(apps)} encontradas", inline=True)
                embed.add_field(name="Próximo Passo", value="Você pode fazer deploy de aplicações", inline=False)
                
            except Exception as e:
                embed = discord.Embed(
                    title="❌ Chave Inválida",
                    description="Sua chave da Square Cloud não está funcionando.",
                    color=0xff0000
                )
                embed.add_field(name="Erro", value=str(e), inline=False)
                embed.add_field(name="Ação", value="Entre em contato com um administrador", inline=False)
            
            embed.set_footer(text="HyperDeploy • Teste de Chave")
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao testar chave: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.danger)
    async def close(self, button, interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.delete_original_response()

# UserPaymentsPanel
class UserPaymentsPanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx
    
    @discord.ui.button(label="Ver Histórico", style=discord.ButtonStyle.primary)
    async def view_history(self, button, interaction):
        try:
            user_id = str(interaction.user.id)
            with open(PAYMENTS_FILE, "r") as f:
                all_payments = json.load(f)
            
            user_payments = all_payments.get(user_id, [])
            if not user_payments:
                await interaction.response.send_message("Nenhum pagamento encontrado.", ephemeral=True, delete_after=10)
                return
            
            # Mostrar últimos 5 pagamentos
            recent_payments = user_payments[-5:]
            msg = '\n'.join([f"R$ {p.get('amount', 0):.2f} - {p.get('status', 'unknown')} - {p.get('date', 'unknown')}" for p in recent_payments])
            
            embed = discord.Embed(title="💳 Seus Últimos Pagamentos", color=0x00ffff)
            embed.add_field(name="Histórico", value=msg, inline=False)
            embed.set_footer(text=f"Total: {len(user_payments)} pagamentos")
            
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=15)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao carregar pagamentos: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.danger)
    async def close(self, button, interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.delete_original_response()

# UserStatusPanel
class UserStatusPanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx
        self.selected_app = None
    
    @discord.ui.button(label="Selecionar App", style=discord.ButtonStyle.primary)
    async def select_app(self, button, interaction):
        try:
            client = Client(squarecloud_config["api_key"])
            apps = await client.all_apps()
            if not apps:
                await interaction.response.send_message("❌ Nenhuma aplicação encontrada.", ephemeral=True, delete_after=5)
                return
            
            # Mostrar lista de apps para seleção
            app_list = "\n".join([f"`{i+1}.` {getattr(app, 'tag', app.id)} (ID: {app.id})" for i, app in enumerate(apps[:10])])
            embed = discord.Embed(title="📱 Selecione uma Aplicação", description=app_list, color=0x00ff00)
            embed.set_footer(text="Digite o número da aplicação desejada")
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=30)
            
            # Armazenar apps para seleção posterior
            user_id = str(interaction.user.id)
            user_app_selections[user_id] = {
                'apps': apps[:10],
                'panel': 'status',
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao carregar aplicações: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Ver Status", style=discord.ButtonStyle.success)
    async def view_status(self, button, interaction):
        user_id = str(interaction.user.id)
        selected_app = user_app_selections.get(user_id, {}).get('selected_app')
        
        if not selected_app:
            await interaction.response.send_message("❌ Selecione uma aplicação primeiro.", ephemeral=True, delete_after=5)
            return
        try:
            client = Client(squarecloud_config["api_key"])
            app = await client.app(selected_app)
            embed = discord.Embed(title=f"📊 Status de {selected_app}", color=0x00ff00)
            embed.add_field(name="Status", value=getattr(app, "status", "-"), inline=True)
            embed.add_field(name="CPU", value=getattr(app, "cpu", "-"), inline=True)
            embed.add_field(name="RAM", value=getattr(app, "ram", "-"), inline=True)
            embed.add_field(name="Logs", value=f"[Ver logs]({getattr(app, 'logs_url', '-')})", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=15)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao ver status: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Start", style=discord.ButtonStyle.success)
    async def start_app(self, button, interaction):
        user_id = str(interaction.user.id)
        selected_app = user_app_selections.get(user_id, {}).get('selected_app')
        
        if not selected_app:
            await interaction.response.send_message("❌ Selecione uma aplicação primeiro.", ephemeral=True, delete_after=5)
            return
        try:
            client = Client(squarecloud_config["api_key"])
            await client.start_app(selected_app)
            await interaction.response.send_message(f"✅ Aplicação {selected_app} iniciada!", ephemeral=True, delete_after=5)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao iniciar aplicação: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger)
    async def stop_app(self, button, interaction):
        user_id = str(interaction.user.id)
        selected_app = user_app_selections.get(user_id, {}).get('selected_app')
        
        if not selected_app:
            await interaction.response.send_message("❌ Selecione uma aplicação primeiro.", ephemeral=True, delete_after=5)
            return
        try:
            client = Client(squarecloud_config["api_key"])
            await client.stop_app(selected_app)
            await interaction.response.send_message(f"🛑 Aplicação {selected_app} parada!", ephemeral=True, delete_after=5)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao parar aplicação: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.danger)
    async def close(self, button, interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.delete_original_response()

# UserBackupPanel
class UserBackupPanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx
        self.selected_app = None
    
    @discord.ui.button(label="Selecionar App", style=discord.ButtonStyle.primary)
    async def select_app(self, button, interaction):
        try:
            client = Client(squarecloud_config["api_key"])
            apps = await client.all_apps()
            if not apps:
                await interaction.response.send_message("❌ Nenhuma aplicação encontrada.", ephemeral=True, delete_after=5)
                return
            
            # Mostrar lista de apps para seleção
            app_list = "\n".join([f"`{i+1}.` {getattr(app, 'tag', app.id)} (ID: {app.id})" for i, app in enumerate(apps[:10])])
            embed = discord.Embed(title="📱 Selecione uma Aplicação", description=app_list, color=0x2ecc71)
            embed.set_footer(text="Digite o número da aplicação desejada")
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=30)
            
            # Armazenar apps para seleção posterior
            user_id = str(interaction.user.id)
            user_app_selections[user_id] = {
                'apps': apps[:10],
                'panel': 'backup',
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao carregar aplicações: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Criar Backup", style=discord.ButtonStyle.success)
    async def create_backup(self, button, interaction):
        user_id = str(interaction.user.id)
        selected_app = user_app_selections.get(user_id, {}).get('selected_app')
        
        if not selected_app:
            await interaction.response.send_message("❌ Selecione uma aplicação primeiro.", ephemeral=True, delete_after=5)
            return
        try:
            client = Client(squarecloud_config["api_key"])
            result = await client.create_backup(selected_app)
            await interaction.response.send_message(f"✅ Backup criado para {selected_app}! ID: {result.get('backup_id', '-')}", ephemeral=True, delete_after=10)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao criar backup: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Listar Backups", style=discord.ButtonStyle.secondary)
    async def list_backups(self, button, interaction):
        user_id = str(interaction.user.id)
        selected_app = user_app_selections.get(user_id, {}).get('selected_app')
        
        if not selected_app:
            await interaction.response.send_message("❌ Selecione uma aplicação primeiro.", ephemeral=True, delete_after=5)
            return
        try:
            client = Client(squarecloud_config["api_key"])
            backups = await client.list_backups(selected_app)
            if not backups:
                await interaction.response.send_message(f"Nenhum backup encontrado para {selected_app}.", ephemeral=True, delete_after=10)
                return
            msg = '\n'.join([f"ID: {b.get('id', '-')} | Data: {b.get('created_at', '-')}" for b in backups])
            await interaction.response.send_message(f"Backups de {selected_app}:\n{msg}", ephemeral=True, delete_after=15)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao listar backups: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.danger)
    async def close(self, button, interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.delete_original_response()

# UserDomainPanel
class UserDomainPanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx
        self.selected_app = None
    
    @discord.ui.button(label="Selecionar App", style=discord.ButtonStyle.primary)
    async def select_app(self, button, interaction):
        try:
            client = Client(squarecloud_config["api_key"])
            apps = await client.all_apps()
            if not apps:
                await interaction.response.send_message("❌ Nenhuma aplicação encontrada.", ephemeral=True, delete_after=5)
                return
            
            # Mostrar lista de apps para seleção
            app_list = "\n".join([f"`{i+1}.` {getattr(app, 'tag', app.id)} (ID: {app.id})" for i, app in enumerate(apps[:10])])
            embed = discord.Embed(title="📱 Selecione uma Aplicação", description=app_list, color=0x9b59b6)
            embed.set_footer(text="Digite o número da aplicação desejada")
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=30)
            
            # Armazenar apps para seleção posterior
            user_id = str(interaction.user.id)
            user_app_selections[user_id] = {
                'apps': apps[:10],
                'panel': 'domain',
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao carregar aplicações: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Listar Domínios", style=discord.ButtonStyle.success)
    async def list_domains(self, button, interaction):
        user_id = str(interaction.user.id)
        selected_app = user_app_selections.get(user_id, {}).get('selected_app')
        
        if not selected_app:
            await interaction.response.send_message("❌ Selecione uma aplicação primeiro.", ephemeral=True, delete_after=5)
            return
        try:
            client = Client(squarecloud_config["api_key"])
            domains = await client.list_domains(selected_app)
            if not domains:
                await interaction.response.send_message(f"Nenhum domínio encontrado para {selected_app}.", ephemeral=True, delete_after=10)
                return
            msg = '\n'.join([f"Domínio: {d.get('domain', '-')} | Status: {d.get('status', '-')}" for d in domains])
            await interaction.response.send_message(f"Domínios de {selected_app}:\n{msg}", ephemeral=True, delete_after=15)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao listar domínios: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.danger)
    async def close(self, button, interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.delete_original_response()

# InfoPanel
class InfoPanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx
    
    @discord.ui.button(label="Sobre o Bot", style=discord.ButtonStyle.primary)
    async def about_bot(self, button, interaction):
        try:
            embed = discord.Embed(
                title=f"🤖 {BOT_NAME}",
                description="Bot para gerenciamento de aplicações na Square Cloud via Discord!",
                color=0x5865F2,
                timestamp=discord.utils.utcnow()
            )
            embed.add_field(name="📋 Comandos", value="/admin - Painel administrativo\n/userpanel - Painel de usuário", inline=False)
            embed.add_field(name="🔗 Links", value="[Square Cloud](https://squarecloud.app) | [Documentação](https://docs.squarecloud.app)", inline=False)
            embed.add_field(name="⚡ Status", value="✅ Online e funcionando", inline=False)
            embed.add_field(name="👨‍💻 Desenvolvedor", value="Hugoo", inline=False)
            embed.add_field(name="📊 Versão", value="v1.0.7", inline=False)
            embed.set_footer(text="HyperDeploy • Square Cloud")
            
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=15)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao carregar informações: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Testar Conexão", style=discord.ButtonStyle.secondary)
    async def test_connection(self, button, interaction):
        try:
            latency = round(interaction.client.latency * 1000)
            embed = discord.Embed(title="🏓 Teste de Conexão", color=0x00ff00)
            embed.add_field(name="Latência", value=f"{latency}ms", inline=True)
            embed.add_field(name="Status", value="✅ Conectado", inline=True)
            embed.add_field(name="Servidor", value=interaction.guild.name if interaction.guild else "DM", inline=True)
            
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro no teste: {e}", ephemeral=True, delete_after=5)
    
    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.danger)
    async def close(self, button, interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.delete_original_response()

def setup(bot, guild_id=None):
    @bot.slash_command(name="userpanel", description="Abrir painel interativo de usuário.", guild_ids=[guild_id] if guild_id else None)
    async def userpanel(ctx):
        await ctx.respond(embed=embed_user_main_panel(), view=UserMainPanel(ctx), ephemeral=True)

# Removido o evento duplicado on_message daqui. O processamento de uploads deve ser feito apenas no bot.py 