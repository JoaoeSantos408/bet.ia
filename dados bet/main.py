from flask import Flask
import requests
import json
from datetime import datetime
import os

app = Flask(__name__)

# CONFIGURAÇÕES DO BOT
TOKEN = 'SEU_TOKEN_AQUI'  # Substitua aqui pelo token real do seu bot
CANAL = -1001234567890    # Substitua pelo ID do seu canal privado

def main():
    hoje = datetime.now().strftime('%d-%m-%Y')

    try:
        with open('palpites.json', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        return f"Erro ao ler o arquivo JSON: {e}"

    palpites_do_dia = dados.get(hoje)

    if not palpites_do_dia:
        mensagem = f"⚠️ Nenhum palpite disponível para hoje ({hoje})."
    else:
        mensagem = "\n\n".join(palpites_do_dia)

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {
        'chat_id': CANAL,
        'text': mensagem
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        return "✅ Enviado com sucesso!"
    else:
        return f"❌ Erro ao enviar: {response.text}"

@app.route('/')
def index():
    return main()

# ✅ ESTE BLOCO É O QUE PERMITE O FUNCIONAMENTO NO RENDER
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
