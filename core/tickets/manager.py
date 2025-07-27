import discord
import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from core.logs.logger import logger
import threading

class TicketManager:
    def __init__(self, bot):
        self.bot = bot
        self.active_tickets: Dict[int, Dict] = {}
        self.tickets_file = "data/tickets.json"
        self.counter_file = "data/ticket_counter.json"
        self.ticket_counter = self.load_ticket_counter()
        self.counter_lock = threading.Lock()
        self.load_tickets()
    
    def load_ticket_counter(self):
        try:
            if os.path.exists(self.counter_file):
                with open(self.counter_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return int(data.get("counter", 1))
            else:
                self.save_ticket_counter(1)
                return 1
        except Exception as e:
            logger.error(f"Erro ao carregar ticket_counter: {e}")
            return 1
    
    def save_ticket_counter(self, value):
        try:
            os.makedirs(os.path.dirname(self.counter_file), exist_ok=True)
            with open(self.counter_file, 'w', encoding='utf-8') as f:
                json.dump({"counter": value}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao salvar ticket_counter: {e}")
    
    def get_next_ticket_number(self):
        with self.counter_lock:
            number = self.ticket_counter
            self.ticket_counter += 1
            self.save_ticket_counter(self.ticket_counter)
            return number
    
    def load_tickets(self):
        try:
            if os.path.exists(self.tickets_file):
                with open(self.tickets_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.active_tickets = {int(k): v for k, v in data.items()}
                logger.info(f"📋 {len(self.active_tickets)} tickets carregados")
            else:
                self.save_tickets()
        except Exception as e:
            logger.error(f"Erro ao carregar tickets: {e}")
            self.active_tickets = {}
    
    def save_tickets(self):
        try:
            os.makedirs(os.path.dirname(self.tickets_file), exist_ok=True)
            with open(self.tickets_file, 'w', encoding='utf-8') as f:
                json.dump(self.active_tickets, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao salvar tickets: {e}")
    
    async def create_ticket(self, user_id: int, guild_id: int, channel_id: int) -> Optional[discord.TextChannel]:
        try:
            if user_id in self.active_tickets:
                return None
            guild = self.bot.get_guild(guild_id)
            if not guild:
                logger.error(f"Guild não encontrada: {guild_id}")
                return None
            category = discord.utils.get(guild.categories, name="Tickets")
            if not category:
                category = await guild.create_category("Tickets")
                logger.info(f"Categoria 'Tickets' criada em {guild.name}")
            ticket_number = self.get_next_ticket_number()
            ticket_name = f"ticket-{ticket_number:03d}"
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True),
                guild.get_member(user_id): discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True)
            }
            channel = await guild.create_text_channel(
                name=ticket_name,
                category=category,
                overwrites=overwrites,
                topic=f"Ticket de deploy para <@{user_id}>"
            )
            self.active_tickets[user_id] = {
                "channel_id": channel.id,
                "guild_id": guild_id,
                "created_at": datetime.now().isoformat(),
                "status": "open",
                "user_id": user_id,
                "files": [],
                "payment_status": "pending",
                "ticket_number": ticket_number
            }
            self.save_tickets()
            
            # Enviar mensagem inicial com instruções
            await self.send_ticket_welcome_message(channel, user_id, ticket_number)
            
            # Log de ticket criado
            await self.log_ticket_created(user_id, ticket_number, channel.id)
            
            logger.info(f"Ticket criado: {ticket_name} para {user_id}")
            return channel
        except Exception as e:
            logger.error(f"Erro ao criar ticket: {e}")
            await self.log_ticket_error(user_id, f"Erro ao criar ticket: {e}")
            return None

    async def send_ticket_welcome_message(self, channel: discord.TextChannel, user_id: int, ticket_number: int):
        """Envia mensagem de boas-vindas com instruções no ticket"""
        try:
            # Obter preço atual do deploy
            from core.payments.config_manager import config_manager
            price = config_manager.get_fresh_deploy_price() if config_manager else 10.00
            timeout_minutes = config_manager.get_ticket_timeout_minutes() if config_manager else 30
            max_file_size = config_manager.get_max_file_size_mb() if config_manager else 25
            
            embed = discord.Embed(
                title="🎫 Ticket de Deploy Criado",
                description=f"Bem-vindo ao seu ticket de deploy! Aqui você pode fazer upload do seu arquivo ZIP.",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            embed.add_field(name="🎫 Número do Ticket", value=f"#{ticket_number:03d}", inline=True)
            embed.add_field(name="💰 Preço do Deploy", value=f"R$ {price:.2f}", inline=True)
            embed.add_field(name="⏰ Expira em", value=f"{timeout_minutes} minutos", inline=True)
            
            embed.add_field(
                name="📋 Instruções", 
                value=(
                    "1. **Envie seu arquivo ZIP** neste canal\n"
                    "2. **Aguarde o QR Code PIX** ser gerado\n"
                    "3. **Faça o pagamento** via PIX\n"
                    "4. **Deploy automático** será iniciado\n\n"
                    "⚠️ **Importante:**\n"
                    "• Apenas arquivos .zip são aceitos\n"
                    f"• Tamanho máximo: {max_file_size}MB\n"
                    f"• Ticket expira em {timeout_minutes} minutos\n"
                    "• Deploy automático após pagamento"
                ), 
                inline=False
            )
            
            embed.add_field(
                name="🔧 Requisitos do ZIP", 
                value=(
                    "• Deve conter `squarecloud.app` ou `squarecloud.config`\n"
                    "• Arquivo principal deve estar na raiz\n"
                    "• Estrutura organizada de pastas\n"
                    "• Sem arquivos desnecessários"
                ), 
                inline=False
            )
            
            embed.set_footer(text="HyperDeploy • Sistema de Tickets")
            
            await channel.send(embed=embed)
            
            # Mensagem adicional com dicas
            tips_embed = discord.Embed(
                title="💡 Dicas para um Deploy Bem-Sucedido",
                description="Siga estas dicas para garantir que seu deploy funcione perfeitamente:",
                color=0xffff00
            )
            tips_embed.add_field(
                name="📁 Estrutura Recomendada",
                value=(
                    "```\n"
                    "seu-projeto/\n"
                    "├── main.py (ou index.js)\n"
                    "├── requirements.txt (ou package.json)\n"
                    "├── squarecloud.app\n"
                    "└── outros arquivos...\n"
                    "```"
                ),
                inline=False
            )
            tips_embed.add_field(
                name="✅ Boas Práticas",
                value=(
                    "• Teste localmente antes do deploy\n"
                    "• Verifique se todas as dependências estão incluídas\n"
                    "• Use nomes de arquivo sem espaços\n"
                    "• Mantenha o ZIP organizado"
                ),
                inline=False
            )
            tips_embed.set_footer(text="HyperDeploy • Dicas de Deploy")
            
            await channel.send(embed=tips_embed)
            
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem de boas-vindas: {e}")
            # Fallback simples
            await channel.send(
                f"🎫 Ticket #{ticket_number:03d} criado com sucesso!\n"
                f"Envie seu arquivo ZIP para continuar com o deploy.\n"
                f"Preço: R$ {price:.2f}"
            )
    async def close_ticket(self, user_id: int, reason: str = "Deploy concluído"):
        try:
            if user_id not in self.active_tickets:
                return False
            ticket_info = self.active_tickets[user_id]
            channel_id = ticket_info["channel_id"]
            channel = self.bot.get_channel(channel_id)
            if channel:
                await channel.delete(reason=f"Ticket fechado: {reason}")
            del self.active_tickets[user_id]
            self.save_tickets()
            
            # Log de ticket fechado
            await self.log_ticket_closed(user_id, reason, ticket_info.get("ticket_number", 0))
            
            logger.info(f"Ticket fechado para {user_id}: {reason}")
            return True
        except Exception as e:
            logger.error(f"Erro ao fechar ticket: {e}")
            await self.log_ticket_error(user_id, f"Erro ao fechar ticket: {e}")
            return False
    async def add_file_to_ticket(self, user_id: int, file_info: Dict):
        try:
            if user_id not in self.active_tickets:
                return False
            self.active_tickets[user_id]["files"].append(file_info)
            self.save_tickets()
            logger.info(f"📁 Arquivo adicionado ao ticket {user_id}: {file_info.get('filename', 'N/A')}")
            return True
        except Exception as e:
            logger.error(f"Erro ao adicionar arquivo ao ticket: {e}")
            return False
    def get_ticket_info(self, user_id: int) -> Optional[Dict]:
        return self.active_tickets.get(user_id)
    def get_active_tickets(self) -> List[Dict]:
        return list(self.active_tickets.values())
    def get_tickets_by_status(self, status: str) -> List[Dict]:
        return [
            ticket for ticket in self.active_tickets.values()
            if ticket.get("status") == status
        ]
    def get_tickets_by_payment_status(self, payment_status: str) -> List[Dict]:
        return [
            ticket for ticket in self.active_tickets.values()
            if ticket.get("payment_status") == payment_status
        ]
    
    async def cleanup_expired_tickets(self):
        """Limpa tickets expirados"""
        try:
            # Obter timeout configurado do config_manager
            from core.payments.config_manager import config_manager
            timeout_minutes = config_manager.get_ticket_timeout_minutes() if config_manager else 30
            current_time = datetime.now()
            expired_tickets = []
            
            for user_id, ticket_info in self.active_tickets.items():
                created_at = datetime.fromisoformat(ticket_info["created_at"])
                if current_time - created_at > timedelta(minutes=timeout_minutes):
                    expired_tickets.append(user_id)
            
            for user_id in expired_tickets:
                await self.close_ticket(user_id, f"Ticket expirado ({timeout_minutes} minutos)")
                
            if expired_tickets:
                logger.info(f"🧹 {len(expired_tickets)} tickets expirados removidos")
                
        except Exception as e:
            logger.error(f"Erro ao limpar tickets expirados: {e}")

    # Métodos de Log
    async def log_ticket_created(self, user_id: int, ticket_number: int, channel_id: int):
        """Log de ticket criado"""
        try:
            from core.logs.organized_logger import log_action
            await log_action(
                user_id=user_id,
                action="Ticket Criado",
                details=f"Ticket #{ticket_number:03d} | Canal: <#{channel_id}>",
                success=True
            )
        except Exception as e:
            logger.error(f"Erro ao logar ticket criado: {e}")

    async def log_ticket_closed(self, user_id: int, reason: str, ticket_number: int):
        """Log de ticket fechado"""
        try:
            from core.logs.organized_logger import log_action
            await log_action(
                user_id=user_id,
                action="Ticket Fechado",
                details=f"Ticket #{ticket_number:03d} | Motivo: {reason}",
                success=True
            )
        except Exception as e:
            logger.error(f"Erro ao logar ticket fechado: {e}")

    async def log_ticket_error(self, user_id: int, error: str):
        """Log de erro em ticket"""
        try:
            from core.logs.organized_logger import log_action
            await log_action(
                user_id=user_id,
                action="Erro no Ticket",
                details=f"Erro: {error}",
                success=False
            )
        except Exception as e:
            logger.error(f"Erro ao logar erro de ticket: {e}")

ticket_manager = None

def setup(bot):
    global ticket_manager
    ticket_manager = TicketManager(bot) 