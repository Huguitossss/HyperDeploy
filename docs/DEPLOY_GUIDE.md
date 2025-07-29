# 🚀 Guia Completo de Deploy - HyperDeploy

Guia detalhado para fazer deploy do HyperDeploy na Square Cloud e configurar o ambiente de produção.

## 📋 Pré-requisitos

### Contas Necessárias
- ✅ **Discord Developer** - Para criar o bot
- ✅ **Square Cloud** - Para hospedar o bot
- ✅ **Mercado Pago** - Para pagamentos PIX
- ✅ **GitHub** - Para repositório do código

### Recursos Técnicos
- **Python 3.11+** - Versão suportada
- **512MB RAM** - Mínimo recomendado
- **1GB Storage** - Para arquivos e logs
- **Conexão estável** - Para APIs externas

## 🔧 Configuração do Bot Discord

### 1. Criar Aplicação Discord
1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique em "New Application"
3. Digite o nome: `HyperDeploy`
4. Clique em "Create"

### 2. Configurar Bot
1. Vá na aba "Bot"
2. Clique em "Add Bot"
3. Em "Privileged Gateway Intents", ative:
   - ✅ **Message Content Intent**
   - ✅ **Server Members Intent**
   - ✅ **Presence Intent**
4. Copie o **Token** (será usado depois)

### 3. Configurar Permissões
1. Vá na aba "OAuth2" → "URL Generator"
2. Selecione os escopos:
   - ✅ **bot**
   - ✅ **applications.commands**
3. Selecione as permissões:
   - ✅ **Administrator** (ou permissões específicas)
   - ✅ **Send Messages**
   - ✅ **Manage Channels**
   - ✅ **Manage Messages**
   - ✅ **Attach Files**
   - ✅ **Embed Links**
   - ✅ **Use Slash Commands**
4. Copie a URL gerada e adicione o bot ao seu servidor

### 4. Obter IDs
1. **Guild ID**: Clique com botão direito no servidor → "Copy Server ID"
2. **Client ID**: Vá em "General Information" → "Application ID"

## 💳 Configuração Mercado Pago

