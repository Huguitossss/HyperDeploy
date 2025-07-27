import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class HyperDeployLogger:
    def __init__(self, name="HyperDeploy", log_dir="logs"):
        self.name = name
        self.log_dir = log_dir
        
        # Criar diretório de logs se não existir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configurar logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Evitar duplicação de handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        # Handler para arquivo com rotação (10MB por arquivo, máximo 5 arquivos)
        file_handler = RotatingFileHandler(
            os.path.join(self.log_dir, "hyperdeploy.log"),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Handler para console (sem timestamp)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatação para arquivo (com timestamp completo)
        file_formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] - %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Formatação para console (limpa, sem timestamp)
        console_formatter = logging.Formatter('%(message)s')
        
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message):
        """Log de debug para informações detalhadas"""
        self.logger.debug(f"🔍 {message}")
    
    def info(self, message):
        """Log de informação geral"""
        self.logger.info(f"ℹ️ {message}")
    
    def warning(self, message):
        """Log de aviso"""
        self.logger.warning(f"⚠️ {message}")
    
    def error(self, message):
        """Log de erro"""
        self.logger.error(f"❌ {message}")
    
    def critical(self, message):
        """Log de erro crítico"""
        self.logger.critical(f"🚨 {message}")
    
    def success(self, message):
        """Log de sucesso personalizado"""
        self.logger.info(f"✅ {message}")
    
    def command(self, user_id, command_name, guild_id=None):
        """Log de comando executado"""
        guild_info = f" (Guild: {guild_id})" if guild_id else ""
        self.logger.info(f"🎯 Comando /{command_name} executado por {user_id}{guild_info}")
    
    def payment(self, user_id, amount, status, payment_id=None):
        """Log de pagamento"""
        payment_info = f" (ID: {payment_id})" if payment_id else ""
        self.logger.info(f"💳 Pagamento R$ {amount:.2f} - Status: {status} - User: {user_id}{payment_info}")
    
    def deploy(self, user_id, app_name, status):
        """Log de deploy"""
        self.logger.info(f"🚀 Deploy {app_name} - Status: {status} - User: {user_id}")
    
    def api_call(self, endpoint, status, response_time=None):
        """Log de chamada à API"""
        time_info = f" ({response_time}ms)" if response_time else ""
        self.logger.debug(f"🌐 API {endpoint} - Status: {status}{time_info}")
    
    def security(self, event, user_id=None, details=None):
        """Log de eventos de segurança"""
        user_info = f" - User: {user_id}" if user_id else ""
        details_info = f" - {details}" if details else ""
        self.logger.warning(f"🔒 Segurança: {event}{user_info}{details_info}")

# Instância global do logger
logger = HyperDeployLogger()

# Funções de conveniência para uso global
def debug(message):
    logger.debug(message)

def info(message):
    logger.info(message)

def warning(message):
    logger.warning(message)

def error(message):
    logger.error(message)

def critical(message):
    logger.critical(message)

def success(message):
    logger.success(message)

def log_command(user_id, command_name, guild_id=None):
    logger.command(user_id, command_name, guild_id)

def log_payment(user_id, amount, status, payment_id=None):
    logger.payment(user_id, amount, status, payment_id)

def log_deploy(user_id, app_name, status):
    logger.deploy(user_id, app_name, status)

def log_api_call(endpoint, status, response_time=None):
    logger.api_call(endpoint, status, response_time)

def log_security(event, user_id=None, details=None):
    logger.security(event, user_id, details)
