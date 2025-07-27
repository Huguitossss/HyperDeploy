# 🤝 Guia de Contribuição - HyperDeploy

Obrigado por considerar contribuir com o HyperDeploy! Este documento fornece diretrizes e informações para contribuir com o projeto.

## 📋 Índice

- [Como Contribuir](#como-contribuir)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Padrões de Código](#padrões-de-código)
- [Processo de Desenvolvimento](#processo-de-desenvolvimento)
- [Reportando Bugs](#reportando-bugs)
- [Solicitando Funcionalidades](#solicitando-funcionalidades)
- [Pull Requests](#pull-requests)
- [Código de Conduta](#código-de-conduta)

## 🚀 Como Contribuir

### Tipos de Contribuição
- 🐛 **Reportar bugs** - Ajude a identificar problemas
- 💡 **Sugerir funcionalidades** - Proponha melhorias
- 🔧 **Corrigir bugs** - Implemente correções
- ✨ **Adicionar funcionalidades** - Desenvolva novas features
- 📚 **Melhorar documentação** - Atualize docs e exemplos
- 🧪 **Testes** - Adicione ou melhore testes

### Antes de Começar
1. **Verifique se já existe uma issue** para o que você quer fazer
2. **Leia a documentação** completa do projeto
3. **Entenda a arquitetura** e padrões utilizados
4. **Configure o ambiente** de desenvolvimento

## 🔧 Configuração do Ambiente

### Pré-requisitos
- Python 3.11+
- Git
- Conta Discord Developer
- Conta Square Cloud
- Conta Mercado Pago (opcional)

### 1. Fork e Clone
```bash
# Fork o repositório no GitHub
# Clone seu fork
git clone https://github.com/seu-usuario/HyperDeploy.git
cd HyperDeploy

# Adicione o repositório original como upstream
git remote add upstream https://github.com/original/HyperDeploy.git
```

### 2. Ambiente Virtual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Ativar ambiente (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configuração
```bash
# Copiar arquivos de configuração
cp config/bot.yaml.example config/bot.yaml
cp config/squarecloud.yaml.example config/squarecloud.yaml

# Editar configurações
# Adicione seus tokens e configurações
```

### 4. Testes
```bash
# Executar testes básicos
python -m pytest tests/

# Verificar sintaxe
python -m py_compile bot.py
python -m py_compile core/commands/admin_panel.py
python -m py_compile core/commands/userpanel.py
```

## 📝 Padrões de Código

### Estrutura do Projeto
```
HyperDeploy/
├── bot.py                          # Bot principal
├── config/                         # Configurações
│   ├── bot.yaml                   # Configurações do bot
│   └── squarecloud.yaml           # Configurações Square Cloud
├── core/                          # Módulos principais
│   ├── commands/                  # Comandos slash
│   ├── payments/                  # Sistema de pagamentos
│   ├── tickets/                   # Sistema de tickets
│   ├── squarecloud/               # Integração Square Cloud
│   └── logs/                      # Sistema de logs
├── data/                          # Dados persistentes
├── uploads/                       # Arquivos temporários
├── qrcodes/                       # QR Codes gerados
├── docs/                          # Documentação
├── tests/                         # Testes
├── requirements.txt               # Dependências
└── README.md                      # Documentação principal
```

### Convenções de Nomenclatura

#### Arquivos e Diretórios
- **snake_case** para arquivos Python
- **kebab-case** para documentação
- **PascalCase** para classes
- **camelCase** para variáveis JavaScript (se houver)

#### Variáveis e Funções
```python
# ✅ Correto
user_id = 123456789
payment_amount = 25.00
async def create_ticket():
    pass

# ❌ Incorreto
userId = 123456789
paymentAmount = 25.00
async def CreateTicket():
    pass
```

#### Classes
```python
# ✅ Correto
class TicketManager:
    def __init__(self, bot):
        self.bot = bot

# ❌ Incorreto
class ticket_manager:
    def __init__(self, bot):
        self.bot = bot
```

### Documentação de Código

#### Docstrings
```python
async def create_payment(user_id: int, amount: float, description: str = "Deploy") -> str:
    """
    Cria um novo pagamento PIX.
    
    Args:
        user_id (int): ID do usuário Discord
        amount (float): Valor do pagamento
        description (str, optional): Descrição do pagamento. Defaults to "Deploy".
    
    Returns:
        str: ID do pagamento criado
        
    Raises:
        ValueError: Se o valor for inválido
        Exception: Se houver erro na criação
    """
    pass
```

#### Comentários
```python
# ✅ Comentários úteis
# Verificar se o usuário tem permissão administrativa
if not ctx.author.guild_permissions.administrator:
    await ctx.respond("❌ Permissão negada", ephemeral=True)
    return

# ❌ Comentários óbvios
# Criar variável
user_id = ctx.author.id
```

### Tratamento de Erros
```python
try:
    # Código que pode gerar erro
    result = await api_call()
except discord.errors.NotFound:
    # Erro específico do Discord
    logger.warning("Canal não encontrado")
    await ctx.respond("❌ Canal não encontrado", ephemeral=True)
except Exception as e:
    # Erro genérico
    logger.error(f"Erro inesperado: {e}")
    await ctx.respond("❌ Erro interno", ephemeral=True)
```

### Logging
```python
import logging

logger = logging.getLogger(__name__)

# ✅ Logs informativos
logger.info(f"Ticket criado: {ticket_id} para {user_id}")

# ✅ Logs de erro
logger.error(f"Erro ao criar ticket: {e}")

# ✅ Logs de debug
logger.debug(f"Configuração carregada: {config}")
```

## 🔄 Processo de Desenvolvimento

### 1. Escolher uma Issue
- Verifique a lista de issues no GitHub
- Escolha uma issue com a label `good first issue` se for sua primeira contribuição
- Comente na issue que você vai trabalhar nela

### 2. Criar Branch
```bash
# Atualizar branch principal
git checkout main
git pull upstream main

# Criar branch para sua feature
git checkout -b feature/nome-da-feature
# ou
git checkout -b fix/nome-do-bug
```

### 3. Desenvolver
- Implemente sua funcionalidade
- Siga os padrões de código
- Adicione testes se necessário
- Atualize documentação

### 4. Commits
```bash
# Commits atômicos e descritivos
git commit -m "feat: adicionar sistema de backup automático"
git commit -m "fix: corrigir erro de timeout em tickets"
git commit -m "docs: atualizar guia de deploy"
git commit -m "test: adicionar testes para payment manager"
```

### 5. Push e Pull Request
```bash
# Push para seu fork
git push origin feature/nome-da-feature

# Criar Pull Request no GitHub
```

## 🐛 Reportando Bugs

### Antes de Reportar
1. **Verifique se já existe uma issue** para o bug
2. **Teste com a versão mais recente** do código
3. **Reproduza o bug** consistentemente
4. **Verifique logs** para informações de erro

### Template de Bug Report
```markdown
## 🐛 Descrição do Bug

Descrição clara e concisa do bug.

## 🔄 Passos para Reproduzir

1. Vá para '...'
2. Clique em '...'
3. Role até '...'
4. Veja o erro

## ✅ Comportamento Esperado

Descrição do que deveria acontecer.

## 📸 Screenshots

Se aplicável, adicione screenshots.

## 🔧 Informações do Sistema

- **Versão do HyperDeploy**: 1.0.7
- **Python**: 3.11.8
- **Discord.py**: 2.6.1
- **Sistema Operacional**: Windows 10
- **Navegador**: Chrome 120.0

## 📋 Logs

```
Logs relevantes aqui
```

## 💡 Contexto Adicional

Qualquer informação adicional sobre o problema.
```

## 💡 Solicitando Funcionalidades

### Template de Feature Request
```markdown
## 💡 Descrição da Funcionalidade

Descrição clara da funcionalidade desejada.

## 🎯 Problema que Resolve

Explicação de como a funcionalidade resolve um problema.

## 💭 Solução Proposta

Descrição da solução proposta.

## 🔄 Alternativas Consideradas

Outras soluções que foram consideradas.

## 📋 Contexto Adicional

Qualquer contexto adicional.
```

## 🔀 Pull Requests

### Checklist do PR
- [ ] Código segue os padrões do projeto
- [ ] Funcionalidade testada localmente
- [ ] Documentação atualizada
- [ ] Testes adicionados (se aplicável)
- [ ] Commits atômicos e descritivos
- [ ] Branch atualizada com main

### Template do PR
```markdown
## 📝 Descrição

Descrição das mudanças implementadas.

## 🔗 Issue Relacionada

Closes #123

## ✅ Checklist

- [ ] Código testado localmente
- [ ] Documentação atualizada
- [ ] Testes passando
- [ ] Sem conflitos de merge

## 📸 Screenshots

Se aplicável, adicione screenshots.

## 🔧 Como Testar

Instruções para testar as mudanças.
```

### Review Process
1. **Automatic Checks** - CI/CD verifica o código
2. **Code Review** - Mantenedores revisam o código
3. **Testing** - Funcionalidade testada
4. **Merge** - PR aprovado e mergeado

## 📚 Documentação

### Atualizando Documentação
- **README.md** - Documentação principal
- **docs/DEPLOY_GUIDE.md** - Guia de deploy
- **docs/API_REFERENCE.md** - Referência da API
- **docs/CHANGELOG.md** - Histórico de mudanças

### Padrões de Documentação
- Use Markdown
- Inclua exemplos de código
- Mantenha estrutura consistente
- Atualize quando necessário

## 🧪 Testes

### Executando Testes
```bash
# Testes unitários
python -m pytest tests/unit/

# Testes de integração
python -m pytest tests/integration/

# Todos os testes
python -m pytest tests/

# Com cobertura
python -m pytest tests/ --cov=core
```

### Escrevendo Testes
```python
import pytest
from core.payments.manager import PaymentManager

class TestPaymentManager:
    def test_create_payment(self):
        manager = PaymentManager()
        payment_id = manager.create_payment(123, 25.00, "Test")
        assert payment_id is not None
        assert payment_id.startswith("pix_")
```

## 🚀 Deploy e Distribuição

### Testando Localmente
```bash
# Executar bot localmente
python bot.py

# Verificar logs
tail -f logs/hyperdeploy.log
```

### Deploy de Teste
1. Configure ambiente de teste
2. Teste funcionalidades
3. Verifique logs
4. Valide integrações

## 📞 Comunicação

### Canais de Comunicação
- **GitHub Issues** - Bugs e funcionalidades
- **GitHub Discussions** - Discussões gerais
- **Discord - #hugo_dsa** - Suporte e comunidade 

### Etiquetas de Issues
- `bug` - Problemas no código
- `enhancement` - Melhorias
- `documentation` - Documentação
- `good first issue` - Boas para iniciantes
- `help wanted` - Precisa de ajuda
- `question` - Perguntas

## 📋 Código de Conduta

### Nossos Padrões
- Seja respeitoso e inclusivo
- Use linguagem apropriada
- Aceite críticas construtivas
- Foque no que é melhor para a comunidade

### Nossas Responsabilidades
- Manter ambiente acolhedor
- Resolver conflitos de forma justa
- Remover conteúdo inadequado
- Comunicar mudanças importantes

### Aplicação
- Reporte comportamento inadequado
- Mantenedores investigarão e responderão
- Ações apropriadas serão tomadas

## 🏆 Reconhecimento

### Contribuidores
- Seu nome será adicionado ao README
- Contribuições serão reconhecidas
- Agradecimentos especiais para contribuições significativas

### Tipos de Contribuição
- **Código** - Implementação de funcionalidades
- **Documentação** - Melhorias na documentação
- **Testes** - Adição de testes
- **Bug Reports** - Identificação de problemas
- **Feature Requests** - Sugestões de melhorias

## 📞 Suporte

### Precisa de Ajuda?
- Abra uma issue no GitHub
- Participe das discussões
- Entre em contato via Discord
- Consulte a documentação

### Recursos Úteis
- [Documentação Discord.py](https://discordpy.readthedocs.io/)
- [Documentação Square Cloud](https://docs.squarecloud.app/)
- [Documentação Mercado Pago](https://developers.mercadopago.com/)

---

**Obrigado por contribuir com o HyperDeploy!** 🚀

*Você também tem livre direito de usar o projeto e melhorá-lo caso queira.*
