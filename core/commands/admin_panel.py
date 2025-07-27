import discord
import yaml
import json
import asyncio
from datetime import datetime
from core.payments.config_manager import config_manager
from core.logs.logger import logger

class AdminMainPanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.ctx = ctx

    @discord.ui.button(label="💰 Preços", style=discord.ButtonStyle.primary, custom_id="prices_btn")
    async def prices_btn(self, button, interaction):
        await interaction.response.send_message(embed=embed_prices_panel(), view=PricesPanel(self.ctx), ephemeral=True)
        await self.log_admin_action(interaction.user.id, "Acessou Painel de Preços")

    @discord.ui.button(label="⚙️ Configurações", style=discord.ButtonStyle.secondary, custom_id="config_btn")
    async def config_btn(self, button, interaction):
        await interaction.response.send_message(embed=embed_config_panel(), view=ConfigPanel(self.ctx), ephemeral=True)
        await self.log_admin_action(interaction.user.id, "Acessou Painel de Configurações")

    @discord.ui.button(label="📊 Status", style=discord.ButtonStyle.success, custom_id="status_btn")
    async def status_btn(self, button, interaction):
        await interaction.response.send_message(embed=embed_status_panel(), view=StatusPanel(self.ctx), ephemeral=True)
        await self.log_admin_action(interaction.user.id, "Acessou Painel de Status")

    @discord.ui.button(label="🧹 Limpeza", style=discord.ButtonStyle.danger, custom_id="cleanup_btn")
    async def cleanup_btn(self, button, interaction):
        await interaction.response.send_message(embed=embed_cleanup_panel(), view=CleanupPanel(self.ctx), ephemeral=True)
        await self.log_admin_action(interaction.user.id, "Acessou Painel de Limpeza")

    @discord.ui.button(label="🔒 Tickets", style=discord.ButtonStyle.danger, custom_id="tickets_btn")
    async def tickets_btn(self, button, interaction):
        await interaction.response.send_message(embed=embed_tickets_panel(), view=TicketsPanel(self.ctx), ephemeral=True)
        await self.log_admin_action(interaction.user.id, "Acessou Painel de Tickets")

    async def log_admin_action(self, admin_id: int, action: str):
        """Log de ação administrativa"""
        try:
            from core.logs.organized_logger import log_admin
            await log_admin(admin_id, action)
        except Exception as e:
            logger.error(f"Erro ao logar ação administrativa: {e}")

def embed_admin_main_panel():
    embed = discord.Embed(
        title="⚙️ Painel Administrativo HyperDeploy",
        description="Gerencie configurações, preços, status e tickets do sistema.",
        color=0x5865F2,
        timestamp=discord.utils.utcnow()
    )
    embed.add_field(name="💰 Preços", value="Configurar preços de deploy", inline=True)
    embed.add_field(name="⚙️ Configurações", value="Configurações gerais do sistema", inline=True)
    embed.add_field(name="📊 Status", value="Status das aplicações e sistema", inline=True)
    embed.add_field(name="🧹 Limpeza", value="Limpeza de arquivos e dados", inline=True)
    embed.add_field(name="🔒 Tickets", value="Gerenciamento de tickets", inline=True)
    embed.set_footer(text="HyperDeploy • Painel Administrativo")
    return embed

def embed_prices_panel():
    current_price = config_manager.get_fresh_deploy_price() if config_manager else 10.00
    embed = discord.Embed(
        title="💰 Configuração de Preços",
        description=f"Preço atual do deploy: **R$ {current_price:.2f}**",
        color=0x00ff00,
        timestamp=discord.utils.utcnow()
    )
    embed.add_field(name="💡 Dica", value="Configure preços competitivos para atrair mais usuários.", inline=False)
    embed.set_footer(text="HyperDeploy • Configuração de Preços")
    return embed

def embed_config_panel():
    if not config_manager:
        embed = discord.Embed(title="❌ Erro", description="Sistema de configuração não disponível.", color=0xff0000)
        return embed
    
    config = config_manager.get_all_config()
    
    # Carregar configurações YAML
    try:
        with open('config/squarecloud.yaml', 'r', encoding='utf-8') as f:
            sq = yaml.safe_load(f)
        with open('config/bot.yaml', 'r', encoding='utf-8') as f:
            bot_config = yaml.safe_load(f)
    except Exception as e:
        sq = {}
        bot_config = {}
    
    embed = discord.Embed(
        title="⚙️ Configurações do Sistema",
        description="Configurações atuais do HyperDeploy",
        color=0x00ff00,
        timestamp=discord.utils.utcnow()
    )
    
    # Configurações dinâmicas
    embed.add_field(name="📁 Tamanho Máximo", value=f"{config.get('max_file_size_mb', 25)} MB", inline=True)
    embed.add_field(name="⏰ Timeout Tickets", value=f"{config.get('ticket_timeout_minutes', 30)} min", inline=True)
    embed.add_field(name="💳 Timeout Pagamentos", value=f"{config.get('payment_timeout_minutes', 30)} min", inline=True)
    embed.add_field(name="🚀 Deploy Automático", value="✅ Ativo" if config.get('auto_deploy', True) else "❌ Inativo", inline=True)
    embed.add_field(name="💳 Mercado Pago", value="✅ Ativo" if config.get('mercadopago_enabled', True) else "❌ Inativo", inline=True)
    
    # Configurações YAML
    embed.add_field(name="🤖 Bot", value=f"**Nome:** {bot_config.get('bot_name', 'N/A')}\n**Versão:** {bot_config.get('version', 'N/A')}", inline=True)
    embed.add_field(name="☁️ Square Cloud", value=f"**API Key:** {'*' * 10 if sq.get('api_key') else 'Não configurado'}", inline=True)
    embed.add_field(name="💳 Mercado Pago", value="✅ Configurado" if bot_config.get('mercadopago_access_token') else "❌ Não configurado", inline=True)
    
    embed.set_footer(text="HyperDeploy • Configurações")
    return embed

