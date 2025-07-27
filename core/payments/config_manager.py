import json
import os
from typing import Dict, Optional
from core.logs.logger import logger

class ConfigManager:
    def __init__(self):
        self.config_file = "data/admin_config.json"
        self.config = self.load_config(log_message=False)
    
    def load_config(self, log_message: bool = False) -> Dict:
        """Carrega configurações do arquivo JSON"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                if log_message:
                    logger.info(f"Configurações carregadas ({len(config)} itens)")
                return config
            else:
                # Configuração padrão
                default_config = {
                    "deploy_price": 10.00,
                    "max_file_size_mb": 25,
                    "ticket_timeout_minutes": 30,
                    "payment_timeout_minutes": 30,
                    "auto_deploy": True,
                    "mercadopago_enabled": True
                }
                self.save_config(default_config)
                return default_config
        except Exception as e:
            logger.error(f"Erro ao carregar configurações: {e}")
            return {}
    
    def save_config(self, config: Dict = None):
        """Salva configurações no arquivo JSON"""
        try:
            if config:
                self.config = config
            
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            logger.info("Configurações salvas")
        except Exception as e:
            logger.error(f"Erro ao salvar configurações: {e}")
    
    def reload_config(self):
        """Recarrega as configurações do disco"""
        self.config = self.load_config(log_message=True)
        logger.info("Configurações recarregadas")
    
    def get_deploy_price(self) -> float:
        """Obtém o preço do deploy"""
        price = self.config.get("deploy_price", 10.00)
        if price is None or price <= 0:
            return 10.00
        return price
    
    def set_deploy_price(self, price: float):
        """Define o preço do deploy"""
        if price is None or price <= 0:
            logger.warning(f"Tentativa de salvar preço inválido: {price}. O valor deve ser maior que zero.")
            return False
        self.config["deploy_price"] = float(price)
        self.save_config()
        self.reload_config()
        logger.info(f"Preço do deploy: R$ {price:.2f}")
        return True
    
    def get_fresh_deploy_price(self) -> float:
        """Obtém o preço do deploy diretamente do arquivo (sempre atualizado)"""
        try:
            # Recarregar configurações do disco
            fresh_config = self.load_config(log_message=False)
            price = fresh_config.get("deploy_price", 10.00)
            if price is None or price <= 0:
                return 10.00
            return price
        except Exception as e:
            logger.error(f"Erro ao obter preço atualizado: {e}")
            return 10.00
    
    def get_max_file_size_mb(self) -> int:
        """Obtém o tamanho máximo de arquivo em MB"""
        return self.config.get("max_file_size_mb", 25)
    
    def set_max_file_size_mb(self, size_mb: int):
        """Define o tamanho máximo de arquivo em MB"""
        self.config["max_file_size_mb"] = int(size_mb)
        self.save_config()
        self.reload_config()
        logger.info(f"Tamanho máximo de arquivo: {size_mb} MB")
    
    def get_ticket_timeout_minutes(self) -> int:
        """Obtém o timeout dos tickets em minutos"""
        return self.config.get("ticket_timeout_minutes", 30)
    
    def set_ticket_timeout_minutes(self, minutes: int):
        """Define o timeout dos tickets em minutos"""
        self.config["ticket_timeout_minutes"] = int(minutes)
        self.save_config()
        self.reload_config()
        logger.info(f"Timeout dos tickets: {minutes} minutos")
    
    def get_payment_timeout_minutes(self) -> int:
        """Obtém o timeout dos pagamentos em minutos"""
        return self.config.get("payment_timeout_minutes", 30)
    
    def set_payment_timeout_minutes(self, minutes: int):
        """Define o timeout dos pagamentos em minutos"""
        self.config["payment_timeout_minutes"] = int(minutes)
        self.save_config()
        self.reload_config()
        logger.info(f"Timeout dos pagamentos: {minutes} minutos")
    
    def is_auto_deploy_enabled(self) -> bool:
        """Verifica se o deploy automático está habilitado"""
        return self.config.get("auto_deploy", True)
    
    def set_auto_deploy(self, enabled: bool):
        """Define se o deploy automático está habilitado"""
        self.config["auto_deploy"] = bool(enabled)
        self.save_config()
        self.reload_config()
        status = "habilitado" if enabled else "desabilitado"
        logger.info(f"Deploy automático {status}")
    
    def is_mercadopago_enabled(self) -> bool:
        """Verifica se o Mercado Pago está habilitado"""
        return self.config.get("mercadopago_enabled", True)
    
    def set_mercadopago_enabled(self, enabled: bool):
        """Define se o Mercado Pago está habilitado"""
        self.config["mercadopago_enabled"] = bool(enabled)
        self.save_config()
        self.reload_config()
        status = "habilitado" if enabled else "desabilitado"
        logger.info(f"Mercado Pago {status}")
    
    def get_all_config(self) -> Dict:
        """Obtém todas as configurações"""
        return self.config.copy()
    
    def get_fresh_config(self) -> Dict:
        """Obtém configurações diretamente do arquivo (sempre atualizado)"""
        try:
            return self.load_config(log_message=False)
        except Exception as e:
            logger.error(f"Erro ao obter configurações atualizadas: {e}")
            return self.config
    
    def reset_to_default(self):
        """Reseta para configurações padrão"""
        default_config = {
            "deploy_price": 10.00,
            "max_file_size_mb": 25,
            "ticket_timeout_minutes": 30,
            "payment_timeout_minutes": 30,
            "auto_deploy": True,
            "mercadopago_enabled": True
        }
        self.save_config(default_config)
        logger.info("Configurações resetadas para padrão")

# Instância global
config_manager = None

def setup():
    """Configura o gerenciador de configurações"""
    global config_manager
    config_manager = ConfigManager() 