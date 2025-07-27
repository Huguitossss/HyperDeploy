import json
import os
from typing import Optional, Dict
from core.logs.logger import logger

class UserKeysManager:
    def __init__(self):
        self.keys_file = "data/user_keys.json"
        self.user_keys: Dict[str, str] = {}
        self.load_keys()
    
    def load_keys(self):
        """Carrega chaves dos usuários do arquivo JSON"""
        try:
            if os.path.exists(self.keys_file):
                with open(self.keys_file, 'r', encoding='utf-8') as f:
                    self.user_keys = json.load(f)
                logger.info(f"{len(self.user_keys)} chaves de usuários carregadas")
            else:
                self.save_keys()
        except Exception as e:
            logger.error(f"Erro ao carregar chaves dos usuários: {e}")
            self.user_keys = {}
    
    def save_keys(self):
        """Salva chaves dos usuários no arquivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.keys_file), exist_ok=True)
            with open(self.keys_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_keys, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao salvar chaves dos usuários: {e}")
    
    def get_user_key(self, user_id: int) -> Optional[str]:
        """Obtém a chave da API de um usuário"""
        return self.user_keys.get(str(user_id))
    
    def set_user_key(self, user_id: int, api_key: str) -> bool:
        """Define a chave da API de um usuário"""
        try:
            if not api_key or api_key.strip() == "":
                logger.warning(f"Tentativa de salvar chave vazia para usuário {user_id}")
                return False
            
            self.user_keys[str(user_id)] = api_key.strip()
            self.save_keys()
            logger.info(f"Chave da API configurada para usuário {user_id}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar chave da API: {e}")
            return False
    
    def remove_user_key(self, user_id: int) -> bool:
        """Remove a chave da API de um usuário"""
        try:
            user_id_str = str(user_id)
            if user_id_str in self.user_keys:
                del self.user_keys[user_id_str]
                self.save_keys()
                logger.info(f"Chave da API removida para usuário {user_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao remover chave da API: {e}")
            return False
    
    def has_user_key(self, user_id: int) -> bool:
        """Verifica se um usuário tem chave configurada"""
        return str(user_id) in self.user_keys
    
    def get_all_users(self) -> Dict[str, str]:
        """Obtém todas as chaves dos usuários"""
        return self.user_keys.copy()
    
    def get_users_count(self) -> int:
        """Obtém o número de usuários com chaves configuradas"""
        return len(self.user_keys)
    
    def validate_api_key(self, api_key: str) -> bool:
        """Valida se a chave da API tem formato válido"""
        if not api_key or api_key.strip() == "":
            return False
        
        # Verificar se tem pelo menos 20 caracteres (chaves da Square Cloud são longas)
        if len(api_key.strip()) < 20:
            return False
        
        # Verificar se não contém espaços (chaves não devem ter espaços)
        if " " in api_key:
            return False
        
        return True

# Instância global
user_keys_manager = None

def setup():
    """Configura o gerenciador de chaves de usuários"""
    global user_keys_manager
    user_keys_manager = UserKeysManager() 