### 1. Criar Conta
1. Acesse [Mercado Pago](https://www.mercadopago.com.br/)
2. Crie uma conta ou faça login
3. Vá em "Desenvolvedores" → "Minhas aplicações"

### 2. Criar Aplicação
1. Clique em "Criar aplicação"
2. Preencha os dados:
   - **Nome**: HyperDeploy
   - **Descrição**: Bot Discord para Square Cloud
   - **Categoria**: Outros
3. Clique em "Criar"

### 3. Gerar Access Token
1. Vá em "Credenciais"
2. Clique em "Gerar token de teste"
3. Copie o **Access Token** gerado

### 4. Configurar Webhook (Opcional)
1. Vá em "Webhooks"
2. Adicione URL: `https://seu-dominio.com/webhook`
3. Selecione eventos: `payment.created`, `payment.updated`

## ☁️ Configuração Square Cloud

### 1. Criar Conta
1. Acesse [Square Cloud](https://squarecloud.app)
2. Faça login com Discord
3. Complete o perfil

### 2. Obter API Key
1. Vá em "Settings" → "API"
2. Clique em "Generate API Key"
3. Copie a **API Key** gerada

### 3. Configurar Aplicação
1. Clique em "New Application"
2. Escolha "From GitHub"
3. Selecione seu repositório
4. Configure:
   - **Name**: HyperDeploy
   - **Description**: Bot Discord para Square Cloud
   - **Main File**: `bot.py`
   - **Memory**: 512MB
   - **Version**: recommended

## 📁 Preparação do Repositório

### 1. Estrutura de Arquivos
```
HyperDeploy/
├── bot.py                          # Bot principal
├── config/                         # Configurações
│   ├── bot.yaml                   # Configurações do bot
│   └── squarecloud.yaml           # Configurações Square Cloud
├── core/                          # Módulos principais
├── data/                          # Dados persistentes
├── uploads/                       # Arquivos temporários
├── qrcodes/                       # QR Codes gerados
├── docs/                          # Documentação
├── requirements.txt               # Dependências
├── squarecloud.config             # Configuração Square Cloud
└── README.md                      # Documentação principal
```

### 2. Arquivo squarecloud.config
```ini
DISPLAY_NAME=HyperDeploy
DESCRIPTION=Bot Discord profissional para Square Cloud
MAIN=bot.py
MEMORY=512
VERSION=recommended
RESTART=true
AUTORESTART=true
```

### 3. Arquivo requirements.txt
```
discord.py>=2.6.1
squarecloud-api>=3.7.3
aiohttp>=3.8.0
pillow>=10.0.0
pyyaml>=6.0
```

### 4. Configurações YAML

#### config/bot.yaml
```yaml
# Discord Bot Configuration
bot_token: "SEU_TOKEN_DISCORD_AQUI"
guild_id: SEU_GUILD_ID_AQUI
client_id: SEU_CLIENT_ID_AQUI

# Mercado Pago Configuration
mercadopago_access_token: "SEU_ACCESS_TOKEN_MERCADOPAGO_AQUI"

# Bot Configuration
bot_version: "1.0.7"
bot_name: "HyperDeploy"
bot_description: "Bot Discord para Square Cloud"

# System Configuration
max_file_size: "150MB"              # Tamanho máximo de arquivo
ticket_timeout: 30                  # Timeout dos tickets (minutos)
payment_timeout: 30                 # Timeout dos pagamentos (minutos)
auto_deploy: true                   # Deploy automático
mercadopago_enabled: true           # Habilitar Mercado Pago

# Log Channels (opcional)
log_channels:
  actions: null                     # Canal para logs de ações
  admin: null                       # Canal para logs administrativos
  payments: null                    # Canal para logs de pagamentos
  deploys: null                     # Canal para logs de deploys
```

#### config/squarecloud.yaml
```yaml
# Square Cloud API Configuration
api_key: "SUA_API_KEY_SQUARECLOUD_AQUI"

# API Settings
base_url: "https://api.squarecloud.app/v2"
timeout: 60                         # Timeout das requisições (segundos)
retry_attempts: 3                   # Tentativas de retry
retry_delay: 5                      # Delay entre tentativas (segundos)

# Application Settings
default_memory: 512                 # Memória padrão (MB)
default_cpu: 25                     # CPU padrão (%)
default_disk: 1024                  # Disco padrão (MB)
max_file_size_mb: 150              # Tamanho máximo do arquivo ZIP

# Backup Settings
backup_enabled: true                # Habilitar backups
backup_interval: 24                 # Intervalo de backup (horas)
backup_retention: 7                 # Retenção de backups (dias)

# Domain Settings
domain_enabled: true                # Habilitar domínios
domain_ssl: true                    # SSL automático
domain_redirect: false              # Redirecionamento automático
```

## 🚀 Deploy na Square Cloud

### 1. Upload via GitHub
1. Faça push do código para GitHub
2. Acesse [Square Cloud](https://squarecloud.app)
3. Clique em "New Application"
4. Escolha "From GitHub"
5. Selecione seu repositório
6. Clique em "Create"

### 2. Configurar Variáveis de Ambiente
No painel da Square Cloud, vá em "Settings" → "Environment Variables":

```env
# Discord Bot
BOT_TOKEN=seu_token_discord_aqui
GUILD_ID=seu_guild_id_aqui
CLIENT_ID=seu_client_id_aqui

# Square Cloud
SQUARECLOUD_API_KEY=sua_api_key_aqui

# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=seu_access_token_aqui

# Configurações do Sistema
MAX_FILE_SIZE=150
TICKET_TIMEOUT=30
PAYMENT_TIMEOUT=30
AUTO_DEPLOY=true
MERCADOPAGO_ENABLED=true
```

### 3. Configurar Recursos
- **Memory**: 512MB (mínimo)
- **CPU**: 25% (padrão)
- **Disk**: 1GB (suficiente)
- **Network**: Padrão

### 4. Iniciar Aplicação
1. Clique em "Start"
2. Aguarde a inicialização
3. Verifique os logs para confirmar funcionamento

## 🔧 Configuração Pós-Deploy

### 1. Sincronizar Comandos
O bot sincroniza automaticamente os comandos slash na inicialização.

### 2. Configurar Canais de Logs
1. Execute `/admin` → 📋 Logs
2. Configure os 4 canais:
   - 👤 **Actions** - Ações dos usuários
   - 🔧 **Admin** - Ações administrativas
   - 💳 **Payments** - Pagamentos processados
   - 🚀 **Deploys** - Deploys realizados

### 3. Configurar Preços
1. Execute `/admin` → 💰 Preços
2. Escolha o valor desejado na lista
3. Confirme a alteração

### 4. Configurar Sistema
1. Execute `/admin` → ⚙️ Configurações
2. Ajuste:
   - 📁 **Tamanho Máximo** - Limite de arquivos
   - ⏰ **Timeout Tickets** - Expiração de tickets
   - 💳 **Timeout Pagamentos** - Expiração de pagamentos

## 📊 Monitoramento

### 1. Logs da Aplicação
- Acesse "Logs" no painel da Square Cloud
- Monitore erros e avisos
- Verifique performance

### 2. Logs do Discord
- Monitore os 4 canais de logs
- Verifique ações dos usuários
- Acompanhe pagamentos e deploys

### 3. Métricas de Performance
- **Uptime**: Deve ser 99%+
- **Memory Usage**: Deve ficar abaixo de 80%
- **CPU Usage**: Deve ficar abaixo de 50%
- **Response Time**: Deve ser < 2 segundos

## 🔒 Segurança

### 1. Proteção de Tokens
- ✅ Nunca compartilhe tokens
- ✅ Use variáveis de ambiente
- ✅ Rotacione tokens periodicamente
- ✅ Monitore uso dos tokens

### 2. Permissões Discord
- ✅ Use permissões mínimas necessárias
- ✅ Monitore ações administrativas
- ✅ Configure roles adequadamente
- ✅ Revogue tokens comprometidos

### 3. Proteção de Dados
- ✅ Dados sensíveis em variáveis de ambiente
- ✅ Logs sem informações pessoais
- ✅ Limpeza automática de arquivos
- ✅ Backup seguro de configurações

## 🐛 Solução de Problemas

### Bot não inicia
1. **Verificar logs** - Acesse logs da Square Cloud
2. **Verificar tokens** - Confirme se estão corretos
3. **Verificar dependências** - Confirme requirements.txt
4. **Verificar permissões** - Confirme permissões Discord

### Comandos não funcionam
1. **Verificar sincronização** - Logs de inicialização
2. **Verificar permissões** - Bot precisa de permissões
3. **Verificar guild_id** - Deve ser o servidor correto
4. **Verificar client_id** - Deve ser o bot correto

### Pagamentos não funcionam
1. **Verificar Mercado Pago** - Token e conta ativos
2. **Verificar webhook** - URL configurada corretamente
3. **Verificar logs** - Erros específicos
4. **Testar manualmente** - API Mercado Pago

### Deploy não funciona
1. **Verificar Square Cloud** - API Key válida
2. **Verificar arquivo ZIP** - Estrutura correta
3. **Verificar limites** - Memória e disco
4. **Verificar logs** - Erros específicos

## 📈 Otimização

### 1. Performance
- **Memory**: Aumente se necessário
- **CPU**: Monitore uso
- **Network**: Verifique latência
- **Storage**: Limpe arquivos antigos

### 2. Escalabilidade
- **Rate Limiting**: Configure adequadamente
- **Caching**: Implemente se necessário
- **Load Balancing**: Para múltiplas instâncias
- **Monitoring**: Métricas em tempo real

### 3. Manutenção
- **Updates**: Mantenha dependências atualizadas
- **Backups**: Configure backups automáticos
- **Logs**: Monitore logs regularmente
- **Security**: Revise configurações periodicamente

## 🆘 Suporte

### Recursos Úteis
- 📚 **Documentação Square Cloud**: [docs.squarecloud.app](https://docs.squarecloud.app)
- 💬 **Discord Square Cloud**: [discord.gg/squarecloud](https://discord.gg/squarecloud)
- 📖 **Documentação Discord.py**: [discordpy.readthedocs.io](https://discordpy.readthedocs.io)
- 💳 **Mercado Pago Developers**: [developers.mercadopago.com](https://developers.mercadopago.com)

### Contato
- 🐛 **Issues**: [GitHub Issues](https://github.com/Huguitossss/HyperDeploy/issues)
- 📧 **Email**:*hugo.devbr@gmail.com*

---

**HyperDeploy - Deploy profissional e confiável para Square Cloud** 🚀
*(Ou não)*