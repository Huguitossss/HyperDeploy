# 🎮 Guia de Uso - HyperDeploy

Este guia ensina como usar todas as funcionalidades do HyperDeploy de forma eficiente.

## 📋 Índice

- [Comandos Básicos](#-comandos-básicos)
- [Painel de Usuário](#-painel-de-usuário)
- [Painel Administrativo](#-painel-administrativo)
- [Sistema de Pagamentos](#-sistema-de-pagamentos)
- [Gerenciamento de Aplicações](#-gerenciamento-de-aplicações)
- [Dicas e Truques](#-dicas-e-truques)

## 🔧 Comandos Básicos

### `/ping`
Testa a conectividade do bot.
```
/ping
```
**Resposta**: Latência do bot em milissegundos

### `/status` (Apenas Admins)
Mostra status detalhado do sistema.
```
/status
```
**Resposta**: Status do bot, API, limpeza automática e uptime

### `/cleanup` (Apenas Admins)
Força limpeza de arquivos expirados.
```
/cleanup
```
**Resposta**: Relatório de arquivos removidos

## 🎮 Painel de Usuário (`/userpanel`)

O painel de usuário é acessível a todos os membros do servidor e oferece funcionalidades básicas.

### Como Acessar
```
/userpanel
```

### Funcionalidades Disponíveis

#### 🚀 Deploy
- **Abrir Ticket**: Cria um ticket para upload de arquivo
- **Ver Status**: Mostra status do último deploy
- **Histórico**: Lista deploys anteriores

#### 🗑️ Deletar
- **Listar Apps**: Mostra todas as aplicações
- **Selecionar**: Escolha aplicação para deletar
- **Confirmar**: Confirma a exclusão

#### 🔑 Chave
- **Configurar**: Define sua chave da Square Cloud
- **Testar**: Testa a conectividade
- **Ver Status**: Mostra status da chave

#### 💳 Pagamentos
- **Ver Histórico**: Lista pagamentos realizados
- **Status**: Mostra status de pagamentos pendentes
- **Detalhes**: Informações detalhadas de cada pagamento

#### 📊 Status
- **Listar Apps**: Mostra todas as aplicações
- **Ver Status**: Status detalhado de uma aplicação
- **Controlar**: Start/Stop/Restart aplicações

#### 🗂️ Backups
- **Listar**: Mostra backups disponíveis
- **Criar**: Cria novo backup
- **Restaurar**: Restaura backup selecionado

#### 🌐 Domínios
- **Listar**: Mostra domínios configurados
- **Adicionar**: Adiciona novo domínio
- **Remover**: Remove domínio existente

#### ℹ️ Info
- **Sobre**: Informações do bot
- **Comandos**: Lista de comandos disponíveis
- **Status**: Status geral do sistema

## 🛠️ Painel Administrativo (`/panel`)

O painel administrativo é acessível apenas a administradores e oferece controle total do sistema.

### Como Acessar
```
/panel
```

### Funcionalidades Disponíveis

#### ⚙️ Configuração
- **Ver Configurações**: Mostra configurações atuais
- **Testar Conexão**: Testa conectividade com Square Cloud
- **Status do Sistema**: Status completo do sistema

#### 🗂️ Backups
- **Listar Backups**: Mostra todos os backups
- **Criar Backup**: Cria backup de aplicação
- **Restaurar Backup**: Restaura backup selecionado

#### 🌐 Domínios
- **Listar Domínios**: Mostra domínios configurados
- **Adicionar Domínio**: Adiciona novo domínio
- **Remover Domínio**: Remove domínio existente

#### 📊 Status
- **Listar Apps**: Mostra todas as aplicações
- **Ver Status**: Status detalhado de aplicação
- **Controlar Apps**: Start/Stop/Restart aplicações

#### 💳 Pagamentos
- **Ver Pendentes**: Lista pagamentos pendentes
- **Gerenciar**: Aprova/rejeita pagamentos
- **Histórico**: Histórico completo de pagamentos

## 💰 Sistema de Pagamentos

### Como Funciona
1. **Usuário** solicita deploy via `/userpanel`
2. **Bot** cria ticket e gera QR Code PIX
3. **Usuário** paga via PixGG
4. **Sistema** detecta pagamento automaticamente
5. **Bot** executa deploy e fecha ticket

### Processo Completo

#### 1. Solicitar Deploy
```
/userpanel → 🚀 Deploy → Abrir Ticket
```

#### 2. Upload do Arquivo
- Envie arquivo `.zip` no ticket criado
- Aguarde confirmação do upload

#### 3. Pagamento PIX
- QR Code será gerado automaticamente
- Escaneie com seu app bancário
- Confirme o pagamento

#### 4. Deploy Automático
- Sistema detecta pagamento
- Executa deploy na Square Cloud
- Notifica conclusão
- Fecha ticket automaticamente

### Status de Pagamentos
- **⏳ Pendente**: Aguardando pagamento
- **✅ Pago**: Pagamento confirmado
- **❌ Expirado**: Tempo esgotado
- **🔄 Processando**: Deploy em andamento

## 🎯 Gerenciamento de Aplicações

### Seleção Interativa
O HyperDeploy usa um sistema único de seleção:

1. **Lista Aplicações**: Bot mostra lista numerada
2. **Digite o Número**: Responda com o número da aplicação
3. **Confirmação**: Bot confirma a seleção
4. **Ação**: Execute a ação desejada

### Exemplo de Seleção
```
Bot: "📋 Aplicações disponíveis:
1. MeuApp (online)
2. TestApp (offline)
3. WebApp (online)

Digite o número da aplicação:"

Usuário: "2"

Bot: "✅ Selecionado: TestApp (offline)
O que deseja fazer?"
```

### Controles de Aplicação
- **▶️ Start**: Inicia a aplicação
- **⏹️ Stop**: Para a aplicação
- **🔄 Restart**: Reinicia a aplicação
- **📊 Status**: Mostra status detalhado

## 📁 Gerenciamento de Backups

### Criar Backup
1. Acesse **Backups** no painel
2. Selecione aplicação
3. Clique em **Criar Backup**
4. Aguarde confirmação

### Restaurar Backup
1. Acesse **Backups** no painel
2. Selecione backup desejado
3. Clique em **Restaurar**
4. Confirme a ação

### Listar Backups
- Mostra todos os backups disponíveis
- Inclui data, tamanho e status
- Permite download direto

## 🌐 Gerenciamento de Domínios

### Adicionar Domínio
1. Acesse **Domínios** no painel
2. Clique em **Adicionar Domínio**
3. Digite o domínio
4. Confirme a adição

### Remover Domínio
1. Acesse **Domínios** no painel
2. Selecione domínio
3. Clique em **Remover**
4. Confirme a remoção

## 🔧 Dicas e Truques

### Mensagens Auto-Destrutivas
- Todas as mensagens são removidas automaticamente
- Tempos variam de 5 a 30 segundos
- Evita spam no chat

### Seleção Rápida
- Use números para seleção rápida
- Não precisa digitar nomes completos
- Sistema é case-insensitive

### Logs Detalhados
- Todos os comandos são logados
- Verifique `logs/hyperdeploy.log` para debug
- Logs incluem usuário, comando e resultado

### Limpeza Automática
- QR Codes são removidos após 1 hora
- Uploads são removidos após 24 horas
- Sistema funciona automaticamente

### Permissões
- **Usuários**: Acesso ao `/userpanel`
- **Administradores**: Acesso total ao `/panel`
- **Sistema**: Comandos `/ping`, `/cleanup`, `/status`

## 🚨 Solução de Problemas

### Bot Não Responde
1. Verifique se está online
2. Teste com `/ping`
3. Verifique permissões

### Erro de Seleção
1. Digite apenas o número
2. Aguarde a lista aparecer
3. Verifique se a aplicação existe

### Pagamento Não Detectado
1. Aguarde alguns minutos
2. Verifique se o pagamento foi confirmado
3. Use `/cleanup` para limpar QR Codes antigos

### Upload Falhou
1. Verifique tamanho do arquivo (máx.MB é setado dinâmicamente)
2. Certifique-se que é um arquivo `.zip`
3. Tente novamente

## 📞 Suporte

Se precisar de ajuda:

1. **Verifique este guia** primeiro
2. **Consulte os logs** em `logs/hyperdeploy.log`
3. **Teste comandos básicos** como `/ping`
4. **Entre em contato** via Discord

---

**🎮 Agora você sabe usar o HyperDeploy! Divirta-se!** 