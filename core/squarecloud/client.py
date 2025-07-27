import yaml
import os
import asyncio
from typing import Optional, Dict, List
from squarecloud import Client, File
from core.logs.logger import logger

class SquareCloudManager:
    def __init__(self, api_key: str = None):
        self.config_file = "config/squarecloud.yaml"
        self.config = self.load_config()
        self.client = None
        self.api_key = api_key or self.config.get("api_key")
        
        if self.api_key and self.api_key != "SUA_API_KEY_SQUARECLOUD_AQUI":
            self.client = Client(self.api_key)
            logger.info("Cliente Square Cloud inicializado")
        else:
            logger.warning("API Key da Square Cloud não configurada")
    
    def load_config(self) -> Dict:
        """Carrega configurações da Square Cloud"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                logger.info("⚙️ Configurações Square Cloud carregadas")
                return config
            else:
                logger.error(f"❌ Arquivo de configuração não encontrado: {self.config_file}")
                return {}
        except Exception as e:
            logger.error(f"❌ Erro ao carregar configurações Square Cloud: {e}")
            return {}
    
    def get_client(self, api_key: Optional[str] = None) -> Optional[Client]:
        """Obtém cliente da Square Cloud"""
        if api_key:
            return Client(api_key)
        return self.client
    
    async def upload_app(self, api_key: str, zip_path: str) -> Dict:
        """Faz upload de uma aplicação para a Square Cloud"""
        try:
            if not os.path.exists(zip_path):
                return {"status": "error", "error": "Arquivo não encontrado"}
            
            client = self.get_client(api_key)
            if not client:
                return {"status": "error", "error": "Cliente não disponível"}
            
            file = File(zip_path)
            result = await client.upload_app(file=file)
            
            logger.info(f"Upload realizado: {result.id if hasattr(result, 'id') else 'N/A'}")
            return {"status": "success", "result": result}
            
        except Exception as e:
            logger.error(f"❌ Erro no upload: {e}")
            return {"status": "error", "error": str(e)}
    
    async def list_apps(self, api_key: str) -> List:
        """Lista todas as aplicações do usuário"""
        try:
            client = self.get_client(api_key)
            if not client:
                return []
            
            apps = await client.all_apps()
            return apps
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar aplicações: {e}")
            return []
    
    async def get_app_status(self, api_key: str, app_id: str) -> Optional[Dict]:
        """Obtém status de uma aplicação"""
        try:
            client = self.get_client(api_key)
            if not client:
                return None
            
            status = await client.app_status(app_id=app_id)
            return status
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter status da aplicação: {e}")
            return None
    
    async def start_app(self, api_key: str, app_id: str) -> bool:
        """Inicia uma aplicação"""
        try:
            client = self.get_client(api_key)
            if not client:
                return False
            
            await client.start_app(app_id=app_id)
            logger.info(f"🚀 Aplicação {app_id} iniciada")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar aplicação: {e}")
            return False
    
    async def stop_app(self, api_key: str, app_id: str) -> bool:
        """Para uma aplicação"""
        try:
            client = self.get_client(api_key)
            if not client:
                return False
            
            await client.stop_app(app_id=app_id)
            logger.info(f"⏹️ Aplicação {app_id} parada")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao parar aplicação: {e}")
            return False
    
    async def restart_app(self, api_key: str, app_id: str) -> bool:
        """Reinicia uma aplicação"""
        try:
            client = self.get_client(api_key)
            if not client:
                return False
            
            await client.restart_app(app_id=app_id)
            logger.info(f"🔄 Aplicação {app_id} reiniciada")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao reiniciar aplicação: {e}")
            return False
    
    async def delete_app(self, api_key: str, app_id: str) -> bool:
        """Deleta uma aplicação"""
        try:
            client = self.get_client(api_key)
            if not client:
                return False
            
            app = await client.app(app_id)
            await app.delete()
            logger.info(f"🗑️ Aplicação {app_id} deletada")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao deletar aplicação: {e}")
            return False
    
    async def get_app_logs(self, api_key: str, app_id: str) -> Optional[str]:
        """Obtém logs de uma aplicação"""
        try:
            client = self.get_client(api_key)
            if not client:
                return None
            
            logs = await client.get_logs(app_id=app_id)
            return logs
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter logs da aplicação: {e}")
            return None
    
    async def create_backup(self, api_key: str, app_id: str) -> Optional[Dict]:
        """Cria backup de uma aplicação"""
        try:
            client = self.get_client(api_key)
            if not client:
                return None
            
            backup_info = await client.backup(app_id)
            logger.info(f"📦 Backup criado para aplicação {app_id}")
            return backup_info
        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}")
            return None
    
    async def list_backups(self, api_key: str, app_id: str) -> List[Dict]:
        """Lista backups de uma aplicação"""
        try:
            client = self.get_client(api_key)
            if not client:
                return []
            
            backups = await client.all_app_backups(app_id=app_id)
            logger.info(f"📦 {len(backups)} backups encontrados para aplicação {app_id}")
            return backups
        except Exception as e:
            logger.error(f"Erro ao listar backups: {e}")
            return []
    
    async def download_backup(self, api_key: str, backup_id: str, app_id: str) -> Optional[bytes]:
        """Download de um backup específico"""
        try:
            client = self.get_client(api_key)
            if not client:
                return None
            
            backup_data = await client.download_backup(app_id, backup_id)
            logger.info(f"📥 Backup {backup_id} baixado com sucesso")
            return backup_data
        except Exception as e:
            logger.error(f"Erro ao baixar backup: {e}")
            return None
    
    async def upload_app(self, api_key: str, file_path: str, app_name: str = None) -> Optional[str]:
        """Upload de uma aplicação (para restore de backup)"""
        try:
            client = self.get_client(api_key)
            if not client:
                return None
            
            # Se não foi especificado nome, usar nome do arquivo
            if not app_name:
                app_name = os.path.splitext(os.path.basename(file_path))[0]
            
            app_info = await client.upload_app(file_path, app_name)
            app_id = app_info.get("id")
            
            if app_id:
                logger.info(f"🚀 Aplicação restaurada: {app_id} ({app_name})")
                return app_id
            else:
                logger.error("❌ Falha ao obter ID da aplicação restaurada")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao fazer upload da aplicação: {e}")
            return None

    async def set_domain(self, api_key: str, app_id: str, domain: str) -> bool:
        """Configura um domínio personalizado para uma aplicação"""
        try:
            client = self.get_client(api_key)
            if not client:
                return False
            
            await client.set_domain(app_id, domain)
            logger.info(f"🌐 Domínio configurado: {domain} para aplicação {app_id}")
            return True
        except Exception as e:
            logger.error(f"Erro ao configurar domínio: {e}")
            return False
    
    async def remove_domain(self, api_key: str, app_id: str, domain: str) -> bool:
        """Remove um domínio personalizado de uma aplicação"""
        try:
            client = self.get_client(api_key)
            if not client:
                return False
            
            await client.remove_domain(app_id, domain)
            logger.info(f"🗑️ Domínio removido: {domain} da aplicação {app_id}")
            return True
        except Exception as e:
            logger.error(f"Erro ao remover domínio: {e}")
            return False
    
    async def list_domains(self, api_key: str, app_id: str) -> List[Dict]:
        """Lista domínios de uma aplicação"""
        try:
            client = self.get_client(api_key)
            if not client:
                return []
            
            domains = await client.domains(app_id)
            logger.info(f"🌐 {len(domains)} domínios encontrados para aplicação {app_id}")
            return domains
        except Exception as e:
            logger.error(f"Erro ao listar domínios: {e}")
            return []

# Instância global
squarecloud_manager = None

def setup(api_key: str):
    global squarecloud_manager
    squarecloud_manager = SquareCloudManager(api_key)