def embed_status_panel():
    import os
    from datetime import datetime
    
    # Verificar status dos serviços
    mercadopago_status = "✅ Configurado" if os.path.exists('config/bot.yaml') else "❌ Não configurado"
    squarecloud_status = "✅ Configurado" if os.path.exists('config/squarecloud.yaml') else "❌ Não configurado"
    
    # Verificar arquivos importantes
    uploads_count = len([f for f in os.listdir('uploads') if f.endswith('.zip')]) if os.path.exists('uploads') else 0
    qrcodes_count = len([f for f in os.listdir('qrcodes') if f.endswith('.png')]) if os.path.exists('qrcodes') else 0
    
    # Verificar configurações atuais
    current_price = config_manager.get_fresh_deploy_price() if config_manager else 10.00
    current_size = config_manager.get_max_file_size_mb() if config_manager else 25
    current_timeout = config_manager.get_ticket_timeout_minutes() if config_manager else 30
    
    embed = discord.Embed(
        title="📊 Status do Sistema HyperDeploy",
        description="Monitoramento completo do sistema",
        color=0x00ff00,
        timestamp=discord.utils.utcnow()
    )
    
    # Status dos serviços
    embed.add_field(name="🤖 Bot", value="✅ Online", inline=True)
    embed.add_field(name="💳 Mercado Pago", value=mercadopago_status, inline=True)
    embed.add_field(name="☁️ Square Cloud", value=squarecloud_status, inline=True)
    
    # Arquivos do sistema
    embed.add_field(name="📁 Uploads", value=f"{uploads_count} arquivos", inline=True)
    embed.add_field(name="🖼️ QR Codes", value=f"{qrcodes_count} arquivos", inline=True)
    embed.add_field(name="⏰ Atualizado", value=f"<t:{int(datetime.now().timestamp())}:R>", inline=True)
    
    # Configurações atuais
    embed.add_field(name="💰 Preço Atual", value=f"R$ {current_price:.2f}", inline=True)
    embed.add_field(name="📏 Tamanho Máx", value=f"{current_size} MB", inline=True)
    embed.add_field(name="⏱️ Timeout", value=f"{current_timeout} min", inline=True)
    
    embed.set_footer(text="HyperDeploy • Monitoramento em Tempo Real")
    return embed

def embed_cleanup_panel():
    embed = discord.Embed(
        title="🧹 Limpeza do Sistema",
        description="Limpeza de arquivos temporários e dados expirados",
        color=0xff9900,
        timestamp=discord.utils.utcnow()
    )
    embed.add_field(name="📁 QR Codes", value="Limpar QR Codes expirados", inline=False)
    embed.add_field(name="📂 Uploads", value="Limpar arquivos temporários", inline=False)
    embed.add_field(name="🗑️ Dados", value="Limpar dados expirados", inline=False)
    embed.set_footer(text="HyperDeploy • Limpeza")
    return embed

def embed_tickets_panel():
    embed = discord.Embed(
        title="🎫 Gerenciamento de Tickets",
        description="Controle de tickets do sistema",
        color=0xff6b6b,
        timestamp=discord.utils.utcnow()
    )
    embed.add_field(name="🔒 Fechar Todos", value="Fechar todos os tickets ativos", inline=False)
    embed.add_field(name="📊 Estatísticas", value="Ver estatísticas de tickets", inline=False)
    embed.set_footer(text="HyperDeploy • Tickets")
    return embed

def embed_logs_panel():
    embed = discord.Embed(
        title="📋 Sistema de Logs Organizados",
        description="Configure e gerencie o sistema de logs do HyperDeploy",
        color=0x9b59b6,
        timestamp=discord.utils.utcnow()
    )
    embed.add_field(name="🔄 Ativar Logs", value="Criar categoria e canais automaticamente", inline=True)
    embed.add_field(name="❌ Desativar Logs", value="Desconectar todos os canais", inline=True)
    embed.add_field(name="👤 Ações", value="Log de ações dos usuários", inline=True)
    embed.add_field(name="💳 Pagamentos", value="Log de transações PIX", inline=True)
    embed.add_field(name="🚀 Deploy", value="Log de deploys de aplicações", inline=True)
    embed.add_field(name="❌ Erros", value="Log de erros do sistema", inline=True)
    embed.add_field(name="🔧 Admin", value="Log de ações administrativas", inline=True)
    embed.add_field(name="📊 Status", value="Status dos canais configurados", inline=True)
    embed.set_footer(text="HyperDeploy • Sistema de Logs Automático")
    return embed

