import json
import os
import asyncio
import discord
from datetime import datetime
from typing import Dict, List, Optional
from core.logs.logger import logger
from core.squarecloud.client import SquareCloudManager

class DomainManager:
    def __init__(self):
        self.domain_data_file = "data/domains.json"
        self.domain_data: Dict = {}
        self.squarecloud_manager = SquareCloudManager()
        self.load_domain_data()
    
    def load_domain_data(self):
        """Carrega dados de domínios do arquivo JSON"""
        try:
            if os.path.exists(self.domain_data_file):
                with open(self.domain_data_file, 'r', encoding='utf-8') as f:
                    self.domain_data = json.load(f)
                logger.info(f"🌐 {len(self.domain_data)} registros de domínios carregados")
            else:
                self.save_domain_data()
        except Exception as e:
            logger.error(f"Erro ao carregar dados de domínios: {e}")
            self.domain_data = {}
    
    def save_domain_data(self):
        """Salva dados de domínios no arquivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.domain_data_file), exist_ok=True)
            with open(self.domain_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.domain_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao salvar dados de domínios: {e}")
    
    async def set_domain(self, api_key: str, app_id: str, domain: str, app_name: str = "Aplicação") -> bool:
        """Configura um domínio personalizado para uma aplicação"""
        try:
            logger.info(f"🌐 Configurando domínio {domain} para aplicação {app_id}")
            
            # Validar formato do domínio
            if not self.validate_domain(domain):
                logger.error(f"❌ Formato de domínio inválido: {domain}")
                return False
            
            # Configurar domínio via Square Cloud API
            success = await self.squarecloud_manager.set_domain(api_key, app_id, domain)
            if not success:
                logger.error(f"❌ Falha ao configurar domínio {domain} para aplicação {app_id}")
                return False
            
            # Salvar informações do domínio
            domain_record = {
                "app_id": app_id,
                "app_name": app_name,
                "domain": domain,
                "configured_at": datetime.now().isoformat(),
                "status": "active"
            }
            
            # Adicionar ao registro
            domain_id = f"{app_id}_{domain}"
            self.domain_data[domain_id] = domain_record
            self.save_domain_data()
            
            logger.info(f"✅ Domínio configurado: {domain} para aplicação {app_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao configurar domínio: {e}")
            return False
    
    async def remove_domain(self, api_key: str, app_id: str, domain: str) -> bool:
        """Remove um domínio personalizado de uma aplicação"""
        try:
            logger.info(f"🗑️ Removendo domínio {domain} da aplicação {app_id}")
            
            # Remover domínio via Square Cloud API
            success = await self.squarecloud_manager.remove_domain(api_key, app_id, domain)
            if not success:
                logger.error(f"❌ Falha ao remover domínio {domain} da aplicação {app_id}")
                return False
            
            # Remover do registro
            domain_id = f"{app_id}_{domain}"
            if domain_id in self.domain_data:
                del self.domain_data[domain_id]
                self.save_domain_data()
                logger.info(f"✅ Domínio removido do registro: {domain}")
            
            logger.info(f"✅ Domínio removido: {domain} da aplicação {app_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao remover domínio: {e}")
            return False
    
    async def list_domains(self, api_key: str, app_id: str = None) -> List[Dict]:
        """Lista domínios de uma aplicação ou todos"""
        try:
            if app_id:
                # Listar domínios de uma aplicação específica
                domains = await self.squarecloud_manager.list_domains(api_key, app_id)
                return domains or []
            else:
                # Listar todos os domínios registrados localmente
                return list(self.domain_data.values())
        except Exception as e:
            logger.error(f"Erro ao listar domínios: {e}")
            return []
    
    def get_domain_info(self, app_id: str, domain: str) -> Optional[Dict]:
        """Obtém informações de um domínio específico"""
        domain_id = f"{app_id}_{domain}"
        return self.domain_data.get(domain_id)
    
    def get_app_domains(self, app_id: str) -> List[Dict]:
        """Obtém todos os domínios de uma aplicação"""
        return [
            record for record in self.domain_data.values()
            if record.get("app_id") == app_id
        ]
    
    def validate_domain(self, domain: str) -> bool:
        """Valida formato de domínio"""
        import re
        
        # Padrão básico para validação de domínio
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        
        if not domain or len(domain) > 253:
            return False
        
        # Verificar se não começa ou termina com hífen
        if domain.startswith('-') or domain.endswith('-'):
            return False
        
        # Verificar se tem pelo menos um ponto (para TLD)
        if '.' not in domain:
            return False
        
        # Verificar se cada parte tem pelo menos 1 caractere
        parts = domain.split('.')
        for part in parts:
            if len(part) == 0 or len(part) > 63:
                return False
        
        return bool(re.match(pattern, domain))
    
    def get_domain_statistics(self) -> Dict:
        """Obtém estatísticas dos domínios"""
        try:
            total_domains = len(self.domain_data)
            active_domains = len([d for d in self.domain_data.values() if d.get("status") == "active"])
            
            # Contar aplicações únicas com domínios
            unique_apps = len(set(d.get("app_id") for d in self.domain_data.values()))
            
            return {
                "total": total_domains,
                "active": active_domains,
                "unique_apps": unique_apps,
                "average_per_app": total_domains / unique_apps if unique_apps > 0 else 0
            }
        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas: {e}")
            return {}
    
    def delete_domain_record(self, app_id: str, domain: str) -> bool:
        """Remove registro de domínio"""
        try:
            domain_id = f"{app_id}_{domain}"
            if domain_id in self.domain_data:
                del self.domain_data[domain_id]
                self.save_domain_data()
                logger.info(f"🗑️ Registro de domínio removido: {domain_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao remover registro de domínio: {e}")
            return False

# Instância global
domain_manager = None

def setup():
    """Configura o gerenciador de domínios"""
    global domain_manager
    domain_manager = DomainManager() 