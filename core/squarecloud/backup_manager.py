import os
import json
import asyncio
import discord
import aiohttp
import aiofiles
from datetime import datetime
from typing import Dict, List, Optional
from core.logs.logger import logger
from core.squarecloud.client import SquareCloudManager

class BackupManager:
    def __init__(self):
        self.backup_folder = "backups"
        self.backup_data_file = "data/backups.json"
        self.backup_data: Dict = {}
        self.squarecloud_manager = SquareCloudManager()
        self.ensure_backup_folder()
        self.load_backup_data()
    
    def ensure_backup_folder(self):
        """Garante que a pasta de backups existe"""
        if not os.path.exists(self.backup_folder):
            os.makedirs(self.backup_folder, exist_ok=True)
            logger.info(f"Pasta de backups criada: {self.backup_folder}")
    
    def load_backup_data(self):
        """Carrega dados de backup do arquivo JSON"""
        try:
            if os.path.exists(self.backup_data_file):
                with open(self.backup_data_file, 'r', encoding='utf-8') as f:
                    self.backup_data = json.load(f)
                logger.info(f"📦 {len(self.backup_data)} registros de backup carregados")
            else:
                self.save_backup_data()
        except Exception as e:
            logger.error(f"Erro ao carregar dados de backup: {e}")
            self.backup_data = {}
    
    def save_backup_data(self):
        """Salva dados de backup no arquivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.backup_data_file), exist_ok=True)
            with open(self.backup_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.backup_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao salvar dados de backup: {e}")
    
    async def create_backup(self, api_key: str, app_id: str, app_name: str = "Aplicação") -> Optional[Dict]:
        """Cria backup de uma aplicação"""
        try:
            logger.info(f"📦 Iniciando backup da aplicação {app_id}")
            
            # Criar backup via Square Cloud API
            backup_info = await self.squarecloud_manager.create_backup(api_key, app_id)
            if not backup_info:
                logger.error(f"❌ Falha ao criar backup da aplicação {app_id}")
                return None
            
            # Gerar nome único para o arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_app_name = "".join(c for c in app_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            backup_filename = f"{safe_app_name}_{timestamp}.zip"
            backup_path = os.path.join(self.backup_folder, backup_filename)
            
            # Salvar informações do backup
            backup_record = {
                "id": backup_info.get("id"),
                "app_id": app_id,
                "app_name": app_name,
                "filename": backup_filename,
                "file_path": backup_path,
                "created_at": datetime.now().isoformat(),
                "size_bytes": 0,
                "status": "created"
            }
            
            # Adicionar ao registro
            backup_id = f"{app_id}_{timestamp}"
            self.backup_data[backup_id] = backup_record
            self.save_backup_data()
            
            logger.info(f"✅ Backup criado: {backup_filename} para aplicação {app_id}")
            return backup_record
            
        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}")
            return None
    
    async def list_backups(self, api_key: str, app_id: str = None) -> List[Dict]:
        """Lista backups de uma aplicação ou todos"""
        try:
            if app_id:
                # Listar backups de uma aplicação específica
                backups = await self.squarecloud_manager.list_backups(api_key, app_id)
                return backups or []
            else:
                # Listar todos os backups registrados localmente
                return list(self.backup_data.values())
        except Exception as e:
            logger.error(f"Erro ao listar backups: {e}")
            return []
    
    async def download_backup(self, api_key: str, backup_id: str, app_id: str) -> Optional[str]:
        """Download de um backup específico"""
        try:
            logger.info(f"📥 Iniciando download do backup {backup_id}")
            
            # Buscar informações do backup
            backup_record = None
            for record in self.backup_data.values():
                if record.get("id") == backup_id:
                    backup_record = record
                    break
            
            if not backup_record:
                logger.error(f"❌ Backup {backup_id} não encontrado")
                return None
            
            # Download do backup
            backup_data = await self.squarecloud_manager.download_backup(api_key, backup_id, app_id)
            if not backup_data:
                logger.error(f"❌ Falha no download do backup {backup_id}")
                return None
            
            # Salvar arquivo localmente
            backup_path = backup_record["file_path"]
            async with aiofiles.open(backup_path, 'wb') as f:
                await f.write(backup_data)
            
            # Atualizar informações
            backup_record["size_bytes"] = len(backup_data)
            backup_record["status"] = "downloaded"
            backup_record["downloaded_at"] = datetime.now().isoformat()
            self.save_backup_data()
            
            logger.info(f"✅ Backup baixado: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Erro ao baixar backup: {e}")
            return None
    
    async def restore_backup(self, api_key: str, backup_path: str, app_name: str = None) -> Optional[str]:
        """Restaura um backup para uma nova aplicação"""
        try:
            logger.info(f"🔄 Iniciando restauração do backup: {backup_path}")
            
            if not os.path.exists(backup_path):
                logger.error(f"❌ Arquivo de backup não encontrado: {backup_path}")
                return None
            
            # Upload do backup como nova aplicação
            app_id = await self.squarecloud_manager.upload_app(api_key, backup_path, app_name)
            if not app_id:
                logger.error(f"❌ Falha na restauração do backup")
                return None
            
            logger.info(f"✅ Backup restaurado como aplicação: {app_id}")
            return app_id
            
        except Exception as e:
            logger.error(f"Erro ao restaurar backup: {e}")
            return None
    
    def get_backup_info(self, backup_id: str) -> Optional[Dict]:
        """Obtém informações de um backup"""
        return self.backup_data.get(backup_id)
    
    def delete_backup_record(self, backup_id: str) -> bool:
        """Remove registro de backup"""
        try:
            if backup_id in self.backup_data:
                backup_record = self.backup_data[backup_id]
                
                # Remover arquivo físico se existir
                file_path = backup_record.get("file_path")
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"🗑️ Arquivo de backup removido: {file_path}")
                
                # Remover do registro
                del self.backup_data[backup_id]
                self.save_backup_data()
                
                logger.info(f"🗑️ Registro de backup removido: {backup_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao remover backup: {e}")
            return False
    
    def get_backup_statistics(self) -> Dict:
        """Obtém estatísticas dos backups"""
        try:
            total_backups = len(self.backup_data)
            downloaded_backups = len([b for b in self.backup_data.values() if b.get("status") == "downloaded"])
            total_size = sum(b.get("size_bytes", 0) for b in self.backup_data.values())
            
            return {
                "total": total_backups,
                "downloaded": downloaded_backups,
                "total_size_mb": total_size / (1024 * 1024),
                "average_size_mb": (total_size / total_backups / (1024 * 1024)) if total_backups > 0 else 0
            }
        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas: {e}")
            return {}

# Instância global
backup_manager = None

def setup():
    global backup_manager
    backup_manager = BackupManager() 