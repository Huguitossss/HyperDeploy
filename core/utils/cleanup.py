import os
import asyncio
import time
from datetime import datetime, timedelta
from core.logs.logger import logger

class CleanupManager:
    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.cleanup_task = None
        
        # Diretórios para limpeza
        self.qrcodes_dir = "qrcodes"
        self.uploads_dir = "uploads"
        
        # Configurações de limpeza
        self.qrcode_expiry_hours = 1  # QR Codes expiram em 1 hora
        self.upload_expiry_hours = 24  # Uploads expiram em 24 horas
        self.cleanup_interval = 300  # Limpeza a cada 5 minutos
    
    async def start_cleanup_service(self):
        """Inicia o serviço de limpeza automática"""
        if self.running:
            return
        
        self.running = True
        logger.info("🧹 Serviço de limpeza automática iniciado")
        
        while self.running:
            try:
                await self.cleanup_expired_files()
                await asyncio.sleep(self.cleanup_interval)
            except Exception as e:
                logger.error(f"Erro no serviço de limpeza: {e}")
                await asyncio.sleep(60)  # Espera 1 minuto em caso de erro
    
    async def stop_cleanup_service(self):
        """Para o serviço de limpeza automática"""
        self.running = False
        if self.cleanup_task:
            self.cleanup_task.cancel()
        logger.info("🧹 Serviço de limpeza automática parado")
    
    async def cleanup_expired_files(self):
        """Remove arquivos expirados"""
        try:
            # Limpar QR Codes expirados
            qrcodes_removed = await self._cleanup_qrcodes()
            
            # Limpar uploads expirados
            uploads_removed = await self._cleanup_uploads()
            
            if qrcodes_removed > 0 or uploads_removed > 0:
                logger.info(f"🧹 Limpeza automática: {qrcodes_removed} QR Codes e {uploads_removed} uploads removidos")
                
        except Exception as e:
            logger.error(f"Erro durante limpeza automática: {e}")
    
    async def _cleanup_qrcodes(self):
        """Remove QR Codes expirados"""
        if not os.path.exists(self.qrcodes_dir):
            return 0
        
        removed_count = 0
        expiry_time = datetime.now() - timedelta(hours=self.qrcode_expiry_hours)
        
        try:
            for filename in os.listdir(self.qrcodes_dir):
                file_path = os.path.join(self.qrcodes_dir, filename)
                
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    
                    if file_time < expiry_time:
                        os.remove(file_path)
                        removed_count += 1
                        logger.debug(f"QR Code expirado removido: {filename}")
            
            return removed_count
            
        except Exception as e:
            logger.error(f"Erro ao limpar QR Codes: {e}")
            return 0
    
    async def _cleanup_uploads(self):
        """Remove uploads expirados"""
        if not os.path.exists(self.uploads_dir):
            return 0
        
        removed_count = 0
        expiry_time = datetime.now() - timedelta(hours=self.upload_expiry_hours)
        
        try:
            for filename in os.listdir(self.uploads_dir):
                file_path = os.path.join(self.uploads_dir, filename)
                
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    
                    if file_time < expiry_time:
                        os.remove(file_path)
                        removed_count += 1
                        logger.debug(f"Upload expirado removido: {filename}")
            
            return removed_count
            
        except Exception as e:
            logger.error(f"Erro ao limpar uploads: {e}")
            return 0
    
    async def force_cleanup(self):
        """Força uma limpeza imediata"""
        logger.info("🧹 Limpeza forçada iniciada")
        await self.cleanup_expired_files()
        logger.info("🧹 Limpeza forçada concluída")
    
    async def get_cleanup_stats(self):
        """Retorna estatísticas de limpeza"""
        stats = {
            'qrcodes_dir': self.qrcodes_dir,
            'uploads_dir': self.uploads_dir,
            'qrcode_expiry_hours': self.qrcode_expiry_hours,
            'upload_expiry_hours': self.upload_expiry_hours,
            'cleanup_interval': self.cleanup_interval,
            'running': self.running
        }
        
        # Contar arquivos atuais
        try:
            if os.path.exists(self.qrcodes_dir):
                stats['qrcodes_count'] = len([f for f in os.listdir(self.qrcodes_dir) if os.path.isfile(os.path.join(self.qrcodes_dir, f))])
            else:
                stats['qrcodes_count'] = 0
                
            if os.path.exists(self.uploads_dir):
                stats['uploads_count'] = len([f for f in os.listdir(self.uploads_dir) if os.path.isfile(os.path.join(self.uploads_dir, f))])
            else:
                stats['uploads_count'] = 0
                
        except Exception as e:
            logger.error(f"Erro ao contar arquivos: {e}")
            stats['qrcodes_count'] = 0
            stats['uploads_count'] = 0
        
        return stats

# Funções de conveniência
async def start_cleanup(bot):
    """Inicia o serviço de limpeza"""
    cleanup_manager = CleanupManager(bot)
    cleanup_manager.cleanup_task = asyncio.create_task(cleanup_manager.start_cleanup_service())
    return cleanup_manager

async def stop_cleanup(cleanup_manager):
    """Para o serviço de limpeza"""
    if cleanup_manager:
        await cleanup_manager.stop_cleanup_service()

async def force_cleanup(cleanup_manager):
    """Força uma limpeza imediata"""
    if cleanup_manager:
        await cleanup_manager.force_cleanup()

async def get_cleanup_stats(cleanup_manager):
    """Retorna estatísticas de limpeza"""
    if cleanup_manager:
        return await cleanup_manager.get_cleanup_stats()
    return None 