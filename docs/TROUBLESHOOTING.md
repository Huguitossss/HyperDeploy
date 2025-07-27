# 🔧 Troubleshooting - HyperDeploy

Guia completo para resolver problemas comuns e avançados no HyperDeploy.

## 📋 Índice

- [Problemas de Configuração](#problemas-de-configuração)
- [Problemas de Deploy](#problemas-de-deploy)
- [Problemas de Pagamento](#problemas-de-pagamento)
- [Problemas de Performance](#problemas-de-performance)
- [Problemas de Integração](#problemas-de-integração)
- [Logs e Debug](#logs-e-debug)
- [Contato e Suporte](#contato-e-suporte)

## ⚙️ Problemas de Configuração

### ❌ Bot não inicia

#### Sintomas
- Bot não aparece online no Discord
- Erro de token inválido
- Bot não responde a comandos

#### Soluções
1. **Verificar Token Discord**
   ```bash
   # Verifique se o token está correto em config/bot.yaml
   bot_token: "SEU_TOKEN_AQUI"
   ```

2. **Verificar Permissões**
   - Bot precisa de permissões de administrador
   - Verificar se foi adicionado ao servidor
   - Confirmar se tem permissão para usar slash commands

3. **Verificar Intents**
   ```python
   # Em bot.py, verificar se os intents estão corretos
   intents = discord.Intents.default()
   intents.message_content = True
   intents.members = True
   intents.presences = True
   ```

4. **Verificar Dependências**
   ```bash
   pip install -r requirements.txt
   pip list | grep discord
   ```

#### Logs de Erro
```
ERROR - Invalid token for bot
ERROR - Missing required intent
ERROR - Bot not in guild
```

### ❌ Comandos não funcionam

#### Sintomas
- Comandos slash não aparecem
- Bot não responde a comandos
- Erro de permissão

#### Soluções
1. **Sincronizar Comandos**
   ```python
   # O bot sincroniza automaticamente na inicialização
   # Verificar logs de sincronização
   ```

2. **Verificar Guild ID**
   ```yaml
   # Em config/bot.yaml
   guild_id: SEU_GUILD_ID_AQUI  # ID do servidor
   ```

3. **Verificar Permissões**
   - Bot precisa de permissão "Use Slash Commands"
   - Verificar se está no servidor correto
   - Confirmar se tem permissões adequadas

4. **Reiniciar Bot**
   ```bash
   # Parar e reiniciar o bot
   python bot.py
   ```

#### Logs de Erro
```
ERROR - Application command failed
ERROR - Missing permissions
ERROR - Guild not found
```

## 🚀 Problemas de Deploy

### ❌ Arquivo ZIP inválido

#### Sintomas
- Erro ao fazer upload
- "Arquivo não suportado"
- "Estrutura inválida"

#### Soluções
1. **Verificar Extensão**
   ```bash
   # Arquivo deve ter extensão .zip
   meu-projeto.zip  # ✅ Correto
   meu-projeto.rar  # ❌ Incorreto
   ```

2. **Verificar Tamanho**
   ```bash
   # Verificar tamanho do arquivo
   ls -lh meu-projeto.zip
   # Deve estar dentro do limite configurado
   ```

3. **Verificar Estrutura**
   ```
   meu-projeto/
   ├── main.py              # ✅ Arquivo principal
   ├── squarecloud.app      # ✅ Configuração obrigatória
   ├── requirements.txt     # ✅ Dependências
   └── src/                 # ✅ Código fonte
   ```

4. **Testar ZIP Localmente**
   ```bash
   # Extrair e testar localmente
   unzip meu-projeto.zip
   cd meu-projeto
   python main.py
   ```

#### Logs de Erro
```
ERROR - Invalid file format
ERROR - File too large
ERROR - Missing squarecloud.app
```

### ❌ squarecloud.app não encontrado

#### Sintomas
- "squarecloud.app não encontrado"
- Deploy falha na validação
- Erro de configuração

#### Soluções
1. **Verificar Localização**
   ```
   # Deve estar na raiz do ZIP
   meu-projeto/
   ├── squarecloud.app      # ✅ Na raiz
   └── src/
       └── squarecloud.app  # ❌ Não na raiz
   ```

2. **Verificar Nome**
   ```ini
   # Nome exato (sem extensão)
   squarecloud.app          # ✅ Correto
   squarecloud.config       # ✅ Alternativo
   squarecloud.txt          # ❌ Incorreto
   ```

3. **Verificar Sintaxe**
   ```ini
   # Sintaxe correta
   DISPLAY_NAME=Minha App
   MAIN=main.py
   VERSION=recommended
   MEMORY=512
   AUTORESTART=true
   ```

4. **Testar Configuração**
   ```bash
   # Validar sintaxe
   cat squarecloud.app
   # Verificar se não há caracteres especiais
   ```

#### Logs de Erro
```
ERROR - squarecloud.app not found
ERROR - Invalid configuration syntax
ERROR - Missing required fields
```

### ❌ Aplicação não inicia

#### Sintomas
- Deploy bem-sucedido mas app offline
- Erro nos logs da aplicação
- Aplicação para logo após iniciar

#### Soluções
1. **Verificar Arquivo Principal**
   ```ini
   # Em squarecloud.app
   MAIN=main.py  # Verificar se o arquivo existe
   ```

2. **Verificar Dependências**
   ```txt
   # Em requirements.txt
   flask==2.3.0
   discord.py==2.6.1
   # Verificar se todas estão listadas
   ```

3. **Verificar Logs da Aplicação**
   ```bash
   # Acessar logs no painel da Square Cloud
   # Procurar por erros específicos
   ```

4. **Testar Localmente**
   ```bash
   # Testar antes do deploy
   pip install -r requirements.txt
   python main.py
   ```

#### Logs de Erro Comuns
```
ERROR - Module not found
ERROR - Port already in use
ERROR - Permission denied
ERROR - Invalid syntax
```

## 💳 Problemas de Pagamento

### ❌ QR Code não gera

#### Sintomas
- QR Code não aparece
- Erro ao gerar pagamento
- "Erro no Mercado Pago"

#### Soluções
1. **Verificar Token Mercado Pago**
   ```yaml
   # Em config/bot.yaml
   mercadopago_access_token: "SEU_ACCESS_TOKEN_AQUI"
   ```

2. **Verificar Conta Mercado Pago**
   - Conta deve estar ativa
   - Verificar se não há restrições
   - Confirmar se é conta de desenvolvedor

3. **Verificar Configuração**
   ```python
   # Verificar se o Mercado Pago está habilitado
   mercadopago_enabled: true
   ```

4. **Testar API Manualmente**
   ```python
   import requests
   
   url = "https://api.mercadopago.com/v1/payments"
   headers = {"Authorization": "Bearer SEU_TOKEN"}
   data = {"transaction_amount": 10.00, "payment_method_id": "pix"}
   
   response = requests.post(url, json=data, headers=headers)
   print(response.json())
   ```

#### Logs de Erro
```
ERROR - Mercado Pago API error
ERROR - Invalid access token
ERROR - Payment creation failed
```

### ❌ Pagamento não confirma

#### Sintomas
- QR Code gerado mas pagamento não confirma
- "Aguardando pagamento" por muito tempo
- Deploy não inicia

#### Soluções
1. **Verificar Valor**
   - Confirmar valor exato do pagamento
   - Verificar se não há taxas adicionais
   - Confirmar moeda (BRL)

2. **Verificar Método de Pagamento**
   - Usar PIX (QR Code ou código)
   - Confirmar pagamento no app do banco
   - Aguardar confirmação

3. **Verificar Timeout**
   ```yaml
   # Em config/bot.yaml
   payment_timeout: 30  # Minutos
   ```

4. **Verificar Polling**
   ```python
   # O bot verifica a cada 5 segundos
   # Verificar logs de verificação
   ```

#### Logs de Erro
```
INFO - Payment pending
INFO - Checking payment status
ERROR - Payment timeout
```

### ❌ Deploy não inicia após pagamento

#### Sintomas
- Pagamento confirmado mas deploy não inicia
- "Aguardando deploy"
- Erro na Square Cloud

#### Soluções
1. **Verificar API Key Square Cloud**
   ```yaml
   # Em config/squarecloud.yaml
   api_key: "SUA_API_KEY_AQUI"
   ```

2. **Verificar Permissões**
   - API Key deve ter permissões de deploy
   - Verificar se não expirou
   - Confirmar se é válida

3. **Verificar Limites**
   - Verificar se não excedeu limites da conta
   - Confirmar se há espaço disponível
   - Verificar se não há aplicações duplicadas

4. **Verificar Logs**
   ```bash
   # Verificar logs do bot
   # Procurar por erros específicos
   ```

#### Logs de Erro
```
ERROR - Square Cloud API error
ERROR - Application creation failed
ERROR - Insufficient resources
```

## ⚡ Problemas de Performance

### ❌ Bot lento

#### Sintomas
- Comandos demoram para responder
- Latência alta
- Timeout de comandos

#### Soluções
1. **Verificar Recursos**
   ```ini
   # Em squarecloud.config
   "ram": 512,    # Aumentar se necessário
   "cpu": 25,     # Aumentar se necessário
   ```

2. **Otimizar Código**
   ```python
   # Usar async/await corretamente
   # Evitar operações bloqueantes
   # Usar cache quando possível
   ```

3. **Verificar Conexão**
   - Verificar latência de rede
   - Confirmar se APIs estão respondendo
   - Verificar rate limits

4. **Monitorar Uso**
   ```bash
   # Verificar uso de recursos
   # Monitorar logs de performance
   ```

#### Logs de Performance
```
INFO - Command executed in 2.5s
WARNING - High latency detected
ERROR - Command timeout
```

### ❌ Muitos erros

#### Sintomas
- Muitos erros nos logs
- Bot instável
- Funcionalidades quebradas

#### Soluções
1. **Verificar Tratamento de Erros**
   ```python
   try:
       # Código que pode gerar erro
       result = await api_call()
   except Exception as e:
       logger.error(f"Erro: {e}")
       # Tratamento adequado
   ```

2. **Verificar Dependências**
   ```bash
   # Atualizar dependências
   pip install --upgrade -r requirements.txt
   ```

3. **Verificar Configurações**
   ```yaml
   # Verificar todas as configurações
   # Confirmar se estão corretas
   ```

4. **Reiniciar Bot**
   ```bash
   # Reiniciar para limpar estado
   # Verificar se problemas persistem
   ```

#### Logs de Erro
```
ERROR - Unhandled exception
ERROR - API rate limit exceeded
ERROR - Connection timeout
```

## 🔗 Problemas de Integração

### ❌ Discord API

#### Sintomas
- Bot desconecta frequentemente
- Comandos não funcionam
- Erros de permissão

#### Soluções
1. **Verificar Gateway**
   ```python
   # Verificar se está usando gateway correto
   # Confirmar se intents estão configurados
   ```

2. **Verificar Rate Limits**
   - Respeitar rate limits do Discord
   - Implementar delays quando necessário
   - Usar bulk operations

3. **Verificar Permissões**
   ```python
   # Verificar permissões antes de executar comandos
   if not ctx.author.guild_permissions.administrator:
       await ctx.respond("❌ Permissão negada")
       return
   ```

#### Logs de Erro
```
ERROR - Discord API error
ERROR - Rate limit exceeded
ERROR - Missing permissions
```

### ❌ Square Cloud API

#### Sintomas
- Deploy falha
- Não consegue listar aplicações
- Erro de autenticação

#### Soluções
1. **Verificar API Key**
   ```yaml
   # Em config/squarecloud.yaml
   api_key: "SUA_API_KEY_AQUI"
   ```

2. **Verificar Endpoints**
   ```python
   # Verificar se endpoints estão corretos
   # Confirmar se API não mudou
   ```

3. **Implementar Retry**
   ```python
   # Implementar retry automático
   # Tratar erros temporários
   ```

#### Logs de Erro
```
ERROR - Square Cloud API error
ERROR - Invalid API key
ERROR - Application not found
```

### ❌ Mercado Pago API

#### Sintomas
- Pagamentos não funcionam
- QR Code não gera
- Erro de autenticação

#### Soluções
1. **Verificar Access Token**
   ```yaml
   # Em config/bot.yaml
   mercadopago_access_token: "SEU_ACCESS_TOKEN_AQUI"
   ```

2. **Verificar Conta**
   - Conta deve estar ativa
   - Verificar se não há restrições
   - Confirmar permissões

3. **Implementar Fallback**
   ```python
   # Implementar fallback para erros
   # Tratar diferentes tipos de erro
   ```

#### Logs de Erro
```
ERROR - Mercado Pago API error
ERROR - Invalid access token
ERROR - Payment creation failed
```

## 📊 Logs e Debug

### Estrutura de Logs
```
logs/
├── hyperdeploy.log          # Log principal
├── actions.log              # Log de ações
├── admin.log                # Log administrativo
├── payments.log             # Log de pagamentos
└── deploys.log              # Log de deploys
```

### Níveis de Log
- **DEBUG** - Informações detalhadas
- **INFO** - Informações gerais
- **WARNING** - Avisos
- **ERROR** - Erros
- **CRITICAL** - Erros críticos

### Comandos de Debug
```python
# No console do Discord
/debug status              # Status do sistema
/debug logs                # Ver logs recentes
/debug config              # Ver configurações
/debug test                # Testar integrações
```

### Logs Importantes
```bash
# Verificar logs em tempo real
tail -f logs/hyperdeploy.log

# Filtrar erros
grep "ERROR" logs/hyperdeploy.log

# Ver logs de pagamento
tail -f logs/payments.log
```

### Debug de Performance
```python
import time

async def measure_performance(func, *args, **kwargs):
    start_time = time.time()
    try:
        result = await func(*args, **kwargs)
        duration = time.time() - start_time
        logger.info(f"Função {func.__name__} executada em {duration:.2f}s")
        return result
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Erro em {func.__name__} após {duration:.2f}s: {e}")
        raise
```

## 📞 Contato e Suporte

### Canais de Suporte
- **Discord**: Servidor oficial do HyperDeploy
- **GitHub**: Issues do projeto
- **Email**: suporte@hyperdeploy.com

### Informações para Suporte
Ao reportar um problema, inclua:
- **Versão do HyperDeploy**
- **Sistema operacional**
- **Logs de erro**
- **Passos para reproduzir**
- **Configurações relevantes**

### Recursos Úteis
- **Documentação**: docs/ do projeto
- **FAQ**: Perguntas frequentes
- **Exemplos**: docs/CONFIGURATION_EXAMPLES.md
- **Comunidade**: Discord e GitHub

### Escalação de Problemas
1. **Verificar documentação** primeiro
2. **Pesquisar issues** existentes
3. **Criar issue** detalhada
4. **Fornecer logs** completos
5. **Aguardar resposta** da equipe

---

**HyperDeploy Troubleshooting - Resolva problemas rapidamente** 🔧

*Este guia cobre os problemas mais comuns. Para suporte adicional, entre em contato!* 