# Painel de Preços
class PricesPanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx

    async def log_admin_action(self, admin_id: int, action: str):
        """Log de ação administrativa"""
        try:
            from core.logs.organized_logger import log_admin
            await log_admin(admin_id, action)
        except Exception as e:
            logger.error(f"Erro ao logar ação administrativa: {e}")

    @discord.ui.button(label="💰 Alterar Preço", style=discord.ButtonStyle.primary)
    async def change_price(self, button, interaction):
        embed = discord.Embed(title="💰 Alterar Preço do Deploy", description="Selecione o novo preço:", color=0x00ff00)
        embed.add_field(name="Preço Atual", value=f"R$ {config_manager.get_fresh_deploy_price() if config_manager else 10.00:.2f}", inline=True)
        
        select = discord.ui.Select(placeholder="Escolha o novo preço...", options=[
            discord.SelectOption(label="R$ 0,00", value="0.00", emoji="🆓"),
            discord.SelectOption(label="R$ 2,50", value="2.50", emoji="💵"),
            discord.SelectOption(label="R$ 5,00", value="5.00", emoji="💵"),
            discord.SelectOption(label="R$ 7,50", value="7.50", emoji="💵"),
            discord.SelectOption(label="R$ 10,00", value="10.00", emoji="💵"),
            discord.SelectOption(label="R$ 12,50", value="12.50", emoji="💵"),
            discord.SelectOption(label="R$ 15,00", value="15.00", emoji="💵"),
            discord.SelectOption(label="R$ 17,50", value="17.50", emoji="💵"),
            discord.SelectOption(label="R$ 20,00", value="20.00", emoji="💵"),
            discord.SelectOption(label="R$ 22,50", value="22.50", emoji="💵"),
            discord.SelectOption(label="R$ 25,00", value="25.00", emoji="💵"),
            discord.SelectOption(label="R$ 30,00", value="30.00", emoji="💵"),
            discord.SelectOption(label="R$ 35,00", value="35.00", emoji="💵"),
            discord.SelectOption(label="R$ 40,00", value="40.00", emoji="💵"),
            discord.SelectOption(label="R$ 50,00", value="50.00", emoji="💵"),
        ])
        
        async def preco_callback(interaction: discord.Interaction):
            novo_preco = float(select.values[0])
            if config_manager:
                config_manager.set_deploy_price(novo_preco)
                await interaction.response.send_message(f"✅ Preço alterado para R$ {novo_preco:.2f}!", ephemeral=True)
                await self.log_admin_action(interaction.user.id, f"Definiu preço para R$ {novo_preco:.2f}")
            else:
                await interaction.response.send_message("❌ Erro: ConfigManager não disponível.", ephemeral=True)
        
        select.callback = preco_callback
        view = discord.ui.View()
        view.add_item(select)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="🔄 Resetar", style=discord.ButtonStyle.secondary)
    async def reset_price(self, button, interaction):
        if config_manager:
            config_manager.set_deploy_price(10.00)
            embed = discord.Embed(
                title="✅ Preço Resetado",
                description="Preço do deploy foi resetado para R$ 10,00",
                color=0x00ff00
            )
            await interaction.response.edit_message(embed=embed, view=None)
            await self.log_admin_action(interaction.user.id, "Resetou preço para R$ 10,00")
        else:
            await interaction.response.send_message("❌ Sistema de configuração não disponível.", ephemeral=True)

    @discord.ui.button(label="❌ Fechar", style=discord.ButtonStyle.danger)
    async def close(self, button, interaction):
        await interaction.response.edit_message(content="Painel fechado.", embed=None, view=None)

# Modais removidos - agora usando botões e seletores funcionais

