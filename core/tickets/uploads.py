import discord
import os
import aiofiles
import asyncio
from datetime import datetime
from typing import Dict, Optional, List
from core.logs.logger import logger
import qrcode
from core.payments.mercadopago import criar_cobranca_pix
import yaml
from datetime import datetime, timedelta
from core.payments.config_manager import config_manager

class UploadManager:
    def __init__(self, bot):
        self.bot = bot
        self.uploads_dir = "uploads"
        self.allowed_extensions = ['.zip']
        self.ensure_uploads_dir()
        
        # Carregar access_token do Mercado Pago
        try:
            with open('config/bot.yaml', 'r', encoding='utf-8') as f:
                bot_config = yaml.safe_load(f)
                self.mercadopago_token = bot_config.get('mercadopago_access_token')
        except Exception as e:
            logger.error(f"Erro ao carregar access_token Mercado Pago: {e}")
            self.mercadopago_token = None
    
    def get_max_file_size(self):
        """Obter tamanho máximo dinâmico da configuração"""
        try:
            if config_manager:
                max_size_mb = config_manager.get_max_file_size_mb()
                return max_size_mb * 1024 * 1024  # Converter para bytes
            else:
                return 25 * 1024 * 1024  # 25MB padrão
        except Exception as e:
            logger.error(f"Erro ao obter tamanho máximo: {e}")
            return 25 * 1024 * 1024  # 25MB padrão
    
    def ensure_uploads_dir(self):
        try:
            if not os.path.exists(self.uploads_dir):
                os.makedirs(self.uploads_dir)
                logger.info(f"Diretório de uploads criado: {self.uploads_dir}")
        except Exception as e:
            logger.error(f"Erro ao criar diretório de uploads: {e}")
    
    async def process_upload(self, message: discord.Message) -> Optional[Dict]:
        try:
            # VERIFICAÇÃO DE PERMISSÕES - Apenas o dono do ticket pode fazer upload
            from core.tickets.manager import ticket_manager
            
            if not ticket_manager:
                await message.channel.send("❌ Sistema de tickets não disponível.", delete_after=5)
                return None
            
            # Verificar se o usuário tem acesso ao ticket
            if not ticket_manager.has_ticket_access(message.author.id, message.channel.id):
                await message.channel.send("❌ Você não tem permissão para fazer upload neste ticket.", delete_after=5)
                await self.log_unauthorized_upload(message.author.id, message.channel.id)
                return None
            
            # Verificar se o usuário é o dono do ticket
            if not ticket_manager.is_ticket_owner(message.author.id, message.channel.id):
                await message.channel.send("❌ Apenas o dono do ticket pode fazer upload.", delete_after=5)
                await self.log_unauthorized_upload(message.author.id, message.channel.id)
                return None
            
            if not message.attachments:
                return None
            attachment = message.attachments[0]
            
            # Verificar extensão
            if not self.is_valid_file(attachment.filename):
                await self.send_invalid_file_message(message.channel)
                return None
                
            # Verificar tamanho
            max_size = self.get_max_file_size()
            if attachment.size > max_size:
                await self.send_file_too_large_message(message.channel, attachment.size)
                return None
            
            # Log de início do upload
            await self.log_upload_start(message.author.id, attachment.filename, attachment.size)
            
            # FEEDBACK IMEDIATO - Confirmar recebimento instantaneamente
            confirmation_message = await self.send_immediate_confirmation(message.channel, attachment)
            
            # Processar arquivo e pagamento em paralelo para otimizar latência
            file_task = asyncio.create_task(self.save_file_async(attachment, message.author.id))
            payment_task = asyncio.create_task(self.prepare_payment_data(message.author.id, attachment))
            
            # Aguardar conclusão do salvamento do arquivo
            file_info = await file_task
            if not file_info:
                await confirmation_message.edit(content="❌ Erro ao salvar arquivo. Tente novamente.")
                return None
            
            # Atualizar confirmação com informações do arquivo
            await self.update_confirmation_with_file_info(confirmation_message, file_info)
            
            # Processar pagamento em background (não bloquear)
            asyncio.create_task(self.process_payment_background(message, file_info))
            
            logger.info(f"Upload processado: {file_info['filename']} ({file_info['size_mb']:.2f}MB) por {message.author.id}")
            
            # Log de upload concluído
            await self.log_upload_success(message.author.id, file_info)
            
            return file_info
            
        except Exception as e:
            logger.error(f"Erro ao processar upload: {e}")
            await self.log_upload_error(message.author.id, str(e))
            return None

    async def send_immediate_confirmation(self, channel: discord.TextChannel, attachment: discord.Attachment) -> discord.Message:
        """Envia confirmação imediata de recebimento do arquivo"""
        try:
            embed = discord.Embed(
                title="📁 Arquivo Recebido",
                description=f"**Arquivo:** {attachment.filename}",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            embed.add_field(name="📊 Tamanho", value=f"{attachment.size / (1024*1024):.2f} MB", inline=True)
            embed.add_field(name="⏳ Status", value="Processando...", inline=True)
            embed.set_footer(text="HyperDeploy • Sistema de Uploads")
            
            return await channel.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Erro ao enviar confirmação imediata: {e}")
            return await channel.send("📁 Arquivo recebido, processando...")

    async def update_confirmation_with_file_info(self, message: discord.Message, file_info: Dict):
        """Atualiza a confirmação com informações detalhadas do arquivo"""
        try:
            # Formatar tamanho com precisão
            size_mb = file_info['size_mb']
            if size_mb < 0.001:
                size_text = f"{size_mb * 1024 * 1024:.0f} bytes"
            elif size_mb < 1:
                size_text = f"{size_mb * 1024:.1f} KB"
            else:
                size_text = f"{size_mb:.2f} MB"
            
            embed = discord.Embed(
                title="✅ Arquivo Processado",
                description=f"**Arquivo:** {file_info['original_filename']}",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            embed.add_field(name="📁 Tamanho", value=size_text, inline=True)
            embed.add_field(name="⏰ Processado", value="agora mesmo", inline=True)
            embed.add_field(name="📋 Nome Interno", value=file_info['filename'], inline=False)
            embed.add_field(name="🔍 Detalhes", value=f"Tamanho real: {file_info['size_bytes']} bytes", inline=False)
            embed.set_footer(text="HyperDeploy • Sistema de Uploads")
            
            await message.edit(embed=embed)
            
        except Exception as e:
            logger.error(f"Erro ao atualizar confirmação: {e}")

    async def save_file_async(self, attachment: discord.Attachment, user_id: int) -> Optional[Dict]:
        """Salva arquivo de forma assíncrona otimizada"""
        try:
            # Registrar tempo de início do upload
            upload_start_time = datetime.now()
            
            filename = f"{user_id}_{upload_start_time.strftime('%Y%m%d_%H%M%S')}_{attachment.filename}"
            file_path = os.path.join(self.uploads_dir, filename)
            
            # Leitura assíncrona otimizada
            file_data = await attachment.read()
            
            # Escrita assíncrona
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(file_data)
            
            # Calcular tamanho real do arquivo salvo
            size_bytes = os.path.getsize(file_path)
            size_mb = size_bytes / (1024 * 1024)
            
            return {
                "filename": filename,
                "file_path": file_path,
                "size_mb": size_mb,
                "size_bytes": size_bytes,
                "uploaded_at": upload_start_time.isoformat(),
                "original_filename": attachment.filename,
                "upload_duration": (datetime.now() - upload_start_time).total_seconds()
            }
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo: {e}")
            return None

    async def prepare_payment_data(self, user_id: int, attachment: discord.Attachment) -> Dict:
        """Prepara dados do pagamento em paralelo"""
        try:
            # Obter valor do deploy da configuração
            valor = config_manager.get_fresh_deploy_price() if config_manager else 10.00
            
            # Fallback para valor zero ou inválido
            if not valor or valor <= 0:
                valor = 10.00
                logger.warning(f"⚠️ Valor inválido detectado, usando valor padrão: R$ {valor:.2f}")
            
            return {
                "user_id": user_id,
                "valor": valor,
                "descricao": f"Deploy HyperDeploy - {attachment.filename}",
                "filename": attachment.filename
            }
        except Exception as e:
            logger.error(f"Erro ao preparar dados do pagamento: {e}")
            return {
                "user_id": user_id,
                "valor": 10.00,
                "descricao": f"Deploy HyperDeploy - {attachment.filename}",
                "filename": attachment.filename
            }

    async def process_payment_background(self, message: discord.Message, file_info: Dict):
        """Processa pagamento em background para não bloquear o upload"""
        try:
            if not self.mercadopago_token:
                raise Exception("Access token Mercado Pago não configurado.")
            
            # Obter valor do deploy da configuração
            valor = config_manager.get_fresh_deploy_price() if config_manager else 10.00
            
            # Fallback para valor zero ou inválido
            if not valor or valor <= 0:
                valor = 10.00
                logger.warning(f"⚠️ Valor inválido detectado, usando valor padrão: R$ {valor:.2f}")
            
            # Validar valor antes de prosseguir
            if valor <= 0:
                raise Exception(f"Valor inválido para pagamento: R$ {valor:.2f}. Configure um valor maior que zero.")
            
            # Criar pagamento no sistema
            from core.payments.manager import payment_manager
            user_id = message.author.id
            descricao = f"Deploy HyperDeploy - {file_info['filename']}"
            
            # Criar pagamento
            payment_id = payment_manager.create_payment(user_id, valor, descricao)
            if not payment_id:
                raise Exception("Erro ao criar pagamento no sistema.")
            
            # Adicionar arquivo ao pagamento
            payment_manager.add_deploy_file(payment_id, file_info['file_path'])
            
            # Log de pagamento criado
            await self.log_payment_created(user_id, payment_id, valor, file_info['filename'])
            
            # Gerar PIX
            pix_code = criar_cobranca_pix(valor, descricao, self.mercadopago_token)
            if not pix_code:
                raise Exception("Erro ao gerar cobrança PIX Mercado Pago.")
            
            # Gerar QR Code a partir do código PIX
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(pix_code)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            nome_arquivo = f"mp_qrcode_{message.author.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            caminho_completo = os.path.join("qrcodes", nome_arquivo)
            if not os.path.exists("qrcodes"):
                os.makedirs("qrcodes")
            img.save(caminho_completo)
            
            # Enviar QR Code
            await send_qr_code(message.channel, user_id, payment_id, valor, file_info['file_path'])
            
            # Log de QR code enviado
            await self.log_qr_sent(user_id, payment_id, valor)
            
        except Exception as e:
            logger.error(f"Erro na integração Mercado Pago: {e}")
            await self.log_payment_error(message.author.id, str(e))
            
            # Mensagem de erro mais informativa
            embed = discord.Embed(
                title="❌ Erro no Pagamento",
                description="Não foi possível gerar o pagamento PIX.",
                color=0xff0000
            )
            embed.add_field(name="🔍 Detalhes", value=str(e), inline=False)
            embed.add_field(name="💡 Solução", value="Entre em contato com um administrador para verificar as configurações.", inline=False)
            embed.set_footer(text="HyperDeploy • Sistema de Pagamentos")
            
            await message.channel.send(embed=embed, delete_after=15)
    
    def is_valid_file(self, filename: str) -> bool:
        return any(filename.lower().endswith(ext) for ext in self.allowed_extensions)
    
    async def send_invalid_file_message(self, channel: discord.TextChannel):
        await channel.send("❌ Arquivo inválido. Envie apenas arquivos .zip.", delete_after=10)
    
    async def send_file_too_large_message(self, channel: discord.TextChannel, file_size: int):
        size_mb = file_size / (1024 * 1024)
        max_size = config_manager.get_max_file_size_mb() if config_manager else 25
        
        embed = discord.Embed(
            title="❌ Arquivo Muito Grande",
            description=f"O arquivo excede o tamanho máximo permitido.",
            color=0xff0000
        )
        embed.add_field(name="📁 Tamanho do Arquivo", value=f"{size_mb:.2f} MB", inline=True)
        embed.add_field(name="📏 Limite Máximo", value=f"{max_size} MB", inline=True)
        embed.add_field(name="💡 Dica", value="Comprima o arquivo ou divida em partes menores.", inline=False)
        embed.set_footer(text="HyperDeploy • Sistema de Uploads")
        
        await channel.send(embed=embed, delete_after=15)

    # Métodos de Log (mantidos como estavam)
    async def log_upload_start(self, user_id: int, filename: str, file_size: int):
        """Log de início do upload"""
        try:
            from core.logs.organized_logger import log_action
            await log_action(
                user_id=user_id,
                action="Upload Iniciado",
                details=f"Arquivo: {filename} | Tamanho: {file_size / (1024*1024):.2f} MB",
                success=True
            )
        except Exception as e:
            logger.error(f"Erro ao logar início do upload: {e}")

    async def log_upload_success(self, user_id: int, file_info: Dict):
        """Log de upload concluído"""
        try:
            from core.logs.organized_logger import log_action
            await log_action(
                user_id=user_id,
                action="Upload Concluído",
                details=f"Arquivo: {file_info['original_filename']} | Tamanho: {file_info['size_mb']:.2f} MB | Duração: {file_info['upload_duration']:.2f}s",
                success=True
            )
        except Exception as e:
            logger.error(f"Erro ao logar upload sucesso: {e}")

    async def log_upload_error(self, user_id: int, error: str):
        """Log de erro no upload"""
        try:
            from core.logs.organized_logger import log_action
            await log_action(
                user_id=user_id,
                action="Erro no Upload",
                details=f"Erro: {error}",
                success=False
            )
        except Exception as e:
            logger.error(f"Erro ao logar erro de upload: {e}")

    async def log_payment_created(self, user_id: int, payment_id: str, valor: float, filename: str):
        """Log de pagamento criado"""
        try:
            from core.logs.organized_logger import log_payment
            await log_payment(
                user_id=user_id,
                payment_id=payment_id,
                amount=valor,
                status="pending",
                details=f"Arquivo: {filename}"
            )
        except Exception as e:
            logger.error(f"Erro ao logar pagamento criado: {e}")

    async def log_qr_sent(self, user_id: int, payment_id: str, valor: float):
        """Log de QR code enviado"""
        try:
            from core.logs.organized_logger import log_payment
            await log_payment(
                user_id=user_id,
                payment_id=payment_id,
                amount=valor,
                status="processing",
                details="QR Code enviado ao usuário"
            )
        except Exception as e:
            logger.error(f"Erro ao logar QR enviado: {e}")

    async def log_payment_error(self, user_id: int, error: str):
        """Log de erro no pagamento"""
        try:
            from core.logs.organized_logger import log_payment
            await log_payment(
                user_id=user_id,
                payment_id="ERROR",
                amount=0.0,
                status="failed",
                details=f"Erro: {error}"
            )
        except Exception as e:
            logger.error(f"Erro ao logar erro de pagamento: {e}")

    async def log_unauthorized_upload(self, user_id: int, channel_id: int):
        """Log de tentativa de upload não autorizado"""
        try:
            from core.logs.organized_logger import log_action
            await log_action(
                user_id=user_id,
                action="Tentativa de Upload Não Autorizado",
                details=f"Usuário: {user_id} | Canal: {channel_id}",
                success=False
            )
        except Exception as e:
            logger.error(f"Erro ao logar tentativa de upload não autorizado: {e}")

async def send_qr_code(channel, user_id, payment_id, valor, file_path):
    """Envia QR Code do PIX no canal"""
    try:
        embed = discord.Embed(
            title="💳 Pagamento PIX Mercado Pago Necessário",
            description="Para prosseguir com o deploy, realize o pagamento via PIX usando o QR Code abaixo.",
            color=0x00ff00,
            timestamp=datetime.now()
        )
        embed.add_field(name="Valor", value=f"R$ {valor:.2f}", inline=True)
        embed.add_field(name="Status", value="Aguardando pagamento...", inline=True)
        embed.add_field(name="Arquivo", value=f"`{os.path.basename(file_path)}`", inline=True)
        embed.set_footer(text="HyperDeploy • Sistema de Pagamentos")
        
        # Gerar QR Code
        qr_path = f"qrcodes/{payment_id}_qrcode.png"
        os.makedirs("qrcodes", exist_ok=True)
        
        # Aqui você precisaria gerar o QR Code real do PIX
        # Por enquanto, vamos usar um placeholder
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"PIX_PAYMENT_{payment_id}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_path)
        
        file = discord.File(qr_path, filename="qrcode.png")
        embed.set_image(url="attachment://qrcode.png")
        await channel.send(embed=embed, file=file)
        logger.info(f"💳 QR Code Mercado Pago enviado para {user_id} - R$ {valor:.2f}")
        
    except Exception as e:
        logger.error(f"Erro ao enviar QR Code: {e}")
        embed = discord.Embed(
            title="❌ Erro ao Gerar QR Code",
            description="Ocorreu um erro ao gerar o QR Code. Tente novamente.",
            color=0xff0000
        )
        await channel.send(embed=embed)

def setup(bot):
    global upload_manager
    upload_manager = UploadManager(bot) 