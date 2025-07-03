from flask import Flask
import requests
import json
from datetime import datetime
import os

app = Flask(__name__)

# Lê variáveis de ambiente configuradas no Render
TOKEN = os.environ.get('BOT_TOKEN')
CANAL = os.environ.get('TELEGRAM_CHANNEL_ID')

def main():
    hoje = datetime.now().strftime('%d-%m-%Y')

    try:
        with open('palpites.json', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        return f"❌ Erro ao carregar JSON: {e}"

    palpites_do_dia = dados.get(hoje)

    if not palpites_do_dia:
        mensagem = f"⚠️ Nenhum palpite disponível para hoje ({hoje})."
    else:
        # Compatível com estrutura antiga (string única)
        if isinstance(palpites_do_dia, str):
            palpites_do_dia = [palpites_do_dia]

        # Junta todos os palpites com 2 quebras de linha
        mensagem = "\n\n".join(palpites_do_dia)

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {
        'chat_id': CANAL,
        'text': mensagem
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("✅ Palpite enviado com sucesso!")
            return "✅ Enviado com sucesso!"
        else:
            print("❌ Erro:", response.text)
            return f"❌ Erro: {response.text}"
    except Exception as e:
        return f"❌ Erro ao tentar enviar mensagem: {e}"

@app.route('/')
def index():
    return main()

# Porta dinâmica exigida pelo Render
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
