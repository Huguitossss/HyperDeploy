# ☁️ Guia de Deploy - HyperDeploy

Este guia ensina como fazer deploy do HyperDeploy na própria Square Cloud.

## 📋 Pré-requisitos

- ✅ Conta ativa na Square Cloud
- ✅ Projeto HyperDeploy configurado
- ✅ Configurações YAML preenchidas
- ✅ Bot Discord criado e configurado

## 🚀 Deploy na Square Cloud

### 1. Preparar o Projeto

#### Estrutura Necessária
```
HyperDeploy/
├── bot.py                 # ✅ Arquivo principal
├── requirements.txt       # ✅ Dependências
├── squarecloud.app        # ✅ Configuração Square Cloud
├── config/                # ✅ Configurações
│   ├── bot.yaml
│   ├── pixgg.yaml
│   └── squarecloud.yaml
├── core/                  # ✅ Código do bot
├── data/                  # ✅ Dados JSON
├── logs/                  # ✅ Logs
├── qrcodes/              # ✅ QR Codes
├── uploads/              # ✅ Uploads
└── docs/                 # ✅ Documentação
```

#### Verificar Arquivos
```bash
# Verificar se todos os arquivos estão presentes
ls -la
ls -la config/
ls -la core/
```

### 2. Criar Aplicação na Square Cloud