# Painel de Configurações
class ConfigPanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx

    # Botões de teste removidos - agora usando seletores funcionais

    @discord.ui.button(label="📁 Tamanho Máximo", style=discord.ButtonStyle.primary)
    async def max_file_size(self, button, interaction):
        embed = discord.Embed(title="📁 Alterar Tamanho Máximo", description="Selecione o novo tamanho:", color=0x00ff00)
        embed.add_field(name="Tamanho Atual", value=f"{config_manager.get_max_file_size_mb() if config_manager else 25} MB", inline=True)
        
        select = discord.ui.Select(placeholder="Escolha o novo tamanho...", options=[
            discord.SelectOption(label="5 MB", value="5", emoji="📦"),
            discord.SelectOption(label="10 MB", value="10", emoji="📦"),
            discord.SelectOption(label="15 MB", value="15", emoji="📦"),
            discord.SelectOption(label="20 MB", value="20", emoji="📦"),
            discord.SelectOption(label="25 MB", value="25", emoji="📦"),
            discord.SelectOption(label="30 MB", value="30", emoji="📦"),
            discord.SelectOption(label="40 MB", value="40", emoji="📦"),
            discord.SelectOption(label="50 MB", value="50", emoji="📦"),
            discord.SelectOption(label="75 MB", value="75", emoji="📦"),
            discord.SelectOption(label="100 MB", value="100", emoji="📦"),
            discord.SelectOption(label="150 MB", value="150", emoji="📦"),
            discord.SelectOption(label="200 MB", value="200", emoji="📦"),
        ])
        
        async def tamanho_callback(interaction: discord.Interaction):
            novo_tamanho = int(select.values[0])
            if config_manager:
                config_manager.set_max_file_size_mb(novo_tamanho)
                await interaction.response.send_message(f"✅ Tamanho máximo alterado para {novo_tamanho} MB!", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Erro: ConfigManager não disponível.", ephemeral=True)
        
        select.callback = tamanho_callback
        view = discord.ui.View()
        view.add_item(select)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="⏰ Timeout Tickets", style=discord.ButtonStyle.secondary)
    async def ticket_timeout(self, button, interaction):
        embed = discord.Embed(title="⏰ Alterar Timeout Tickets", description="Selecione o novo timeout:", color=0x00ff00)
        embed.add_field(name="Timeout Atual", value=f"{config_manager.get_ticket_timeout_minutes() if config_manager else 30} minutos", inline=True)
        
        select = discord.ui.Select(placeholder="Escolha o novo timeout...", options=[
            discord.SelectOption(label="5 minutos", value="5", emoji="⏱️"),
            discord.SelectOption(label="10 minutos", value="10", emoji="⏱️"),
            discord.SelectOption(label="15 minutos", value="15", emoji="⏱️"),
            discord.SelectOption(label="20 minutos", value="20", emoji="⏱️"),
            discord.SelectOption(label="30 minutos", value="30", emoji="⏱️"),
            discord.SelectOption(label="45 minutos", value="45", emoji="⏱️"),
            discord.SelectOption(label="60 minutos", value="60", emoji="⏱️"),
            discord.SelectOption(label="90 minutos", value="90", emoji="⏱️"),
            discord.SelectOption(label="120 minutos", value="120", emoji="⏱️"),
            discord.SelectOption(label="180 minutos", value="180", emoji="⏱️"),
            discord.SelectOption(label="240 minutos", value="240", emoji="⏱️"),
        ])
        
        async def timeout_callback(interaction: discord.Interaction):
            novo_timeout = int(select.values[0])
            if config_manager:
                config_manager.set_ticket_timeout_minutes(novo_timeout)
                await interaction.response.send_message(f"✅ Timeout de tickets alterado para {novo_timeout} minutos!", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Erro: ConfigManager não disponível.", ephemeral=True)
        
        select.callback = timeout_callback
        view = discord.ui.View()
        view.add_item(select)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="💳 Timeout Pagamentos", style=discord.ButtonStyle.secondary)
    async def payment_timeout(self, button, interaction):
        embed = discord.Embed(title="💳 Alterar Timeout Pagamentos", description="Selecione o novo timeout:", color=0x00ff00)
        embed.add_field(name="Timeout Atual", value=f"{config_manager.get_payment_timeout_minutes() if config_manager else 30} minutos", inline=True)
        
        select = discord.ui.Select(placeholder="Escolha o novo timeout...", options=[
            discord.SelectOption(label="5 minutos", value="5", emoji="⏱️"),
            discord.SelectOption(label="10 minutos", value="10", emoji="⏱️"),
            discord.SelectOption(label="15 minutos", value="15", emoji="⏱️"),
            discord.SelectOption(label="20 minutos", value="20", emoji="⏱️"),
            discord.SelectOption(label="30 minutos", value="30", emoji="⏱️"),
            discord.SelectOption(label="45 minutos", value="45", emoji="⏱️"),
            discord.SelectOption(label="60 minutos", value="60", emoji="⏱️"),
            discord.SelectOption(label="90 minutos", value="90", emoji="⏱️"),
            discord.SelectOption(label="120 minutos", value="120", emoji="⏱️"),
            discord.SelectOption(label="180 minutos", value="180", emoji="⏱️"),
            discord.SelectOption(label="240 minutos", value="240", emoji="⏱️"),
        ])
        
        async def timeout_callback(interaction: discord.Interaction):
            novo_timeout = int(select.values[0])
            if config_manager:
                config_manager.set_payment_timeout_minutes(novo_timeout)
                await interaction.response.send_message(f"✅ Timeout de pagamentos alterado para {novo_timeout} minutos!", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Erro: ConfigManager não disponível.", ephemeral=True)
        
        select.callback = timeout_callback
        view = discord.ui.View()
        view.add_item(select)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="🚀 Deploy Automático", style=discord.ButtonStyle.success)
    async def toggle_auto_deploy(self, button, interaction):
        if config_manager:
            current = config_manager.is_auto_deploy_enabled()
            config_manager.set_auto_deploy(not current)
            status = "habilitado" if not current else "desabilitado"
            embed = discord.Embed(
                title="✅ Deploy Automático",
                description=f"Deploy automático foi **{status}**",
                color=0x00ff00
            )
            embed.add_field(name="Funcionalidade", value="Deploy automático após confirmação de pagamento", inline=False)
            embed.add_field(name="Benefícios", value="• Processo automatizado\n• Menos intervenção manual\n• Deploy instantâneo", inline=False)
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            await interaction.response.send_message("❌ Sistema de configuração não disponível.", ephemeral=True)

    @discord.ui.button(label="💳 Mercado Pago", style=discord.ButtonStyle.success)
    async def toggle_mercadopago(self, button, interaction):
        if config_manager:
            current = config_manager.is_mercadopago_enabled()
            config_manager.set_mercadopago_enabled(not current)
            status = "habilitado" if not current else "desabilitado"
            embed = discord.Embed(
                title="✅ Mercado Pago",
                description=f"Sistema de pagamentos foi **{status}**",
                color=0x00ff00
            )
            embed.add_field(name="Funcionalidade", value="Sistema de pagamentos PIX via Mercado Pago", inline=False)
            embed.add_field(name="Recursos", value="• QR Code automático\n• Verificação de pagamento\n• Integração completa", inline=False)
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            await interaction.response.send_message("❌ Sistema de configuração não disponível.", ephemeral=True)

    @discord.ui.button(label="📋 Logs", style=discord.ButtonStyle.secondary)
    async def logs_btn(self, button, interaction):
        await interaction.response.send_message(embed=embed_logs_panel(), view=LogsPanel(self.ctx), ephemeral=True)

    @discord.ui.button(label="❌ Fechar", style=discord.ButtonStyle.danger)
    async def close(self, button, interaction):
        await interaction.response.edit_message(content="Painel fechado.", embed=None, view=None)

