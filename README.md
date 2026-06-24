# Desafio Técnico - Integração Supabase & Z-API (b2bflow)

Este repositório contém a solução desenvolvida para o desafio técnico da b2bflow. O objetivo principal do projeto é realizar a integração automatizada entre um banco de dados relacional e um serviço de mensageria para WhatsApp.

## 🚀 O que o projeto faz?

O script foi desenvolvido em **Python** e realiza o seguinte fluxo de dados:
1. Conecta de forma segura ao banco de dados **Supabase** via API REST.
2. Busca e consome os dados de até 3 contatos cadastrados na tabela `contatos`.
3. Valida os dados e dispara, de forma sequencial, uma mensagem personalizada para o WhatsApp de cada contato através da **Z-API**.
4. Conta com um sistema completo de **Auditoria por Logs** (`logging`) para monitoramento de sucesso e tratamento de falhas em tempo real.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **Supabase** (Banco de dados e API REST)
* **Z-API** (API de integração com WhatsApp)
* **Requests** (Consumo de APIs HTTP)
* **Python-Dotenv** (Gerenciamento seguro de variáveis de ambiente)

---

## 📦 Configuração e Execução

### 1. Variáveis de Ambiente
O projeto utiliza um arquivo `.env` para proteger credenciais sensíveis (configurado no `.gitignore`). Para rodar o projeto, crie um arquivo `.env` na raiz com a seguinte estrutura:

```env
SUPABASE_URL="sua_url_do_supabase"
SUPABASE_KEY="seu_token_jwt_anon_key"
ZAPI_INSTANCE_ID="id_da_sua_instancia"
ZAPI_TOKEN="token_da_sua_instancia"
ZAPI_CLIENT_TOKEN="seu_client_token_da_conta"

### 2. Instalação e execução

No terminal, instale as dependências e execute o script principal:
# Instalar dependências
pip install -r requirements.txt

# Executar o script
python main.py

---

### 💻 Comandos para enviar pro terminal:

Depois de salvar o arquivo `README.md`, copie e cole essa linha única no seu terminal do VS Code para subir tudo de vez:

```bash
git add README.md && git commit -m "docs: adiciona README detalhando o projeto" && git push origin main
