import asyncio
import os
import shutil
import discord
from typing import Optional, Dict
from datetime import datetime
from core.logs.logger import logger
from core.payments.manager import payment_manager
from core.tickets.manager import ticket_manager
from core.squarecloud.client import squarecloud_manager
from core.squarecloud.user_keys import user_keys_manager

class DeployManager:
    def __init__(self):
        self.deploy_queue = []
        self.processing = False
    
    async def process_confirmed_payments(self):
        """Processa pagamentos confirmados e faz deploy automático"""
        try:
            if not payment_manager:
                return
            
            # Obter pagamentos confirmados
            confirmed_payments = payment_manager.get_payments_by_status("paid")
            
            for payment in confirmed_payments:
                payment_id = payment["id"]
                user_id = payment["user_id"]
                deploy_file = payment.get("deploy_file")
                
                # Verificar se já foi processado
                if payment.get("deploy_processed"):
                    continue
                
                # Verificar se tem arquivo de deploy
                if not deploy_file or not os.path.exists(deploy_file):
                    logger.warning(f"Arquivo de deploy não encontrado para pagamento {payment_id}")
                    continue
                
                # Verificar se usuário tem chave configurada
                if not user_keys_manager.has_user_key(user_id):
                    logger.warning(f"Usuário {user_id} não tem chave da API configurada")
                    continue
                
                # Processar deploy
                await self.process_deploy(payment_id, user_id, deploy_file)
                
        except Exception as e:
            logger.error(f"Erro ao processar pagamentos confirmados: {e}")
    
    async def process_deploy(self, payment_id: str, user_id: int, zip_path: str):
        """Processa o deploy de uma aplicação"""
        try:
            logger.info(f"Iniciando deploy para pagamento {payment_id} - Usuário {user_id}")
            
            # Marcar pagamento como em processamento
            payment_manager.update_payment_status(payment_id, "processing")
            
            # Obter chave da API do usuário
            api_key = user_keys_manager.get_user_key(user_id)
            if not api_key:
                logger.error(f"Chave da API não encontrada para usuário {user_id}")
                payment_manager.update_payment_status(payment_id, "failed", {"error": "Chave da API não configurada"})
                return
            
            # Fazer upload para Square Cloud
            result = await squarecloud_manager.upload_app(api_key, zip_path)
            
            if result["status"] == "success":
                app_result = result["result"]
                app_id = app_result.id if hasattr(app_result, 'id') else "N/A"
                app_name = getattr(app_result, 'name', 'N/A')
                
                # Marcar pagamento como deploy concluído
                payment_manager.update_payment_status(payment_id, "deployed", {
                    "app_id": app_id,
                    "app_name": app_name,
                    "deploy_completed_at": datetime.now().isoformat()
                })
                
                # Iniciar aplicação se configurado
                config = squarecloud_manager.config
                if config.get("auto_deploy", {}).get("start_after_deploy", True):
                    try:
                        await squarecloud_manager.start_app(api_key, app_id)
                        logger.info(f"Aplicação {app_id} iniciada automaticamente")
                    except Exception as e:
                        logger.warning(f"Erro ao iniciar aplicação automaticamente: {e}")
                
                # Notificar usuário
                await self.notify_deploy_success(user_id, payment_id, app_id, app_name, zip_path)
                
                logger.info(f"✅ Deploy concluído com sucesso - App ID: {app_id}")
                
            else:
                error_msg = result.get("error", "Erro desconhecido")
                payment_manager.update_payment_status(payment_id, "failed", {"error": error_msg})
                await self.notify_deploy_failed(user_id, payment_id, error_msg)
                logger.error(f"❌ Deploy falhou para pagamento {payment_id}: {error_msg}")
            
            # Limpar arquivo temporário
            try:
                if os.path.exists(zip_path):
                    os.remove(zip_path)
                    logger.info(f"🗑️ Arquivo temporário removido: {zip_path}")
            except Exception as e:
                logger.warning(f"Erro ao remover arquivo temporário: {e}")
                
        except Exception as e:
            logger.error(f"Erro ao processar deploy: {e}")
            payment_manager.update_payment_status(payment_id, "failed", {"error": str(e)})
            await self.notify_deploy_failed(user_id, payment_id, str(e))
    
    async def notify_deploy_success(self, user_id: int, payment_id: str, app_id: str, app_name: str, zip_path: str):
        """Notifica usuário sobre deploy bem-sucedido"""
        try:
            # Tentar enviar mensagem no canal do ticket
            ticket_info = ticket_manager.get_ticket_info(user_id)
            if ticket_info:
                channel_id = ticket_info["channel_id"]
                channel = ticket_manager.bot.get_channel(channel_id)
                
                if channel:
                    embed = discord.Embed(
                        title="✅ Deploy Concluído!",
                        description=f"Seu deploy foi realizado com sucesso!",
                        color=0x00ff00,
                        timestamp=datetime.now()
                    )
                    embed.add_field(name="ID da Aplicação", value=f"`{app_id}`", inline=True)
                    embed.add_field(name="Nome", value=f"`{app_name}`", inline=True)
                    embed.add_field(name="Arquivo", value=f"`{os.path.basename(zip_path)}`", inline=True)
                    embed.add_field(name="Status", value="🟢 Online", inline=True)
                    embed.set_footer(text="HyperDeploy • Deploy Automático")
                    
                    await channel.send(f"🎉 <@{user_id}>, seu deploy foi concluído com sucesso!", embed=embed)
                    return
            
            # Se não conseguir enviar no canal, tentar DM
            user = ticket_manager.bot.get_user(user_id)
            if user:
                try:
                    embed = discord.Embed(
                        title="✅ Deploy Concluído!",
                        description=f"Seu deploy foi realizado com sucesso!",
                        color=0x00ff00
                    )
                    embed.add_field(name="ID da Aplicação", value=f"`{app_id}`", inline=True)
                    embed.add_field(name="Nome", value=f"`{app_name}`", inline=True)
                    embed.add_field(name="Status", value="🟢 Online", inline=True)
                    
                    await user.send(embed=embed)
                except Exception as e:
                    logger.warning(f"Erro ao enviar DM para usuário {user_id}: {e}")
                    
        except Exception as e:
            logger.error(f"Erro ao notificar sucesso do deploy: {e}")
    
    async def notify_deploy_failed(self, user_id: int, payment_id: str, error_msg: str):
        """Notifica usuário sobre falha no deploy"""
        try:
            # Tentar enviar mensagem no canal do ticket
            ticket_info = ticket_manager.get_ticket_info(user_id)
            if ticket_info:
                channel_id = ticket_info["channel_id"]
                channel = ticket_manager.bot.get_channel(channel_id)
                
                if channel:
                    embed = discord.Embed(
                        title="❌ Deploy Falhou",
                        description=f"Ocorreu um erro durante o deploy:",
                        color=0xff0000,
                        timestamp=datetime.now()
                    )
                    embed.add_field(name="Erro", value=f"```{error_msg}```", inline=False)
                    embed.add_field(name="Ação", value="Entre em contato com um administrador", inline=False)
                    embed.set_footer(text="HyperDeploy • Deploy Automático")
                    
                    await channel.send(f"❌ <@{user_id}>, houve um problema com seu deploy.", embed=embed)
                    return
            
            # Se não conseguir enviar no canal, tentar DM
            user = ticket_manager.bot.get_user(user_id)
            if user:
                try:
                    embed = discord.Embed(
                        title="❌ Deploy Falhou",
                        description=f"Ocorreu um erro durante o deploy:",
                        color=0xff0000
                    )
                    embed.add_field(name="Erro", value=f"```{error_msg}```", inline=False)
                    
                    await user.send(embed=embed)
                except Exception as e:
                    logger.warning(f"Erro ao enviar DM para usuário {user_id}: {e}")
                    
        except Exception as e:
            logger.error(f"Erro ao notificar falha do deploy: {e}")
    
    async def start_deploy_loop(self):
        """Inicia o loop de verificação de pagamentos para deploy"""
        while True:
            try:
                await self.process_confirmed_payments()
                await asyncio.sleep(10)  # Verificar a cada 10 segundos
            except Exception as e:
                logger.error(f"Erro no loop de deploy: {e}")
                await asyncio.sleep(30)  # Aguardar mais tempo em caso de erro

# Instância global
deploy_manager = None

def setup():
    """Configura o gerenciador de deploy"""
    global deploy_manager
    deploy_manager = DeployManager() 