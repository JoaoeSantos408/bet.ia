from flask import Flask
import requests
import json
from datetime import datetime

app = Flask(__name__)

# CONFIGURAÇÕES
TOKEN = '7869611756:AAHkz2XV3j9XhX8rAqzSgos4VlVmnNdM3XQ'
CANAL = -1002802811664

def main():
    hoje = datetime.now().strftime('%d-%m-%Y')

    with open('palpites.json', encoding='utf-8') as f:
        dados = json.load(f)

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
        print("✅ Palpite enviado com sucesso!")
        return "✅ Enviado com sucesso!"
    else:
        print("❌ Erro:", response.text)
        return f"❌ Erro: {response.text}"

@app.route('/')
def index():
    return main()

# Mantém o app rodando
app.run(host='0.0.0.0', port=81)
