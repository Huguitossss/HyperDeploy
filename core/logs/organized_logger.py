import discord
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
from core.logs.logger import logger

class OrganizedLogger:
    def __init__(self, bot):
        self.bot = bot
        self.log_channels_file = "data/log_channels.json"
        self.log_channels: Dict[str, int] = {}
        self.load_log_channels()
    
    def load_log_channels(self):
        """Carrega configuração dos canais de log"""
        try:
            if os.path.exists(self.log_channels_file):
                with open(self.log_channels_file, 'r', encoding='utf-8') as f:
                    self.log_channels = json.load(f)
            else:
                self.save_log_channels()
        except Exception as e:
            logger.error(f"Erro ao carregar canais de log: {e}")
            self.log_channels = {}
    
    def save_log_channels(self):
        """Salva configuração dos canais de log"""
        try:
            os.makedirs(os.path.dirname(self.log_channels_file), exist_ok=True)
            with open(self.log_channels_file, 'w', encoding='utf-8') as f:
                json.dump(self.log_channels, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao salvar canais de log: {e}")
    
    def set_log_channel(self, log_type: str, channel_id: int) -> bool:
        """Define um canal para um tipo específico de log"""
        try:
            self.log_channels[log_type] = channel_id
            self.save_log_channels()
            logger.info(f"📋 Canal de log '{log_type}' configurado: {channel_id}")
            return True
        except Exception as e:
            logger.error(f"Erro ao configurar canal de log: {e}")
            return False
    
    def get_log_channel(self, log_type: str) -> Optional[int]:
        """Obtém o ID do canal para um tipo de log"""
        return self.log_channels.get(log_type)
    
    async def send_log(self, log_type: str, embed: discord.Embed, content: str = None) -> bool:
        """Envia log para o canal apropriado"""
        try:
            channel_id = self.get_log_channel(log_type)
            if not channel_id:
                logger.warning(f"⚠️ Canal de log '{log_type}' não configurado")
                return False
            
            channel = self.bot.get_channel(channel_id)
            if not channel:
                logger.error(f"❌ Canal de log não encontrado: {channel_id}")
                return False
            
            # Enviar mensagem
            if content:
                await channel.send(content=content, embed=embed)
            else:
                await channel.send(embed=embed)
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar log: {e}")
            return False
    
    async def log_action(self, user_id: int, action: str, details: str = None, success: bool = True):
        """Log de ações dos usuários"""
        try:
            user = self.bot.get_user(user_id)
            username = user.name if user else f"User {user_id}"
            
            embed = discord.Embed(
                title="👤 Ação do Usuário",
                description=f"**Usuário:** {username} (`{user_id}`)\n**Ação:** {action}",
                color=0x00ff00 if success else 0xff0000,
                timestamp=datetime.now()
            )
            
            if details:
                embed.add_field(name="📝 Detalhes", value=details, inline=False)
            
            embed.add_field(name="✅ Status", value="Sucesso" if success else "Falha", inline=True)
            embed.set_footer(text="HyperDeploy • Log de Ações")
            
            await self.send_log("actions", embed)
            
        except Exception as e:
            logger.error(f"Erro ao logar ação: {e}")
    
    async def log_admin(self, admin_id: int, action: str, details: str = None, target: str = None):
        """Log de ações administrativas"""
        try:
            admin = self.bot.get_user(admin_id)
            admin_name = admin.name if admin else f"Admin {admin_id}"
            
            embed = discord.Embed(
                title="👑 Ação Administrativa",
                description=f"**Administrador:** {admin_name} (`{admin_id}`)\n**Ação:** {action}",
                color=0x9b59b6,
                timestamp=datetime.now()
            )
            
            if details:
                embed.add_field(name="📝 Detalhes", value=details, inline=False)
            
            if target:
                embed.add_field(name="🎯 Alvo", value=target, inline=True)
            
            embed.set_footer(text="HyperDeploy • Log Administrativo")
            
            await self.send_log("admin", embed)
            
        except Exception as e:
            logger.error(f"Erro ao logar ação administrativa: {e}")
    
    async def log_payment(self, user_id: int, payment_id: str, amount: float, status: str, details: str = None):
        """Log de pagamentos"""
        try:
            user = self.bot.get_user(user_id)
            username = user.name if user else f"User {user_id}"
            
            # Cores baseadas no status
            color_map = {
                "pending": 0xffff00,
                "paid": 0x00ff00,
                "expired": 0xff0000,
                "failed": 0xff0000,
                "processing": 0x0099ff
            }
            color = color_map.get(status, 0x808080)
            
            embed = discord.Embed(
                title="💳 Pagamento Processado",
                description=f"**Usuário:** {username} (`{user_id}`)\n**ID:** `{payment_id}`\n**Valor:** R$ {amount:.2f}",
                color=color,
                timestamp=datetime.now()
            )
            
            embed.add_field(name="📊 Status", value=status.upper(), inline=True)
            
            if details:
                embed.add_field(name="📝 Detalhes", value=details, inline=False)
            
            embed.set_footer(text="HyperDeploy • Log de Pagamentos")
            
            await self.send_log("payments", embed)
            
        except Exception as e:
            logger.error(f"Erro ao logar pagamento: {e}")
    
    async def log_deploy(self, user_id: int, app_id: str, app_name: str, status: str, details: str = None):
        """Log de deploys"""
        try:
            user = self.bot.get_user(user_id)
            username = user.name if user else f"User {user_id}"
            
            # Cores baseadas no status
            color_map = {
                "started": 0x0099ff,
                "success": 0x00ff00,
                "failed": 0xff0000,
                "processing": 0xffff00
            }
            color = color_map.get(status, 0x808080)
            
            embed = discord.Embed(
                title="🚀 Deploy Realizado",
                description=f"**Usuário:** {username} (`{user_id}`)\n**Aplicação:** {app_name}\n**ID:** `{app_id}`",
                color=color,
                timestamp=datetime.now()
            )
            
            embed.add_field(name="📊 Status", value=status.upper(), inline=True)
            
            if details:
                embed.add_field(name="📝 Detalhes", value=details, inline=False)
            
            embed.set_footer(text="HyperDeploy • Log de Deploys")
            
            await self.send_log("deploys", embed)
            
        except Exception as e:
            logger.error(f"Erro ao logar deploy: {e}")
    
    async def log_error(self, error_type: str, error_message: str, context: str = None, user_id: int = None):
        """Log de erros"""
        try:
            embed = discord.Embed(
                title="❌ Erro do Sistema",
                description=f"**Tipo:** {error_type}\n**Mensagem:** {error_message}",
                color=0xff0000,
                timestamp=datetime.now()
            )
            
            if context:
                embed.add_field(name="🔍 Contexto", value=context, inline=False)
            
            if user_id:
                user = self.bot.get_user(user_id)
                username = user.name if user else f"User {user_id}"
                embed.add_field(name="👤 Usuário", value=f"{username} (`{user_id}`)", inline=True)
            
            embed.set_footer(text="HyperDeploy • Log de Erros")
            
            # Enviar para canal de admin se disponível, senão para actions
            await self.send_log("admin", embed) or await self.send_log("actions", embed)
            
        except Exception as e:
            logger.error(f"Erro ao logar erro: {e}")
    
    def get_log_channels_info(self) -> Dict[str, Any]:
        """Obtém informações sobre os canais de log configurados"""
        try:
            channels = {}
            log_types = ["actions", "payments", "deploy", "errors", "admin"]
            
            for log_type in log_types:
                channel_id = self.log_channels.get(log_type)
                if channel_id:
                    channel = self.bot.get_channel(channel_id)
                    channels[log_type] = {
                        "configured": channel is not None,
                        "name": channel.name if channel else "Canal não encontrado",
                        "id": channel_id
                    }
                else:
                    channels[log_type] = {
                        "configured": False,
                        "name": "N/A",
                        "id": None
                    }
            
            return {
                "channels": channels,
                "total_configured": len([c for c in channels.values() if c["configured"]]),
                "total_types": len(log_types)
            }
        except Exception as e:
            logger.error(f"Erro ao obter informações dos canais: {e}")
            return {"channels": {}, "total_configured": 0, "total_types": 0}

# Instância global
organized_logger = None

def setup(bot):
    """Configura o logger organizado"""
    global organized_logger
    organized_logger = OrganizedLogger(bot)

# Funções de conveniência para uso global
async def log_action(user_id: int, action: str, details: str = None, success: bool = True):
    """Log de ações dos usuários"""
    if organized_logger:
        await organized_logger.log_action(user_id, action, details, success)

async def log_admin(admin_id: int, action: str, details: str = None, target: str = None):
    """Log de ações administrativas"""
    if organized_logger:
        await organized_logger.log_admin(admin_id, action, details, target)

async def log_payment(user_id: int, payment_id: str, amount: float, status: str, details: str = None):
    """Log de pagamentos"""
    if organized_logger:
        await organized_logger.log_payment(user_id, payment_id, amount, status, details)

async def log_deploy(user_id: int, app_id: str, app_name: str, status: str, details: str = None):
    """Log de deploys"""
    if organized_logger:
        await organized_logger.log_deploy(user_id, app_id, app_name, status, details)

async def log_error(error_type: str, error_message: str, context: str = None, user_id: int = None):
    """Log de erros"""
    if organized_logger:
        await organized_logger.log_error(error_type, error_message, context, user_id) 