#### Acessar Square Cloud
1. Acesse [Square Cloud](https://squarecloud.app)
2. Faça login na sua conta
3. Clique em **"Criar Aplicação"**

#### Configurar Aplicação
1. **Nome**: `HyperDeploy`
2. **Tipo**: `Python`
3. **Versão**: `3.11`
4. **Ram**: `512 MB` (mínimo recomendado)
5. **Disco**: `1 GB` (suficiente)
6. **CPU**: `25%` (padrão)

#### Upload dos Arquivos
1. **Método**: Upload de arquivo
2. **Arquivo**: Compacte todo o projeto em `.zip`
3. **Estrutura**: Mantenha a estrutura de pastas

### 3. Configurar Variáveis de Ambiente

#### Variáveis Obrigatórias
```env
# Discord Bot
DISCORD_TOKEN=seu_token_discord_aqui
GUILD_ID=1175572640568709180

# Square Cloud
SQUARECLOUD_API_KEY=sua_api_key_aqui

# PixGG
PIXGG_EMAIL=seu_email@pixgg.com
PIXGG_PASSWORD=sua_senha_pixgg
PRECO_DEPLOY=10.00
```

#### Como Configurar
1. Na aplicação criada, vá em **"Configurações"**
2. Clique em **"Variáveis de Ambiente"**
3. Adicione cada variável individualmente
4. Clique em **"Salvar"**

### 4. Configurar Arquivo squarecloud.app

#### Criar Arquivo
```yaml
# squarecloud.app
main: bot.py
version: "3.11"
ram: 512
disk: 1024
cpu: 25
auto_restart: true
```

#### Parâmetros Detalhados

| Parâmetro |  Valor  | Descrição |
|-----------| ------- |-----------|
| `main`    | `bot.py`| Arquivo principal |
| `version` |  `3.11` | Versão do Python |
| `ram`     |  `512`  | RAM em MB |
| `disk`    |  `1024` | Disco em MB |
| `cpu`     |   `25`  | CPU em % |
| `auto_restart` | `true` | Reiniciar automaticamente |

### 5. Configurar Requirements.txt

#### Verificar Dependências
```txt
# requirements.txt
py-cord>=2.4.0
squarecloud-api>=1.0.0
requests>=2.31.0
aiofiles>=23.2.0
PyYAML>=6.0.1
qrcode>=7.4.2
Pillow>=10.0.0
```

#### Instalar Dependências
1. Square Cloud instala automaticamente
2. Verifique se não há erros
3. Logs mostram progresso da instalação

### 6. Fazer Deploy

#### Iniciar Aplicação
1. Clique em **"Iniciar"**
2. Aguarde o processo de deploy
3. Verifique os logs de inicialização

#### Verificar Funcionamento
1. **Logs**: Verifique se não há erros
2. **Status**: Deve aparecer como "Online"
3. **Bot**: Deve aparecer online no Discord

### 7. Configurações Avançadas

#### Configurar Domínio Personalizado
1. Vá em **"Domínios"**
2. Adicione seu domínio
3. Configure DNS conforme instruções

#### Configurar SSL
1. SSL é ativado automaticamente
2. Certificado Let's Encrypt gratuito
3. Renovação automática

#### Configurar Backup
1. Vá em **"Backups"**
2. Configure backup automático
3. Escolha frequência e retenção

## 🔧 Configurações Específicas

### Configuração para Produção
```yaml
# squarecloud.app (Produção)
main: bot.py
version: "3.11"
ram: 1024
disk: 2048
cpu: 50
auto_restart: true
backup: true
backup_interval: 24
```

### Configuração para Desenvolvimento
```yaml
# squarecloud.app (Desenvolvimento)
main: bot.py
version: "3.11"
ram: 256
disk: 512
cpu: 25
auto_restart: false
```

### Configuração com Proxy
```yaml
# squarecloud.app (Com Proxy)
main: bot.py
version: "3.11"
ram: 512
disk: 1024
cpu: 25
auto_restart: true
proxy: true
```

## 📊 Monitoramento

### Logs da Aplicação
1. **Acesse**: Painel da aplicação
2. **Vá em**: "Logs"
3. **Monitore**: Erros e informações

### Métricas de Performance
- **CPU**: Uso de processamento
- **RAM**: Uso de memória
- **Disco**: Espaço utilizado
- **Rede**: Tráfego de dados

### Alertas
1. Configure alertas para:
   - Alto uso de CPU/RAM
   - Aplicação offline
   - Erros críticos

## 🔒 Segurança

### Proteção de Tokens
- ✅ Use variáveis de ambiente
- ✅ Nunca commite tokens no Git
- ✅ Rotacione tokens regularmente

### Permissões
- ✅ Configure permissões mínimas necessárias
- ✅ Use roles específicos no Discord
- ✅ Monitore acesso administrativo

### Backup de Configurações
- ✅ Faça backup das configurações
- ✅ Documente todas as variáveis
- ✅ Mantenha cópias de segurança

## 🚨 Solução de Problemas

### Erro: "ModuleNotFoundError"
```bash
# Verificar requirements.txt
cat requirements.txt

# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "Invalid token"
- Verifique se `DISCORD_TOKEN` está correto
- Confirme se o bot está no servidor
- Teste o token localmente

### Erro: "ACCESS_DENIED"
- Verifique se `SQUARECLOUD_API_KEY` está correto
- Confirme se a conta está ativa
- Teste a API key

### Aplicação Não Inicia
1. Verifique os logs
2. Confirme variáveis de ambiente
3. Teste localmente primeiro
4. Verifique recursos disponíveis

### Bot Não Responde
1. Verifique se está online
2. Teste com `/ping`
3. Verifique permissões
4. Confirme configurações

## 📈 Otimização

### Performance
- **RAM**: Aumente se necessário
- **CPU**: Monitore uso
- **Disco**: Limpe arquivos temporários

### Custo
- **Plano Gratuito**: 512MB RAM, 1GB disco
- **Plano Pago**: Mais recursos disponíveis
- **Otimização**: Use recursos eficientemente

### Escalabilidade
- **Múltiplas Instâncias**: Para alta demanda
- **Load Balancer**: Distribuir carga
- **Cache**: Reduzir latência

## 🔄 Atualizações

### Atualizar Código
1. Faça upload da nova versão
2. Reinicie a aplicação
3. Verifique funcionamento

### Atualizar Configurações
1. Modifique variáveis de ambiente
2. Reinicie a aplicação
3. Teste funcionalidades

### Rollback
1. Use backup anterior
2. Restaure configurações
3. Verifique estabilidade

## 📞 Suporte

### Recursos Square Cloud
- **Documentação**: [docs.squarecloud.app](https://docs.squarecloud.app)
- **Discord**: [discord.gg/squarecloud](https://discord.gg/squarecloud)
- **Status**: [status.squarecloud.app](https://status.squarecloud.app)

### Logs Úteis
```bash
# Logs da aplicação
tail -f logs/hyperdeploy.log

# Logs do sistema
# Acesse via painel da Square Cloud
```

---

**☁️ Deploy concluído! O HyperDeploy está rodando na Square Cloud!** 