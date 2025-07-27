import json
import os
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from core.logs.logger import logger

class PaymentManager:
    def __init__(self):
        self.payments_file = "data/payments.json"
        self.payments: Dict[str, Dict] = {}
        self.load_payments()
    
    def load_payments(self):
        """Carrega pagamentos salvos do arquivo JSON"""
        try:
            if os.path.exists(self.payments_file):
                with open(self.payments_file, 'r', encoding='utf-8') as f:
                    self.payments = json.load(f)
                logger.info(f"{len(self.payments)} pagamentos carregados")
            else:
                self.save_payments()
        except Exception as e:
            logger.error(f"Erro ao carregar pagamentos: {e}")
            self.payments = {}
    
    def save_payments(self):
        """Salva pagamentos no arquivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.payments_file), exist_ok=True)
            with open(self.payments_file, 'w', encoding='utf-8') as f:
                json.dump(self.payments, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao salvar pagamentos: {e}")
    
    def create_payment(self, user_id: int, amount: float, description: str = "Deploy HyperDeploy") -> str:
        """Cria um novo pagamento"""
        try:
            payment_id = f"pix_{user_id}_{int(datetime.now().timestamp())}"
            
            # Obter timeout configurado do config_manager
            from core.payments.config_manager import config_manager
            timeout_minutes = config_manager.get_payment_timeout_minutes() if config_manager else 30
            
            payment_info = {
                "id": payment_id,
                "user_id": user_id,
                "amount": amount,
                "description": description,
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(minutes=timeout_minutes)).isoformat(),
                "paid_at": None,
                "qr_code_path": None,
                "pix_key": None,
                "deploy_file": None
            }
            
            self.payments[payment_id] = payment_info
            self.save_payments()
            
            logger.info(f"Pagamento criado: {payment_id} - R$ {amount:.2f} (expira em {timeout_minutes} min)")
            return payment_id
            
        except Exception as e:
            logger.error(f"Erro ao criar pagamento: {e}")
            return None
    
    def get_payment(self, payment_id: str) -> Optional[Dict]:
        """Obtém informações de um pagamento"""
        return self.payments.get(payment_id)
    
    def update_payment_status(self, payment_id: str, status: str, additional_info: Dict = None):
        """Atualiza status de um pagamento"""
        try:
            if payment_id not in self.payments:
                logger.error(f"Pagamento não encontrado: {payment_id}")
                return False
            
            payment = self.payments[payment_id]
            payment["status"] = status
            
            if status == "paid":
                payment["paid_at"] = datetime.now().isoformat()
            
            if additional_info:
                payment.update(additional_info)
            
            self.save_payments()
            
            logger.info(f"Status atualizado: {payment_id} -> {status}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao atualizar status do pagamento: {e}")
            return False
    
    def get_payments_by_user(self, user_id: int) -> List[Dict]:
        """Obtém pagamentos de um usuário"""
        return [
            payment for payment in self.payments.values()
            if payment.get("user_id") == user_id
        ]
    
    def get_payments_by_status(self, status: str) -> List[Dict]:
        """Obtém pagamentos por status"""
        return [
            payment for payment in self.payments.values()
            if payment.get("status") == status
        ]
    
    def get_pending_payments(self) -> List[Dict]:
        """Obtém pagamentos pendentes"""
        return self.get_payments_by_status("pending")
    
    def get_paid_payments(self) -> List[Dict]:
        """Obtém pagamentos pagos"""
        return self.get_payments_by_status("paid")
    
    def get_expired_payments(self) -> List[Dict]:
        """Obtém pagamentos expirados"""
        expired_payments = []
        current_time = datetime.now()
        
        for payment in self.payments.values():
            if payment.get("status") == "pending":
                expires_at = datetime.fromisoformat(payment["expires_at"])
                if current_time > expires_at:
                    expired_payments.append(payment)
        
        return expired_payments
    
    def cleanup_expired_payments(self):
        """Remove pagamentos expirados"""
        try:
            expired_payments = self.get_expired_payments()
            
            for payment in expired_payments:
                payment_id = payment["id"]
                self.update_payment_status(payment_id, "expired")
                
                # Remover QR Code se existir
                qr_code_path = payment.get("qr_code_path")
                if qr_code_path and os.path.exists(qr_code_path):
                    os.remove(qr_code_path)
                    logger.info(f"🗑️ QR Code removido: {qr_code_path}")
            
            if expired_payments:
                logger.info(f"🧹 {len(expired_payments)} pagamentos expirados processados")
                
        except Exception as e:
            logger.error(f"Erro na limpeza de pagamentos: {e}")
    
    def get_payment_statistics(self) -> Dict:
        """Obtém estatísticas dos pagamentos"""
        try:
            total_payments = len(self.payments)
            pending_payments = len(self.get_pending_payments())
            paid_payments = len(self.get_paid_payments())
            expired_payments = len(self.get_expired_payments())
            
            total_amount = sum(
                payment["amount"] for payment in self.payments.values()
                if payment.get("status") == "paid"
            )
            
            return {
                "total": total_payments,
                "pending": pending_payments,
                "paid": paid_payments,
                "expired": expired_payments,
                "total_amount": total_amount,
                "success_rate": (paid_payments / total_payments * 100) if total_payments > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas: {e}")
            return {}
    
    def add_deploy_file(self, payment_id: str, file_path: str):
        """Adiciona arquivo de deploy ao pagamento"""
        try:
            if payment_id in self.payments:
                self.payments[payment_id]["deploy_file"] = file_path
                self.save_payments()
                logger.info(f"📁 Arquivo de deploy adicionado ao pagamento {payment_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Erro ao adicionar arquivo de deploy: {e}")
            return False
    
    def get_deploy_file(self, payment_id: str) -> Optional[str]:
        """Obtém arquivo de deploy de um pagamento"""
        payment = self.get_payment(payment_id)
        return payment.get("deploy_file") if payment else None
    
    def mark_payment_for_deploy(self, payment_id: str):
        """Marca pagamento para deploy"""
        try:
            if payment_id in self.payments:
                self.payments[payment_id]["deploy_ready"] = True
                self.payments[payment_id]["deploy_ready_at"] = datetime.now().isoformat()
                self.save_payments()
                logger.info(f"🚀 Pagamento {payment_id} marcado para deploy")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Erro ao marcar pagamento para deploy: {e}")
            return False
    
    def get_payments_ready_for_deploy(self) -> List[Dict]:
        """Obtém pagamentos prontos para deploy"""
        return [
            payment for payment in self.payments.values()
            if payment.get("status") == "paid" and payment.get("deploy_ready") and payment.get("deploy_file")
        ]
    
    def complete_deploy(self, payment_id: str, success: bool = True):
        """Marca deploy como concluído"""
        try:
            if payment_id in self.payments:
                self.payments[payment_id]["deploy_completed"] = True
                self.payments[payment_id]["deploy_completed_at"] = datetime.now().isoformat()
                self.payments[payment_id]["deploy_success"] = success
                self.save_payments()
                
                status = "✅" if success else "❌"
                logger.info(f"{status} Deploy concluído para pagamento {payment_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Erro ao marcar deploy como concluído: {e}")
            return False
    
    def get_recent_payments(self, hours: int = 24) -> List[Dict]:
        """Obtém pagamentos recentes"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_payments = []
            
            for payment in self.payments.values():
                created_at = datetime.fromisoformat(payment["created_at"])
                if created_at > cutoff_time:
                    recent_payments.append(payment)
            
            return recent_payments
            
        except Exception as e:
            logger.error(f"Erro ao obter pagamentos recentes: {e}")
            return []
    
    async def cleanup_loop(self):
        """Loop de limpeza automática de pagamentos"""
        while True:
            try:
                self.cleanup_expired_payments()
                await asyncio.sleep(300)  # Verificar a cada 5 minutos
            except Exception as e:
                logger.error(f"Erro no loop de limpeza de pagamentos: {e}")
                await asyncio.sleep(60)

# Instância global
payment_manager = None

def setup():
    """Configura o gerenciador de pagamentos"""
    global payment_manager
    payment_manager = PaymentManager()
