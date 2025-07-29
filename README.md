# 🤖 HyperDeploy - Bot Discord para Square Cloud

**HyperDeploy** é um bot Discord para gerenciamento de aplicações na Square Cloud, com sistema de pagamento PIX integrado via Mercado Pago e interface moderna com slash commands.

## ✨ Funcionalidades Principais

### 🚀 **Sistema de Deploy Automático**
- **Upload de arquivos ZIP** até 150MB (configurável)
- **Sistema de tickets privados** - Cada usuário tem seu canal exclusivo
- **Deploy automático** após confirmação de pagamento PIX
- **Validação completa** de arquivos e estrutura
- **Configuração dinâmica** via painel administrativo

### 💳 **Sistema de Pagamento PIX**
- **Integração Mercado Pago** - Pagamentos PIX seguros e confiáveis
- **QR Code instantâneo** - Geração automática após upload
- **Verificação automática** - Polling a cada 5 segundos
- **Valores configuráveis** - Preços definidos via painel admin
- **Timeout personalizável** - Tempo limite para pagamento ajustável

### 🎫 **Sistema de Tickets Avançado**
- **Canais privados** - `ticket-XXX` para cada usuário
- **Mensagens de boas-vindas** - Instruções detalhadas e dicas
- **Timeout configurável** - Expiração personalizável (5-60 minutos)
- **Limpeza automática** - Tickets expirados removidos automaticamente
- **Organização total** - Sem poluição no chat público

### 👑 **Painel Administrativo Completo**
- **`/admin`** - Painel centralizado com todas as funções
- **Configuração de preços** - Lista com 15 opções (R$ 0,00 até R$ 50,00)
- **Tamanho máximo de arquivos** - Configurável via interface
- **Timeouts dinâmicos** - Tickets e pagamentos personalizáveis
- **Sistema de logs** - 4 canais organizados por categoria
- **Estatísticas em tempo real** - Status completo do sistema

### 📊 **Gerenciamento de Aplicações**
- **`/userpanel`** - Painel centralizado para usuários
- **Status em tempo real** - Verificação de aplicações ativas
- **Gerenciamento completo** - Start, stop, restart, delete
- **Backups automáticos** - Sistema de backup integrado
- **Domínios personalizados** - Configuração de domínios

### 🔧 **Sistema de Logs Organizados**
- **4 canais separados** para organização total:
  - 📋 **Actions** - Ações dos usuários
  - 🔧 **Admin** - Ações administrativas
  - 💳 **Payments** - Pagamentos processados
  - 🚀 **Deploys** - Deploys realizados
- **Configuração flexível** - Via painel admin ou arquivo
- **Logs detalhados** - Informações completas de cada ação

## 🛠️ Tecnologias Utilizadas

