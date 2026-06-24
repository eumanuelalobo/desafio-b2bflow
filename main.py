import os
import logging
import requests
from dotenv import load_dotenv

# Configuração de Logs para auditoria e monitoramento profissional
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Carrega as variáveis de ambiente do arquivo .env de forma segura
load_dotenv()

# Inicialização das credenciais lidas do ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")

def buscar_contatos_supabase():
    """
    Realiza uma requisição HTTP GET na API REST do Supabase 
    para buscar até 3 contatos cadastrados na tabela 'contatos'.
    
    Returns:
        list: Lista de dicionários contendo os dados dos contatos ou lista vazia em caso de falha.
    """
    logging.info("Buscando contatos no Supabase...")
    url = f"{SUPABASE_URL}/rest/v1/contatos"
    
    # Cabeçalhos necessários para autenticação na API REST do Supabase
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    
    # Filtros da API: seleciona apenas colunas relevantes e limita o retorno
    params = {
        "select": "nome,telefone",
        "limit": 3
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Lança uma exceção caso o status não seja 2xx
        contatos = response.json()
        logging.info(f"Sucesso: {len(contatos)} contato(s) encontrado(s).")
        return contatos
    except Exception as e:
        logging.error(f"Erro ao buscar dados no Supabase: {e}")
        return []

def enviar_mensagem_zapi(nome, telefone):
    """
    Envia uma mensagem de texto personalizada via WhatsApp utilizando a API da Z-API.
    
    Args:
        nome (str): Nome do destinatário para personalização da mensagem.
        telefone (str): Número do telefone formatado (ex: 5511999999999).
        
    Returns:
        bool: True se o envio for bem-sucedido, False caso contrário.
    """
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"
    
    # Cabeçalhos exigidos pela Z-API, incluindo o token de validação do cliente
    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN
    }
    
    mensagem = f"Olá, {nome} tudo bem com você?"
    
    payload = {
        "phone": str(telefone).strip(),
        "message": mensagem
    }
    
    try:
        logging.info(f"Enviando mensagem para {nome} ({telefone})...")
        response = requests.post(url, json=payload, headers=headers)
        
        # Caso a API retorne um status diferente de 200, loga a resposta textual do servidor
        if response.status_code != 200:
            logging.error(f"Erro detalhado da Z-API: {response.text}")
            
        response.raise_for_status()
        logging.info(f"Mensagem enviada com sucesso para {nome}!")
        return True
    except Exception as e:
        logging.error(f"Falha ao enviar mensagem para {nome}: {e}")
        return False

def main():
    """Função principal que gerencia o fluxo de execução do script."""
    # Validação de segurança para garantir que nenhuma variável de ambiente está nula
    if not all([SUPABASE_URL, SUPABASE_KEY, ZAPI_INSTANCE_ID, ZAPI_TOKEN, ZAPI_CLIENT_TOKEN]):
        logging.error("Erro: Variáveis de ambiente faltando no arquivo .env!")
        return

    # Executa a busca no banco de dados
    contatos = buscar_contatos_supabase()
    
    if not contatos:
        logging.warning("Nenhum contato encontrado para processar.")
        return

    # Itera sobre os contatos e