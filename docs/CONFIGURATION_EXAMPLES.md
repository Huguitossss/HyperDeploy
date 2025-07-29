# ⚙️ Exemplos de Configuração - HyperDeploy

Guia completo com exemplos de configuração para diferentes cenários e tipos de aplicação.

## 📋 Índice

- [Configurações Básicas](#configurações-básicas)
- [Exemplos por Linguagem](#exemplos-por-linguagem)
- [Configurações Avançadas](#configurações-avançadas)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Configurações de Performance](#configurações-de-performance)
- [Exemplos de Deploy](#exemplos-de-deploy)

## 🔧 Configurações Básicas

### squarecloud.app (Configuração Padrão)
```ini
DISPLAY_NAME=Minha Aplicação
MAIN=main.py
VERSION=recommended
MEMORY=512
AUTORESTART=true
```

### squarecloud.config (Configuração JSON)
```json
{
  "main": "main.py",
  "version": "3.11",
  "ram": 512,
  "disk": 1024,
  "cpu": 25,
  "auto_restart": true,
  "backup": true,
  "backup_interval": 24,
  "description": "Minha aplicação na Square Cloud"
}
```

### requirements.txt (Dependências Python)
```txt
discord.py==2.6.1
aiohttp==3.8.0
pillow==10.0.0
pyyaml==6.0.1
```

## 🐍 Exemplos por Linguagem

### Python - Bot Discord
```ini
# squarecloud.app
DISPLAY_NAME=Meu Bot Discord
MAIN=bot.py
VERSION=recommended
MEMORY=512
AUTORESTART=true
```

```python
# bot.py
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} está online!')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

bot.run('SEU_TOKEN_AQUI')
```

```txt
# requirements.txt
discord.py==2.6.1
```

### Python - API Flask
```ini
# squarecloud.app
DISPLAY_NAME=API Flask
MAIN=app.py
VERSION=recommended
MEMORY=512
AUTORESTART=true
```

```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"message": "Hello World!"})

@app.route('/api/users')
def get_users():
    return jsonify({"users": ["user1", "user2"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
```

```txt
# requirements.txt
flask==2.3.0
```

### Python - Bot Telegram
```ini
# squarecloud.app
DISPLAY_NAME=Bot Telegram
MAIN=bot.py
VERSION=recommended
MEMORY=512
AUTORESTART=true
```

```python
# bot.py
import telebot

bot = telebot.TeleBot("SEU_TOKEN_AQUI")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Como posso ajudar?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
```

```txt
# requirements.txt
pyTelegramBotAPI==4.12.0
```

### Node.js - Bot Discord
```json
// squarecloud.config
{
  "main": "index.js",
  "version": "18",
  "ram": 512,
  "disk": 1024,
  "cpu": 25,
  "auto_restart": true,
  "backup": true,
  "backup_interval": 24,
  "description": "Bot Discord em Node.js"
}
```

```javascript
// index.js
const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

client.once('ready', () => {
  console.log('Bot está online!');
});

client.on('messageCreate', message => {
  if (message.content === '!ping') {
    message.reply('Pong!');
  }
});

client.login('SEU_TOKEN_AQUI');
```

```json
// package.json
{
  "name": "meu-bot-discord",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "discord.js": "^14.11.0"
  },
  "scripts": {
    "start": "node index.js"
  }
}
```

### Node.js - API Express
```json
// squarecloud.config
{
  "main": "app.js",
  "version": "18",
  "ram": 512,
  "disk": 1024,
  "cpu": 25,
  "auto_restart": true,
  "backup": true,
  "backup_interval": 24,
  "description": "API Express"
}
```

```javascript
// app.js
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'API funcionando!' });
});

app.get('/api/users', (req, res) => {
  res.json({ users: ['user1', 'user2'] });
});

app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});
```

```json
// package.json
{
  "name": "api-express",
  "version": "1.0.0",
  "main": "app.js",
  "dependencies": {
    "express": "^4.18.2"
  },
  "scripts": {
    "start": "node app.js"
  }
}
```

## 🚀 Configurações Avançadas

### Aplicação com Domínio Personalizado
```ini
# squarecloud.app
DISPLAY_NAME=Meu Site
MAIN=app.py
VERSION=recommended
MEMORY=512
AUTORESTART=true
SUBDOMAIN=meu-site
```

### Aplicação com Variáveis de Ambiente
```ini
# squarecloud.app
DISPLAY_NAME=API com Env
MAIN=app.py
VERSION=recommended
MEMORY=512
AUTORESTART=true
```

```python
# app.py
import os
from flask import Flask

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
API_KEY = os.getenv('API_KEY', 'default_key')
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

@app.route('/')
def home():
    return f"API Key: {API_KEY}, Debug: {DEBUG}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 3000)))
```

### Aplicação com Backup Automático
```ini
# squarecloud.app
DISPLAY_NAME=App com Backup
MAIN=app.py
VERSION=recommended
MEMORY=512
AUTORESTART=true
BACKUP=true
BACKUP_INTERVAL=12
```

### Aplicação com SSL
```ini
# squarecloud.app
DISPLAY_NAME=App Segura
MAIN=app.py
VERSION=recommended
MEMORY=512
AUTORESTART=true
SUBDOMAIN=app-segura
SSL=true
```

## 🔐 Variáveis de Ambiente

### .env (Arquivo de Variáveis)
```env
# Configurações do Banco
DATABASE_URL=postgresql://user:pass@localhost/db
DATABASE_PASSWORD=senha_segura_123

# Configurações da API
API_KEY=chave_api_super_secreta
API_SECRET=segredo_muito_seguro

# Configurações do Bot
BOT_TOKEN=SEU_TOKEN_DISCORD_AQUI
CLIENT_ID=1234567890123456789

# Configurações do Sistema
DEBUG=false
PORT=3000
NODE_ENV=production

# Configurações de Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=seu_email_aqui@exemplo.com
EMAIL_PASS=sua_senha_aqui

# Configurações de Pagamento
MERCADOPAGO_ACCESS_TOKEN=SEU_ACCESS_TOKEN_MERCADOPAGO_AQUI
MERCADOPAGO_PUBLIC_KEY=SEU_PUBLIC_KEY_MERCADOPAGO_AQUI
```

### .env.example (Exemplo de Variáveis)
```env
# Copie este arquivo para .env e preencha com seus valores
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=your_api_key_here
BOT_TOKEN=your_bot_token_here
DEBUG=false
PORT=3000
```

## ⚡ Configurações de Performance

### Aplicação Leve (256MB RAM)
```ini
# squarecloud.app
DISPLAY_NAME=App Leve
MAIN=app.py
VERSION=recommended
MEMORY=256
AUTORESTART=true
```

### Aplicação Média (512MB RAM)
```ini
# squarecloud.app
DISPLAY_NAME=App Média
MAIN=app.py
VERSION=recommended
MEMORY=512
AUTORESTART=true
```

### Aplicação Pesada (1024MB RAM)
```ini
# squarecloud.app
DISPLAY_NAME=App Pesada
MAIN=app.py
VERSION=recommended
MEMORY=1024
AUTORESTART=true
```

### Aplicação com CPU Limitado
```ini
# squarecloud.app
DISPLAY_NAME=App CPU Limitado
MAIN=app.py
VERSION=recommended
MEMORY=512
CPU=10
AUTORESTART=true
```

## 📦 Exemplos de Deploy

### Estrutura Completa - Bot Discord
```
meu-bot-discord/
├── bot.py                    # Arquivo principal
├── requirements.txt          # Dependências Python
├── squarecloud.app          # Configuração Square Cloud
├── .env                     # Variáveis de ambiente
├── .gitignore               # Arquivos ignorados
├── README.md                # Documentação
├── cogs/                    # Comandos do bot
│   ├── __init__.py
│   ├── admin.py
│   └── user.py
├── utils/                   # Utilitários
│   ├── __init__.py
│   └── helpers.py
└── data/                    # Dados do bot
    └── config.json
```

### Estrutura Completa - API Flask
```
minha-api/
├── app.py                   # Arquivo principal
├── requirements.txt         # Dependências Python
├── squarecloud.app         # Configuração Square Cloud
├── .env                     # Variáveis de ambiente
├── .gitignore               # Arquivos ignorados
├── README.md                # Documentação
├── routes/                  # Rotas da API
│   ├── __init__.py
│   ├── auth.py
│   └── users.py
├── models/                  # Modelos de dados
│   ├── __init__.py
│   └── user.py
├── utils/                   # Utilitários
│   ├── __init__.py
│   └── database.py
└── static/                  # Arquivos estáticos
    ├── css/
    └── js/
```

### Estrutura Completa - Site Estático
```
meu-site/
├── index.html               # Página principal
├── squarecloud.app         # Configuração Square Cloud
├── .gitignore               # Arquivos ignorados
├── README.md                # Documentação
├── css/                     # Estilos
│   ├── style.css
│   └── responsive.css
├── js/                      # JavaScript
│   ├── main.js
│   └── utils.js
├── images/                  # Imagens
│   ├── logo.png
│   └── banner.jpg
└── pages/                   # Páginas adicionais
    ├── about.html
    └── contact.html
```

## 🔧 Configurações Específicas

### Bot com Sistema de Logs
```python
# bot.py
import discord
import logging
from discord.ext import commands

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logger.info(f'{bot.user} está online!')

@bot.event
async def on_command_error(ctx, error):
    logger.error(f'Erro no comando {ctx.command}: {error}')

bot.run('SEU_TOKEN_AQUI')
```

### API com Middleware de Autenticação
```python
# app.py
from flask import Flask, request, jsonify
from functools import wraps
import os

app = Flask(__name__)

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.getenv('API_KEY'):
            return jsonify({"error": "API key inválida"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return jsonify({"message": "API funcionando!"})

@app.route('/api/protected')
@require_api_key
def protected():
    return jsonify({"message": "Rota protegida!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 3000)))
```

### Bot com Sistema de Economia
```python
# bot.py
import discord
import json
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Sistema de economia
def load_economy():
    if os.path.exists('economy.json'):
        with open('economy.json', 'r') as f:
            return json.load(f)
    return {}

def save_economy(economy_data):
    with open('economy.json', 'w') as f:
        json.dump(economy_data, f, indent=2)

@bot.command()
async def balance(ctx):
    economy = load_economy()
    user_id = str(ctx.author.id)
    balance = economy.get(user_id, 0)
    await ctx.send(f'Seu saldo: {balance} moedas')

@bot.command()
async def daily(ctx):
    economy = load_economy()
    user_id = str(ctx.author.id)
    economy[user_id] = economy.get(user_id, 0) + 100
    save_economy(economy)
    await ctx.send('Você recebeu 100 moedas!')

bot.run('SEU_TOKEN_AQUI')
```

## 📋 Checklist de Deploy

### Antes do Deploy
- [ ] **Arquivo principal** configurado corretamente
- [ ] **Dependências** listadas em requirements.txt/package.json
- [ ] **squarecloud.app** ou **squarecloud.config** na raiz
- [ ] **Variáveis de ambiente** configuradas
- [ ] **Arquivos desnecessários** removidos
- [ ] **Teste local** realizado
- [ ] **Logs** configurados
- [ ] **Tratamento de erros** implementado

### Durante o Deploy
- [ ] **Upload do ZIP** realizado
- [ ] **Validação** automática passou
- [ ] **Pagamento PIX** confirmado
- [ ] **Deploy** iniciado automaticamente
- [ ] **Logs** verificados
- [ ] **Aplicação** acessível

### Após o Deploy
- [ ] **Status** da aplicação verificado
- [ ] **Logs** monitorados
- [ ] **Performance** testada
- [ ] **Backup** configurado
- [ ] **Domínio** configurado (se necessário)

---

**HyperDeploy - Configurações para todos os tipos de aplicação** ⚙️

*Use estes exemplos como base para suas configurações!* 