- **[Python 3.11+](https://www.python.org/)** - Linguagem principal
- **[discord.py 2.6.1](https://discordpy.readthedocs.io/)** - API Discord
- **[squarecloud-api](https://github.com/squarecloudofc/sdk-api-py)** - API oficial Square Cloud
- **[Mercado Pago](https://www.mercadopago.com.br/)** - Pagamentos PIX
- **[aiohttp](https://docs.aiohttp.org/)** - Requisições assíncronas
- **[Pillow](https://pypi.org/project/pillow/)** - Geração de QR Codes

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- Conta Discord Developer
- API Key da Square Cloud
- Conta Mercado Pago (para pagamentos PIX)

### 1. Clonar o Repositório
```bash
git clone https://github.com/huguitossss/HyperDeploy.git
cd HyperDeploy
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar Bot Discord
1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications)
2. Crie uma nova aplicação
3. Vá em "Bot" e copie o token
4. Configure as permissões necessárias:
   - `Use Slash Commands`
   - `Send Messages`
   - `Manage Channels`
   - `Attach Files`
   - `Read Message History`
5. Copie os arquivos de exemplo:
```bash
cp config/bot.example.yaml config/bot.yaml
cp config/squarecloud.example.yaml config/squarecloud.yaml
```
6. Edite `config/bot.yaml` com suas credenciais:
```yaml
bot_token: "SEU_TOKEN_DISCORD_AQUI"
guild_id: SEU_GUILD_ID_AQUI
mercadopago_access_token: "SEU_ACCESS_TOKEN_MERCADOPAGO_AQUI"
```

### 4. Configurar Square Cloud
1. Acesse [Square Cloud](https://squarecloud.app)
2. Faça login na sua conta
3. Vá em "Minha Conta" > "API"
4. Clique em "Gerar Nova Chave"
5. Edite `config/squarecloud.yaml`:
```yaml
api_key: "SUA_API_KEY_SQUARECLOUD_AQUI"
```

### 5. Configurar Mercado Pago (Opcional)
1. Acesse [Mercado Pago Developers](https://developers.mercadopago.com)
2. Crie uma conta de desenvolvedor
3. Gere um Access Token
4. Adicione no `config/bot.yaml`:
```yaml
mercadopago_access_token: "SEU_ACCESS_TOKEN_MERCADOPAGO_AQUI"
```

### 5. Configurar Mercado Pago
1. Acesse [Mercado Pago Developers](https://www.mercadopago.com.br/developers)
2. Crie uma aplicação
3. Gere um Access Token
4. Adicione no `config/bot.yaml`

### 6. Executar o Bot
```bash
python bot.py
```

## 📚 Comandos Disponíveis

### 👤 **Comandos de Usuário**

#### `/userpanel`
Painel centralizado para usuários com todas as funcionalidades:
- 🚀 **Deploy** - Criar ticket para deploy
- 🗑️ **Delete** - Remover aplicações
- 🔑 **Chaves** - Gerenciar chaves da Square Cloud
- 💳 **Pagamentos** - Histórico de pagamentos
- 📊 **Status** - Status das aplicações
- 💾 **Backups** - Gerenciar backups
- 🌐 **Domínios** - Configurar domínios
- ℹ️ **Info** - Informações do bot

### 👑 **Comandos de Administrador**

#### `/admin`
Painel administrativo completo com todas as configurações:
- 💰 **Preços** - Configurar valores dos deploys
- ⚙️ **Configurações** - Tamanho máximo, timeouts, etc.
- 📊 **Status** - Status completo do sistema
- 🧹 **Limpeza** - Limpar dados e arquivos
- 🔒 **Tickets** - Gerenciar tickets ativos
- 📋 **Logs** - Configurar canais de logs

## 🎫 Sistema de Tickets

### Como Funciona
1. **Usuário executa `/userpanel`** → Clica em "🚀 Deploy"
2. **Canal privado criado** → `ticket-XXX` exclusivo
3. **Mensagem de boas-vindas** → Instruções detalhadas
4. **Upload do arquivo ZIP** → Validação automática
5. **QR Code PIX gerado** → Pagamento instantâneo
6. **Verificação automática** → Polling a cada 5 segundos
7. **Deploy automático** → Após confirmação do pagamento
8. **Ticket expira** → Limpeza automática configurável

### Vantagens
- ✅ **Organização total** - Sem poluição no chat público
- ✅ **Privacidade** - Cada usuário tem seu espaço
- ✅ **Instruções claras** - Mensagens detalhadas e dicas
- ✅ **Timeout configurável** - 5 a 60 minutos via painel admin
- ✅ **Limpeza automática** - Tickets expirados removidos

## 💳 Sistema de Pagamento PIX

### Processo Completo
1. **Upload do arquivo** → Validação e salvamento
2. **Geração do pagamento** → Dados preparados automaticamente
3. **QR Code PIX** → Gerado instantaneamente
4. **Verificação automática** → Polling a cada 5 segundos
5. **Confirmação** → Deploy inicia automaticamente
6. **Limpeza** → QR Codes removidos após uso

### Configurações
- **Valores dinâmicos** - Configuráveis via painel admin
- **Timeout personalizável** - 5 a 60 minutos
- **Verificação robusta** - Múltiplas tentativas
- **Logs detalhados** - Registro completo de transações

## 🔧 Configurações Administrativas

### Painel de Preços (`/admin` → 💰 Preços)
- **Lista de preços** - 15 opções (R$ 0,00 até R$ 50,00)
- **Alteração instantânea** - Valores atualizados em tempo real
- **Reset automático** - Volta para R$ 10,00 padrão
- **Logs de alterações** - Registro de todas as mudanças

### Configurações do Sistema (`/admin` → ⚙️ Configurações)
- **📁 Tamanho Máximo** - Limite de arquivo (1-500 MB)
- **⏰ Timeout Tickets** - Expiração de tickets (5-60 min)
- **💳 Timeout Pagamentos** - Expiração de pagamentos (5-60 min)
- **🚀 Deploy Automático** - Habilitar/desabilitar
- **💳 Mercado Pago** - Habilitar/desabilitar PIX

### Sistema de Logs (`/admin` → 📋 Logs)
- **4 canais organizados**:
  - 👤 **Actions** - Ações dos usuários
  - 🔧 **Admin** - Ações administrativas
  - 💳 **Payments** - Pagamentos processados
  - 🚀 **Deploys** - Deploys realizados
- **Configuração flexível** - Via painel ou arquivo
- **Testes automáticos** - Verificação de canais

## 🏗️ Arquitetura do Projeto

```
HyperDeploy/
├── bot.py                          # Bot principal
├── config/                         # Configurações
│   ├── bot.yaml                   # Configurações do bot
│   └── squarecloud.yaml           # Configurações Square Cloud
├── core/                          # Módulos principais
│   ├── commands/                  # Comandos slash
│   │   ├── admin_panel.py        # Painel administrativo
│   │   └── userpanel.py          # Painel de usuário
│   ├── payments/                  # Sistema de pagamentos
│   │   ├── manager.py            # Gerenciador de pagamentos
│   │   ├── config_manager.py     # Configurações
│   │   └── mercadopago.py        # Integração Mercado Pago
│   ├── tickets/                   # Sistema de tickets
│   │   ├── manager.py            # Gerenciador de tickets
│   │   └── uploads.py            # Processamento de uploads
│   ├── squarecloud/               # Integração Square Cloud
│   │   ├── client.py             # Cliente da API
│   │   ├── backup_manager.py     # Gerenciador de backups
│   │   └── domain_manager.py     # Gerenciador de domínios
│   └── logs/                      # Sistema de logs
│       └── organized_logger.py   # Logger organizado
├── data/                          # Dados persistentes
│   ├── admin_config.json         # Configurações admin
│   ├── payments.json             # Histórico de pagamentos
│   ├── tickets.json              # Tickets ativos
│   └── user_keys.json            # Chaves dos usuários
├── uploads/                       # Arquivos temporários
├── qrcodes/                       # QR Codes gerados
├── docs/                          # Documentação
├── requirements.txt               # Dependências
├── squarecloud.config             # Configuração Square Cloud
└── README.md                      # Este arquivo
```

## 🔐 Segurança

### Medidas Implementadas
- ✅ **Validação de arquivos** - Extensões e tamanhos verificados
- ✅ **Rate limiting** - Proteção contra spam
- ✅ **Logs detalhados** - Auditoria completa
- ✅ **Tratamento de erros** - Fallback robusto
- ✅ **Variáveis de ambiente** - Credenciais seguras
- ✅ **Verificação de pagamentos** - Sistema confiável
- ✅ **Permissões administrativas** - Controle de acesso
- ✅ **Canais privados** - Logs organizados e seguros
- ✅ **Sistema de tickets** - Privacidade total
- ✅ **Sanitização de dados** - Proteção contra injeções
- ✅ **Timeout configurável** - Controle de sessões
- ✅ **Limpeza automática** - Dados sensíveis removidos

## 🚀 Deploy na Square Cloud

### 1. Preparar o Projeto
1. Faça upload do projeto para um repositório GitHub
2. Configure o arquivo `squarecloud.config`:
```ini
DISPLAY_NAME=HyperDeploy
DESCRIPTION=Bot Discord para Square Cloud
MAIN=bot.py
MEMORY=512
VERSION=recommended
RESTART=true
```

### 2. Deploy na Square Cloud
1. Acesse o [painel da Square Cloud](https://squarecloud.app)
2. Clique em "New Application"
3. Escolha "From GitHub"
4. Selecione seu repositório
5. Configure as variáveis de ambiente

### 3. Variáveis de Ambiente
Configure no painel da Square Cloud:
```env
# Discord Bot
BOT_TOKEN=seu_token_discord
GUILD_ID=seu_guild_id

# Square Cloud
SQUARECLOUD_API_KEY=sua_api_key

# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=seu_access_token
```

## 📊 Sistema de Logs Organizados

### Canais Recomendados
```
📁 LOGS HYPERDEPLOY
├── 👤 hyperdeploy-actions     # Ações dos usuários
├── 🔧 hyperdeploy-admin       # Ações administrativas  
├── 💳 hyperdeploy-payments    # Pagamentos processados
└── 🚀 hyperdeploy-deploys     # Deploys realizados
```

### Configuração via Painel Admin
1. Execute `/admin` → 📋 Logs
2. Configure cada canal separadamente
3. Teste a configuração automaticamente

### Tipos de Logs

#### Actions Logs (👤 hyperdeploy-actions)
- Comandos executados pelos usuários
- Tentativas de acesso
- Ações em tickets
- Erros do sistema

#### Admin Logs (🔧 hyperdeploy-admin)
- Mudanças de configuração
- Alterações de valores
- Status do sistema
- Ações administrativas

#### Payments Logs (💳 hyperdeploy-payments)
- Pagamentos aprovados
- Pagamentos rejeitados
- Pagamentos pendentes
- Valores e configurações

#### Deploy Logs (🚀 hyperdeploy-deploys)
- Aplicações implantadas
- Sucessos e falhas
- Informações técnicas
- Valores pagos

## 🔄 Fluxo Completo de Deploy

### Processo Detalhado
1. **Usuário executa `/userpanel`** → Clica em "🚀 Deploy"
2. **Ticket criado** → Canal privado `ticket-XXX`
3. **Mensagem de boas-vindas** → Instruções e configurações atuais
4. **Upload do arquivo ZIP** → Validação automática
5. **Confirmação imediata** → Feedback instantâneo
6. **Processamento paralelo** → Salvamento + preparação pagamento
7. **QR Code PIX gerado** → Pagamento instantâneo
8. **Verificação automática** → Polling a cada 5 segundos
9. **Confirmação de pagamento** → Deploy inicia automaticamente
10. **Ticket expira** → Limpeza automática configurável

### Validações Implementadas
- **Arquivo ZIP** - Formato e estrutura verificados
- **Tamanho máximo** - Configurável via painel admin
- **Estrutura interna** - `squarecloud.app` ou `squarecloud.config`
- **Dados de pagamento** - Validação completa
- **Timeout configurável** - Tickets e pagamentos personalizáveis

## 🎯 Recursos Avançados

### Sistema de Cache Inteligente
- **Configurações em cache** - Acesso rápido a dados
- **Persistência automática** - Dados salvos automaticamente
- **Sincronização em tempo real** - Alterações refletidas instantaneamente

### Tratamento Robusto de Erros
- **Fallback inteligente** - Sistema funciona mesmo com APIs indisponíveis
- **Retry automático** - Múltiplas tentativas com configurações otimizadas
- **Logs detalhados** - Captura completa de erros para debugging
- **Recovery automático** - Sistema continua funcionando mesmo com falhas

### Performance Otimizada
- **Processamento paralelo** - Upload e pagamento simultâneos
- **Feedback imediato** - Confirmações instantâneas
- **Timeout otimizado** - Configurações balanceadas
- **Limpeza automática** - Recursos liberados automaticamente

## 🐛 Solução de Problemas

### Bot não responde
- Verifique se o token está correto em `config/bot.yaml`
- Confirme se o bot tem permissões no servidor
- Verifique se as dependências estão instaladas

### Erro no Mercado Pago
- Confirme o Access Token em `config/bot.yaml`
- Verifique se a conta Mercado Pago está ativa
- Teste a integração manualmente

### Erro no deploy
- Verifique se a API Key da Square Cloud está correta
- Confirme se o ZIP contém `squarecloud.app` ou `squarecloud.config`
- Verifique se a aplicação não excede limites da Square Cloud

### Problemas de configuração
- Use `/admin` → ⚙️ Configurações para verificar valores
- Confirme se os canais de logs existem
- Verifique permissões administrativas

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

- 📚 Documentação Square Cloud: [docs.squarecloud.app](https://docs.squarecloud.app)
- 🐛 Issues: [GitHub Issues](https://github.com/huguitossss/HyperDeploy/issues)

## 🔄 Changelog

### v1.0.7 - Sistema Completo e Estável
- ✅ **Sistema de tickets avançado** - Canais privados com mensagens detalhadas
- ✅ **Painel administrativo completo** - Configurações dinâmicas via interface
- ✅ **Sistema de pagamento robusto** - PIX via Mercado Pago integrado
- ✅ **Logs organizados** - 4 canais separados por categoria
- ✅ **Configurações dinâmicas** - Timeouts e tamanhos personalizáveis
- ✅ **Tratamento de erros** - Sistema robusto com fallback
- ✅ **Performance otimizada** - Processamento paralelo e feedback imediato

### v1.0.6 - Correções e Melhorias
- ✅ **Correção de timeouts** - Mensagens refletem configurações atuais
- ✅ **Interface limpa** - Remoção de duplicações no painel admin
- ✅ **Logs administrativos** - Sistema completo de logging
- ✅ **Validação robusta** - Verificações completas de dados

### v1.0.5 - Sistema de Upload Otimizado
- ✅ **Latência reduzida** - Processamento paralelo implementado
- ✅ **Feedback imediato** - Confirmações instantâneas
- ✅ **Contador removido** - Sistema simplificado e estável
- ✅ **Validação melhorada** - Verificações completas de arquivos

### v1.0.0 - Lançamento Inicial
- ✅ **Sistema de deploy completo** - Upload e deploy automático
- ✅ **Integração PIX** - Pagamentos via Mercado Pago
- ✅ **Interface moderna** - Slash commands e painéis
- ✅ **Configurações flexíveis** - Sistema adaptável

---

**Desenvolvido por Hugoo!**

*HyperDeploy!* 