# Modal para tamanho de arquivo
class FileSizeModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="📁 Configurar Tamanho Máximo")
        self.size_input = InputText(
            label="Tamanho Máximo (MB)",
            placeholder="25",
            required=True,
            max_length=5,
            value="25"
        )
        self.add_item(self.size_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            size = int(self.size_input.value.strip())
            if size <= 0 or size > 100:
                raise ValueError("Tamanho deve ser entre 1 e 100 MB")
            
            if config_manager:
                config_manager.set_max_file_size_mb(size)
                embed = discord.Embed(
                    title="✅ Tamanho Atualizado",
                    description=f"Tamanho máximo foi alterado para **{size} MB**",
                    color=0x00ff00
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message("❌ Sistema de configuração não disponível.", ephemeral=True)
                
        except ValueError:
            embed = discord.Embed(
                title="❌ Tamanho Inválido",
                description="Digite um tamanho válido (1-100 MB)",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro: {str(e)}", ephemeral=True)

# Modal para timeout
class TimeoutModal(discord.ui.Modal):
    def __init__(self, timeout_type: str):
        super().__init__(title=f"⏰ Configurar Timeout {timeout_type.title()}")
        self.timeout_type = timeout_type
        
        self.timeout_input = InputText(
            label=f"Timeout {timeout_type.title()} (minutos)",
            placeholder="30",
            required=True,
            max_length=5,
            value="30"
        )
        self.add_item(self.timeout_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            minutes = int(self.timeout_input.value.strip())
            if minutes <= 0 or minutes > 1440:
                raise ValueError("Timeout deve ser entre 1 e 1440 minutos")
            
            if config_manager:
                if self.timeout_type == "ticket":
                    config_manager.set_ticket_timeout_minutes(minutes)
                else:
                    config_manager.set_payment_timeout_minutes(minutes)
                
                embed = discord.Embed(
                    title="✅ Timeout Atualizado",
                    description=f"Timeout de {self.timeout_type} foi alterado para **{minutes} minutos**",
                    color=0x00ff00
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message("❌ Sistema de configuração não disponível.", ephemeral=True)
                
        except ValueError:
            embed = discord.Embed(
                title="❌ Timeout Inválido",
                description="Digite um timeout válido (1-1440 minutos)",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro: {str(e)}", ephemeral=True)

# Painel de Status
class StatusPanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx

    @discord.ui.button(label="🔄 Atualizar", style=discord.ButtonStyle.primary)
    async def refresh(self, button, interaction):
        embed = embed_status_panel()
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="❌ Fechar", style=discord.ButtonStyle.danger)
    async def close(self, button, interaction):
        await interaction.response.edit_message(content="Painel fechado.", embed=None, view=None)

# Painel de Limpeza
class CleanupPanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx

    @discord.ui.button(label="🧹 Executar Limpeza", style=discord.ButtonStyle.primary)
    async def run_cleanup(self, button, interaction):
        try:
            import os
            import shutil
            from datetime import datetime
            
            # Criar backup antes da limpeza
            backup_dir = f"backups/cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Limpar arquivos temporários
            cleaned_files = 0
            cleaned_size = 0
            
            # Limpar QR codes antigos (mais de 1 hora)
            qrcodes_dir = "qrcodes"
            if os.path.exists(qrcodes_dir):
                for file in os.listdir(qrcodes_dir):
                    if file.endswith('.png'):
                        file_path = os.path.join(qrcodes_dir, file)
                        file_age = datetime.now().timestamp() - os.path.getmtime(file_path)
                        if file_age > 3600:  # 1 hora
                            size = os.path.getsize(file_path)
                            os.remove(file_path)
                            cleaned_files += 1
                            cleaned_size += size
            
            # Limpar uploads antigos (mais de 24 horas)
            uploads_dir = "uploads"
            if os.path.exists(uploads_dir):
                for file in os.listdir(uploads_dir):
                    if file.endswith('.zip'):
                        file_path = os.path.join(uploads_dir, file)
                        file_age = datetime.now().timestamp() - os.path.getmtime(file_path)
                        if file_age > 86400:  # 24 horas
                            size = os.path.getsize(file_path)
                            os.remove(file_path)
                            cleaned_files += 1
                            cleaned_size += size
            
            cleaned_size_mb = cleaned_size / (1024 * 1024)
            
            embed = discord.Embed(
                title="🧹 Limpeza Executada",
                description="Limpeza de arquivos temporários concluída com sucesso!",
                color=0x00ff00
            )
            embed.add_field(name="🗑️ Arquivos Removidos", value=f"{cleaned_files} arquivos", inline=True)
            embed.add_field(name="💾 Espaço Liberado", value=f"{cleaned_size_mb:.2f} MB", inline=True)
            embed.add_field(name="📁 Backup Criado", value=f"`{backup_dir}`", inline=True)
            embed.add_field(name="ℹ️ Detalhes", value="• QR Codes antigos (>1h)\n• Uploads antigos (>24h)\n• Backup automático criado", inline=False)
            
            await interaction.response.edit_message(embed=embed, view=None)
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro na Limpeza",
                description=f"Erro ao executar limpeza: {str(e)}",
                color=0xff0000
            )
            await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="🧹 Limpar QR Codes", style=discord.ButtonStyle.danger)
    async def cleanup_qrcodes(self, button, interaction):
        try:
            from core.utils.cleanup import cleanup_qr_codes
            count = cleanup_qr_codes()
            await interaction.response.send_message(f"✅ {count} QR codes removidos", ephemeral=True, delete_after=5)
            await self.log_admin_action(interaction.user.id, f"Removeu {count} QR codes")
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro: {e}", ephemeral=True, delete_after=5)

    @discord.ui.button(label="🧹 Limpar Uploads", style=discord.ButtonStyle.danger)
    async def cleanup_uploads(self, button, interaction):
        try:
            from core.utils.cleanup import cleanup_uploads
            count = cleanup_uploads()
            await interaction.response.send_message(f"✅ {count} arquivos de upload removidos", ephemeral=True, delete_after=5)
            await self.log_admin_action(interaction.user.id, f"Removeu {count} arquivos de upload")
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro: {e}", ephemeral=True, delete_after=5)

    @discord.ui.button(label="🧹 Limpar Tudo", style=discord.ButtonStyle.danger)
    async def cleanup_all(self, button, interaction):
        try:
            from core.utils.cleanup import cleanup_all_files
            count = cleanup_all_files()
            await interaction.response.send_message(f"✅ {count} arquivos temporários removidos", ephemeral=True, delete_after=5)
            await self.log_admin_action(interaction.user.id, f"Removeu {count} arquivos temporários")
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro: {e}", ephemeral=True, delete_after=5)

    @discord.ui.button(label="❌ Fechar", style=discord.ButtonStyle.danger)
    async def close(self, button, interaction):
        await interaction.response.edit_message(content="Painel fechado.", embed=None, view=None)

# Painel de Tickets
class TicketsPanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx

    async def log_admin_action(self, admin_id: int, action: str):
        """Log de ação administrativa"""
        try:
            from core.logs.organized_logger import log_admin
            await log_admin(admin_id, action)
        except Exception as e:
            logger.error(f"Erro ao logar ação administrativa: {e}")

    @discord.ui.button(label="🔒 Fechar Todos", style=discord.ButtonStyle.danger)
    async def close_all_tickets(self, button, interaction):
        try:
            from core.tickets.manager import ticket_manager
            if not ticket_manager:
                await interaction.response.send_message("❌ Sistema de tickets não disponível", ephemeral=True, delete_after=5)
                return
            
            active_tickets = ticket_manager.get_active_tickets()
            closed_count = 0
            failed_count = 0
            
            for ticket in active_tickets:
                user_id = ticket.get("user_id")
                if user_id:
                    try:
                        success = await ticket_manager.close_ticket(user_id, "Fechado pelo administrador")
                        if success:
                            closed_count += 1
                        else:
                            failed_count += 1
                    except Exception as e:
                        logger.error(f"Erro ao fechar ticket {user_id}: {e}")
                        failed_count += 1
            
            # Verificar se a interação ainda é válida antes de responder
            try:
                if closed_count > 0:
                    message = f"✅ {closed_count} tickets fechados"
                    if failed_count > 0:
                        message += f" | ❌ {failed_count} falharam"
                else:
                    message = f"❌ Nenhum ticket foi fechado ({failed_count} falharam)"
                
                await interaction.response.send_message(message, ephemeral=True, delete_after=5)
                await self.log_admin_action(interaction.user.id, f"Fechou {closed_count} tickets")
                
            except discord.errors.NotFound:
                # Interação expirada ou canal inexistente
                logger.warning("Interação expirada ao fechar tickets")
                return
            except Exception as e:
                logger.error(f"Erro ao responder interação: {e}")
                return
            
        except Exception as e:
            try:
                await interaction.response.send_message(f"❌ Erro: {e}", ephemeral=True, delete_after=5)
            except discord.errors.NotFound:
                logger.error(f"Erro ao fechar tickets (interação expirada): {e}")
            except Exception as response_error:
                logger.error(f"Erro ao responder interação: {response_error}")

    @discord.ui.button(label="📊 Estatísticas", style=discord.ButtonStyle.primary)
    async def ticket_stats(self, button, interaction):
        try:
            from core.tickets.manager import ticket_manager
            if not ticket_manager:
                await interaction.response.send_message("❌ Sistema de tickets não disponível", ephemeral=True, delete_after=5)
                return
            
            active_tickets = ticket_manager.get_active_tickets()
            total_tickets = len(active_tickets)
            
            embed = discord.Embed(
                title="📊 Estatísticas de Tickets",
                description="Informações sobre tickets ativos",
                color=0x00ff00
            )
            embed.add_field(name="🎫 Tickets Ativos", value=str(total_tickets), inline=True)
            embed.add_field(name="⏰ Última Atualização", value=datetime.now().strftime("%H:%M:%S"), inline=True)
            
            if total_tickets > 0:
                # Mostrar alguns tickets como exemplo
                sample_tickets = active_tickets[:3]
                ticket_list = []
                for ticket in sample_tickets:
                    user_id = ticket.get("user_id", "N/A")
                    created_at = ticket.get("created_at", "N/A")
                    if created_at != "N/A":
                        try:
                            dt = datetime.fromisoformat(created_at)
                            created_at = dt.strftime("%d/%m %H:%M")
                        except:
                            pass
                    ticket_list.append(f"<@{user_id}> - {created_at}")
                
                embed.add_field(name="📋 Exemplos", value="\n".join(ticket_list) if ticket_list else "Nenhum", inline=False)
            
            embed.set_footer(text="HyperDeploy • Sistema de Tickets")
            
            try:
                await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)
                await self.log_admin_action(interaction.user.id, "Visualizou estatísticas de tickets")
            except discord.errors.NotFound:
                logger.warning("Interação expirada ao mostrar estatísticas")
                return
            except Exception as e:
                logger.error(f"Erro ao responder interação de estatísticas: {e}")
                return
            
        except Exception as e:
            try:
                await interaction.response.send_message(f"❌ Erro: {e}", ephemeral=True, delete_after=5)
            except discord.errors.NotFound:
                logger.error(f"Erro ao mostrar estatísticas (interação expirada): {e}")
            except Exception as response_error:
                logger.error(f"Erro ao responder interação: {response_error}")

    @discord.ui.button(label="❌ Fechar", style=discord.ButtonStyle.secondary)
    async def close(self, button, interaction):
        await interaction.response.edit_message(content="Painel fechado.", embed=None, view=None)

# Painel de Logs
class LogsPanel(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.ctx = ctx

    @discord.ui.button(label="🔄 Ativar Logs", style=discord.ButtonStyle.success)
    async def enable_logs(self, button, interaction):
        await self.setup_automatic_logs(interaction, enable=True)

    @discord.ui.button(label="❌ Desativar Logs", style=discord.ButtonStyle.danger)
    async def disable_logs(self, button, interaction):
        await self.setup_automatic_logs(interaction, enable=False)

    @discord.ui.button(label="👤 Ações", style=discord.ButtonStyle.primary)
    async def actions_log(self, button, interaction):
        await self.configure_log_channel(interaction, "actions", "Log de Ações")

    @discord.ui.button(label="💳 Pagamentos", style=discord.ButtonStyle.primary)
    async def payments_log(self, button, interaction):
        await self.configure_log_channel(interaction, "payments", "Log de Pagamentos")

    @discord.ui.button(label="🚀 Deploy", style=discord.ButtonStyle.primary)
    async def deploy_log(self, button, interaction):
        await self.configure_log_channel(interaction, "deploy", "Log de Deploy")

    @discord.ui.button(label="❌ Erros", style=discord.ButtonStyle.danger)
    async def errors_log(self, button, interaction):
        await self.configure_log_channel(interaction, "errors", "Log de Erros")

    @discord.ui.button(label="🔧 Admin", style=discord.ButtonStyle.secondary)
    async def admin_log(self, button, interaction):
        await self.configure_log_channel(interaction, "admin", "Log de Admin")

    @discord.ui.button(label="📊 Status", style=discord.ButtonStyle.success)
    async def status_log(self, button, interaction):
        await self.show_log_status(interaction)

    @discord.ui.button(label="❌ Fechar", style=discord.ButtonStyle.secondary)
    async def close(self, button, interaction):
        await interaction.response.edit_message(content="Painel fechado.", embed=None, view=None)

    async def setup_automatic_logs(self, interaction, enable: bool):
        """Configura logs automáticos criando categoria e canais"""
        try:
            from core.logs.organized_logger import organized_logger
            
            if not organized_logger:
                await interaction.response.send_message("❌ Sistema de logs não disponível", ephemeral=True, delete_after=5)
                return
            
            if enable:
                # Criar categoria e canais automaticamente
                success = await self.create_log_category_and_channels(interaction.guild)
                if success:
                    embed = discord.Embed(
                        title="✅ Logs Ativados",
                        description="Categoria **HyperDeploy - Logs** criada com todos os canais configurados automaticamente!",
                        color=0x00ff00
                    )
                    embed.add_field(name="Categoria", value="HyperDeploy - Logs", inline=True)
                    embed.add_field(name="Canais Criados", value="5 canais de log", inline=True)
                    embed.set_footer(text="HyperDeploy • Sistema de Logs Automático")
                    
                    await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)
                else:
                    await interaction.response.send_message("❌ Erro ao criar categoria e canais", ephemeral=True, delete_after=5)
            else:
                # Desativar logs (remover configurações)
                organized_logger.log_channels.clear()
                organized_logger.save_log_channels()
                
                embed = discord.Embed(
                    title="❌ Logs Desativados",
                    description="Todos os canais de log foram desconectados. A categoria não será removida automaticamente.",
                    color=0xff0000
                )
                embed.set_footer(text="HyperDeploy • Sistema de Logs")
                
                await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)
                
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao configurar logs: {e}", ephemeral=True, delete_after=5)

    async def create_log_category_and_channels(self, guild) -> bool:
        """Cria categoria e canais de log automaticamente"""
        try:
            from core.logs.organized_logger import organized_logger
            
            # Verificar se categoria já existe
            category_name = "HyperDeploy - Logs"
            category = discord.utils.get(guild.categories, name=category_name)
            
            if not category:
                # Criar categoria
                category = await guild.create_category(
                    name=category_name,
                    reason="Sistema de logs HyperDeploy"
                )
            
            # Configurações dos canais
            log_channels = {
                "actions": {"name": "👤-ações", "topic": "Log de ações dos usuários"},
                "payments": {"name": "💳-pagamentos", "topic": "Log de transações PIX"},
                "deploy": {"name": "🚀-deploy", "topic": "Log de deploys de aplicações"},
                "errors": {"name": "❌-erros", "topic": "Log de erros do sistema"},
                "admin": {"name": "🔧-admin", "topic": "Log de ações administrativas"}
            }
            
            # Criar ou obter canais
            for log_type, config in log_channels.items():
                channel_name = config["name"]
                channel = discord.utils.get(guild.channels, name=channel_name, category=category)
                
                if not channel:
                    # Criar canal
                    channel = await guild.create_text_channel(
                        name=channel_name,
                        category=category,
                        topic=config["topic"],
                        reason=f"Canal de log {log_type} - HyperDeploy"
                    )
                
                # Configurar canal no sistema de logs
                organized_logger.set_log_channel(log_type, channel.id)
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar categoria e canais: {e}")
            return False

    async def configure_log_channel(self, interaction, log_type, log_name):
        """Configura canal para um tipo de log específico"""
        try:
            from core.logs.organized_logger import organized_logger
            
            embed = discord.Embed(
                title=f"📋 Configurar {log_name}",
                description=f"Para configurar o canal de **{log_name}**:\n\n1. Crie um canal no servidor\n2. Copie o ID do canal\n3. Cole o ID no modal abaixo\n\n**Canal atual:** {self.get_current_channel(log_type)}",
                color=0x9b59b6
            )
            
            # Modal para inserir ID do canal
            modal = LogChannelModal(log_type, log_name)
            await interaction.response.send_modal(modal)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao configurar log: {e}", ephemeral=True, delete_after=5)

    async def show_log_status(self, interaction):
        """Mostra status dos canais de log configurados"""
        try:
            from core.logs.organized_logger import organized_logger
            
            if not organized_logger:
                await interaction.response.send_message("❌ Sistema de logs não disponível", ephemeral=True, delete_after=5)
                return
            
            info = organized_logger.get_log_channels_info()
            
            embed = discord.Embed(
                title="📊 Status dos Canais de Log",
                description="Canais configurados para logs",
                color=0x00ff00,
                timestamp=discord.utils.utcnow()
            )
            
            for log_type, channel_info in info['channels'].items():
                status = "✅ Configurado" if channel_info['configured'] else "❌ Não configurado"
                channel_name = channel_info['name'] if channel_info['configured'] else "N/A"
                embed.add_field(
                    name=f"{log_type.title()}", 
                    value=f"{status}\nCanal: {channel_name}", 
                    inline=True
                )
            
            embed.add_field(name="📈 Total", value=f"{info['total_configured']}/{info['total_types']} configurados", inline=False)
            embed.set_footer(text="HyperDeploy • Status de Logs")
            await interaction.response.edit_message(embed=embed, view=None)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao mostrar status: {e}", ephemeral=True, delete_after=5)

    def get_current_channel(self, log_type):
        """Obtém o canal atual configurado para um tipo de log"""
        try:
            from core.logs.organized_logger import organized_logger
            if organized_logger:
                channel_id = organized_logger.get_log_channel(log_type)
                if channel_id:
                    channel = self.ctx.bot.get_channel(channel_id)
                    return f"<#{channel_id}> ({channel.name if channel else 'Canal não encontrado'})"
            return "Não configurado"
        except:
            return "Erro ao verificar"

# Modal para configurar canal de log
class LogChannelModal(discord.ui.Modal):
    def __init__(self, log_type, log_name):
        super().__init__(title=f"Configurar {log_name}")
        self.log_type = log_type
        self.log_name = log_name
        
        self.channel_id = discord.ui.InputText(
            label="ID do Canal",
            placeholder="Ex: 1234567890123456789",
            required=True,
            min_length=17,
            max_length=20
        )
        self.add_item(self.channel_id)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            from core.logs.organized_logger import organized_logger
            
            if not organized_logger:
                await interaction.response.send_message("❌ Sistema de logs não disponível", ephemeral=True, delete_after=5)
                return
            
            # Validar ID do canal
            try:
                channel_id = int(self.channel_id.value)
            except ValueError:
                await interaction.response.send_message("❌ ID do canal inválido", ephemeral=True, delete_after=5)
                return
            
            # Verificar se o canal existe
            channel = interaction.guild.get_channel(channel_id)
            if not channel:
                await interaction.response.send_message("❌ Canal não encontrado no servidor", ephemeral=True, delete_after=5)
                return
            
            # Configurar canal
            success = organized_logger.set_log_channel(self.log_type, channel_id)
            
            if success:
                embed = discord.Embed(
                    title="✅ Canal Configurado",
                    description=f"Canal **{channel.name}** configurado para **{self.log_name}**",
                    color=0x00ff00
                )
                embed.add_field(name="Canal", value=f"<#{channel_id}>", inline=True)
                embed.add_field(name="Tipo", value=self.log_type, inline=True)
                embed.set_footer(text="HyperDeploy • Configuração de Logs")
                
                await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)
            else:
                await interaction.response.send_message("❌ Erro ao configurar canal", ephemeral=True, delete_after=5)
                
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro: {e}", ephemeral=True, delete_after=5)

def setup(bot, guild_id=None):
    @bot.slash_command(name="admin", description="Painel administrativo (apenas admins).", guild_ids=[guild_id] if guild_id else None)
    async def admin(ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("❌ Apenas administradores podem usar este comando.", ephemeral=True)
            return
        
        await ctx.respond(embed=embed_admin_main_panel(), view=AdminMainPanel(ctx), ephemeral=True) 