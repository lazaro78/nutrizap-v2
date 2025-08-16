import requests
import json

# Configurações da UltraMsg API (substitua pelos seus dados)
ULTRAMSG_INSTANCE_ID = 'instance138876'
ULTRAMSG_TOKEN = '4hxm72jbbso7qmje'
ULTRAMSG_API_URL = f'https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat'

CHECKOUT_LINK = 'https://pay.cakto.com.br/tayduyr_496632'

def send_message(chat_id, text):
    payload = {
        'token': ULTRAMSG_TOKEN,
        'to': chat_id,
        'body': text
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(ULTRAMSG_API_URL, data=payload, headers=headers)
    return response.json()

def handle_message(message_body, chat_id):
    message_body_lower = message_body.lower()

    # Boas-vindas
    if 'oi' in message_body_lower or 'olá' in message_body_lower:
        send_message(chat_id,
                     "👋 Olá! Seja bem-vindo(a) ao *NutriZap*.\n\n" +
                     "💡 Fazemos *uma avaliação nutricional grátis* da sua refeição para você conhecer nosso serviço. \n" +
                     "📸 Envie agora a foto do seu prato para começarmos!")

    # Recebe foto para avaliação (UltraMsg API requer um webhook para receber mídias)
    # Para simplificar, vamos simular a recepção de uma foto com uma mensagem de texto específica por enquanto.
    elif 'foto' in message_body_lower and 'prato' in message_body_lower:
        send_message(chat_id, "🔍 Analisando sua refeição... 🍽️")
        # Simula 


        # Simula "análise"
        # Em um ambiente real, você processaria a imagem aqui.
        send_message(chat_id,
                     "✅ Avaliação concluída!\n\n" +
                     "🍅 Sua refeição está equilibrada, mas poderia ter mais vegetais e menos carboidratos simples.\n" +
                     "💪 Com nosso *plano Premium*, você recebe análises ilimitadas, dicas personalizadas e suporte 24h pelo WhatsApp.")

        # Gatilho para venda
        send_message(chat_id,
                     "🔥 Garanta agora seu acesso Premium e continue recebendo análises instantâneas!\n" +
                     f"💳 Clique aqui para assinar: {CHECKOUT_LINK}")

    # Caso o usuário fale de assinar
    elif 'assinar' in message_body_lower or 'premium' in message_body_lower:
        send_message(chat_id,
                     f"💳 Aqui está seu link para assinar e liberar acesso imediato:\n{CHECKOUT_LINK}")

    # Resposta padrão
    else:
        send_message(chat_id,
                     "🤖 Desculpe, não entendi.\n" +
                     "Envie *oi* para começar ou envie a foto do seu prato. 📸")

# Exemplo de como você receberia uma mensagem (isso seria via webhook da UltraMsg)
# No PythonAnywhere, você configuraria um web app Flask/Django para receber esses webhooks.
# Por enquanto, vamos simular uma chamada para testar a lógica.

# if __name__ == "__main__":
#     # Simulação de uma mensagem recebida
#     # Em um ambiente real, 'message_body' e 'chat_id' viriam do webhook da UltraMsg
#     test_message_body = "Olá"
#     test_chat_id = "5511999999999@c.us" # Substitua por um número de teste real
#     handle_message(test_message_body, test_chat_id)
#     print("Mensagem de teste processada. Verifique o WhatsApp do número de teste.")

# Para o PythonAnywhere, você precisaria de um framework web como Flask ou Django
# para criar um endpoint que a UltraMsg possa chamar (webhook).
# Exemplo básico com Flask:

from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("================ DADOS RECEBIDOS ===============")
    print(data)  # Esta linha vai imprimir os dados no log do Render
    print("==================================================")
    
    if data:
        resposta = processar_mensagem(data)
        enviar_resposta(resposta)
        return "OK", 200
    else:
        return "Nenhum dado recebido", 400

# Para rodar localmente para testes (não no PythonAnywhere diretamente)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


