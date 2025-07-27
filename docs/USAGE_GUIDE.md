# 📖 Guia de Uso - HyperDeploy

Guia completo para usuários finais sobre como usar o HyperDeploy para fazer deploy de aplicações na Square Cloud.

## 🎯 Índice

- [Primeiros Passos](#primeiros-passos)
- [Comandos de Usuário](#comandos-de-usuário)
- [Sistema de Tickets](#sistema-de-tickets)
- [Sistema de Pagamento](#sistema-de-pagamento)
- [Gerenciamento de Aplicações](#gerenciamento-de-aplicações)
- [Dicas e Truques](#dicas-e-truques)
- [Solução de Problemas](#solução-de-problemas)

## 🚀 Primeiros Passos

### 1. Acessar o Bot
1. **Entre no servidor Discord** onde o HyperDeploy está configurado
2. **Verifique se o bot está online** (status verde)
3. **Execute `/userpanel`** para acessar o painel principal

### 2. Configurar Chave da Square Cloud
1. **Execute `/userpanel`** → Clique em **🔑 Chaves**
2. **Cole sua API Key** da Square Cloud
3. **Confirme a configuração**
4. ✅ **Sua chave está salva e segura**

### 3. Primeiro Deploy
1. **Execute `/userpanel`** → Clique em **🚀 Deploy**
2. **Aguarde o ticket ser criado**
3. **Envie seu arquivo ZIP**
4. **Faça o pagamento PIX**
5. **Aguarde o deploy automático**

## 📋 Comandos de Usuário

### `/userpanel` - Painel Principal
O painel central com todas as funcionalidades:

#### 🚀 **Deploy**
- **Criar ticket** para novo deploy
- **Upload de arquivo ZIP**
- **Pagamento PIX automático**
- **Deploy na Square Cloud**

#### 🗑️ **Delete**
- **Listar aplicações** ativas
- **Selecionar aplicação** para deletar
- **Confirmação** obrigatória
- **Remoção permanente**

#### 🔑 **Chaves**
- **Configurar API Key** da Square Cloud
- **Validar chave** automaticamente
- **Salvar chave** de forma segura
- **Gerenciar múltiplas chaves**

#### 💳 **Pagamentos**
- **Histórico completo** de pagamentos
- **Status** de cada transação
- **Valores pagos** e datas
- **Detalhes** das aplicações

#### 📊 **Status**
- **Status em tempo real** das aplicações
- **Uso de recursos** (CPU, RAM)
- **Uptime** e URLs
- **Logs** das aplicações

#### 💾 **Backups**
- **Criar backup** da aplicação
- **Listar backups** disponíveis
- **Baixar backup** localmente
- **Restaurar** de backup

#### 🌐 **Domínios**
- **Configurar domínio** personalizado
- **Listar domínios** ativos
- **Gerenciar SSL** automático
- **Remover domínio**

#### ℹ️ **Info**
- **Informações do bot** e versão
- **Status do sistema**
- **Links úteis**
- **Suporte**

## 🎫 Sistema de Tickets

### Como Funciona
1. **Execute `/userpanel`** → Clique em **🚀 Deploy**
2. **Canal privado criado** automaticamente
3. **Mensagem de boas-vindas** com instruções
4. **Upload do arquivo ZIP**
5. **QR Code PIX gerado**
6. **Pagamento e deploy automático**

### Estrutura do Ticket
```
🎫 Ticket #XXX
💰 Preço: R$ XX,XX
⏰ Expira em: XX minutos
📋 Instruções detalhadas
🔧 Requisitos do ZIP
💡 Dicas para deploy
```

### Requisitos do Arquivo ZIP
- ✅ **squarecloud.app** ou **squarecloud.config** na raiz
- ✅ **Arquivo principal** (main.py, index.js, etc.)
- ✅ **Dependências** (requirements.txt, package.json)
- ✅ **Estrutura organizada** de pastas
- ❌ **Sem arquivos desnecessários**

### Exemplo de Estrutura
```
meu-projeto/
├── main.py                    # Arquivo principal
├── requirements.txt           # Dependências Python
├── squarecloud.app           # Configuração Square Cloud
├── src/                      # Código fonte
│   ├── __init__.py
│   └── app.py
├── static/                   # Arquivos estáticos
│   ├── css/
│   └── js/
└── README.md                 # Documentação
```

### Configuração squarecloud.app
```ini
DISPLAY_NAME=Minha Aplicação
MAIN=main.py
VERSION=recommended
MEMORY=512
AUTORESTART=true
```

## 💳 Sistema de Pagamento

### Processo de Pagamento
1. **Upload do arquivo** → Validação automática
2. **QR Code PIX** → Gerado instantaneamente
3. **Pagamento** → Via PIX (QR Code ou código)
4. **Verificação** → Automática a cada 5 segundos
5. **Deploy** → Inicia automaticamente após confirmação

### Métodos de Pagamento
- **QR Code PIX** - Escaneie com app do banco
- **Código PIX** - Copie e cole no app
- **Valores configuráveis** - Definidos pelo administrador

### Status de Pagamento
- **⏳ Pendente** - Aguardando pagamento
- **✅ Aprovado** - Pagamento confirmado
- **❌ Rejeitado** - Pagamento negado
- **⏰ Expirado** - Tempo limite excedido

### Timeout de Pagamento
- **Configurável** pelo administrador
- **Padrão**: 30 minutos
- **Limpeza automática** após expiração
- **Novo QR Code** se necessário

## 🛠️ Gerenciamento de Aplicações

### Status das Aplicações
- **🟢 Online** - Aplicação rodando
- **🔴 Offline** - Aplicação parada
- **🟡 Iniciando** - Aplicação iniciando
- **🔵 Parando** - Aplicação parando

### Controles Disponíveis
- **▶️ Start** - Iniciar aplicação
- **⏹️ Stop** - Parar aplicação
- **🔄 Restart** - Reiniciar aplicação
- **📋 Logs** - Ver logs em tempo real
- **🗑️ Delete** - Remover aplicação

### Informações Exibidas
- **Nome da aplicação**
- **Status atual**
- **Uso de CPU** (%)
- **Uso de RAM** (MB)
- **Uptime** (tempo ativo)
- **URL da aplicação**
- **Data de criação**

### Logs das Aplicações
- **Logs em tempo real**
- **Últimas 100 linhas**
- **Filtros por tipo**
- **Download de logs**
- **Limpeza automática**

## 💾 Sistema de Backups

### Criar Backup
1. **Execute `/userpanel`** → **💾 Backups**
2. **Selecione aplicação**
3. **Clique em "Criar Backup"**
4. **Aguarde a criação**
5. **Download automático**

### Gerenciar Backups
- **Listar backups** disponíveis
- **Informações** de cada backup
- **Tamanho** e data de criação
- **Download** local
- **Restauração** automática

### Configurações de Backup
- **Backup automático** a cada 24h
- **Retenção** de 7 dias
- **Compressão** automática
- **Validação** de integridade

## 🌐 Sistema de Domínios

### Configurar Domínio
1. **Execute `/userpanel`** → **🌐 Domínios**
2. **Digite o domínio** (ex: meu-site.com)
3. **Confirme a configuração**
4. **SSL automático** configurado
5. **DNS configurado** automaticamente

### Gerenciar Domínios
- **Listar domínios** ativos
- **Status SSL** de cada domínio
- **Renovação automática** de certificados
- **Remoção** de domínios

### Tipos de Domínio
- **Subdomínio** - app.squarecloud.app
- **Domínio personalizado** - meu-site.com
- **Wildcard** - *.meu-site.com

## 📊 Monitoramento

### Métricas Disponíveis
- **CPU Usage** - Uso de processador
- **Memory Usage** - Uso de memória
- **Disk Usage** - Uso de disco
- **Network** - Tráfego de rede
- **Uptime** - Tempo ativo

### Alertas Automáticos
- **Aplicação offline** - Notificação automática
- **Uso alto de recursos** - Alertas de performance
- **Erros críticos** - Notificações imediatas
- **Backup falhou** - Alerta de backup

## 💡 Dicas e Truques

### Otimização de Performance
- **Use .gitignore** para excluir arquivos desnecessários
- **Comprima imagens** antes do upload
- **Remova logs** antigos do ZIP
- **Use requirements.txt** para Python
- **Configure .env** para variáveis

### Estrutura Recomendada
```
projeto/
├── main.py              # Arquivo principal
├── requirements.txt     # Dependências
├── squarecloud.app     # Configuração
├── .env.example        # Exemplo de variáveis
├── .gitignore          # Arquivos ignorados
├── README.md           # Documentação
└── src/                # Código fonte
```

### Configuração Otimizada
```ini
# squarecloud.app otimizado
DISPLAY_NAME=Minha App
MAIN=main.py
VERSION=recommended
MEMORY=512
CPU=25
AUTORESTART=true
BACKUP=true
BACKUP_INTERVAL=24
```

### Variáveis de Ambiente
```env
# .env para configurações
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=your_api_key_here
DEBUG=false
PORT=3000
```

## 🐛 Solução de Problemas

### Problemas Comuns

#### ❌ "Arquivo ZIP inválido"
- **Verifique a extensão** (.zip)
- **Confirme o tamanho** (dentro do limite)
- **Verifique a estrutura** interna
- **Teste o ZIP** localmente

#### ❌ "squarecloud.app não encontrado"
- **Coloque na raiz** do ZIP
- **Verifique o nome** exato
- **Confirme a extensão** (.app)
- **Teste a sintaxe** do arquivo

#### ❌ "Pagamento não confirmado"
- **Aguarde 5 segundos** para verificação
- **Verifique o valor** exato
- **Confirme o pagamento** no app do banco
- **Tente novamente** se necessário

#### ❌ "Aplicação não inicia"
- **Verifique os logs** da aplicação
- **Confirme o arquivo principal** em squarecloud.app
- **Teste localmente** antes do deploy
- **Verifique dependências** em requirements.txt

#### ❌ "Erro de permissão"
- **Verifique se tem permissão** no servidor
- **Confirme se o bot está online**
- **Tente novamente** em alguns minutos
- **Contate um administrador**

### Logs de Erro
- **Verifique logs** da aplicação
- **Procure por erros** específicos
- **Compare com** logs de sucesso
- **Pesquise soluções** online

### Contato para Suporte
- **Discord**: Servidor do HyperDeploy
- **GitHub**: Issues do projeto
- **Documentação**: docs/ do projeto
- **Administrador**: Do servidor

## 📚 Recursos Adicionais

### Documentação
- **README.md** - Documentação principal
- **docs/DEPLOY_GUIDE.md** - Guia de deploy
- **docs/API_REFERENCE.md** - Referência da API
- **docs/CHANGELOG.md** - Histórico de versões

### Links Úteis
- **Square Cloud**: [squarecloud.app](https://squarecloud.app)
- **Discord.py**: [discordpy.readthedocs.io](https://discordpy.readthedocs.io)
- **Mercado Pago**: [mercadopago.com.br](https://mercadopago.com.br)

### Comunidade
- **Discord**: Servidor oficial
- **GitHub**: Repositório do projeto
- **Issues**: Reportar problemas
- **Discussions**: Discussões gerais

---

**HyperDeploy - Deploy simples e profissional para Square Cloud** 🚀

*Siga este guia para aproveitar ao máximo o HyperDeploy!* 