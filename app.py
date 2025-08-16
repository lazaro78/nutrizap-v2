import requests
from flask import Flask, request

app = Flask(__name__)

# ===================================================================
# SUAS CREDENCIAIS E LINK DE CHECKOUT - JÁ CONFIGURADOS
# ===================================================================
ULTRAMSG_INSTANCE_ID = "instance138876"
ULTRAMSG_TOKEN = "4hxm72jbbso7qmje"
ULTRAMSG_API_URL = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"
CHECKOUT_LINK = "https://pay.cakto.com.br/tayduyr_496632"

def enviar_resposta(destinatario, texto ):
    """Envia uma mensagem de texto para o usuário via UltraMsg."""
    params = {
        "token": ULTRAMSG_TOKEN,
        "to": destinatario,
        "body": texto,
        "priority": 1
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        response = requests.post(ULTRAMSG_API_URL, data=params, headers=headers)
        response.raise_for_status()
        print(f"Resposta enviada para {destinatario}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar resposta: {e}")

def processa_mensagem(dados_da_mensagem):
    """Função principal que processa a mensagem e envia a resposta."""
    try:
        remetente = dados_da_mensagem['de']
        mensagem_texto = dados_da_mensagem['corpo']
        msg_lower = mensagem_texto.lower()

        print(f"Processando mensagem: '{mensagem_texto}' de {remetente}")

        # Ignora mensagens do próprio bot para evitar loops
        if dados_da_mensagem.get('fromMe') is True:
            print("Mensagem do próprio bot ignorada.")
            return

        # Fluxo de Boas-vindas
        if 'oi' in msg_lower or 'olá' in msg_lower:
            enviar_resposta(remetente,
                            "👋 Olá! Seja bem-vindo(a) ao *NutriZap*.\n\n"
                            "💡 Fazemos *uma avaliação nutricional grátis* da sua refeição para você conhecer nosso serviço.\n"
                            "📸 Envie agora a foto do seu prato para começarmos!")
            return

        # Simulação de recebimento de foto
        if 'foto' in msg_lower or 'prato' in msg_lower or 'refeição' in msg_lower:
            enviar_resposta(remetente, "🔍 Analisando sua refeição... 🍽️")
            enviar_resposta(remetente,
                            "✅ Avaliação concluída!\n\n"
                            "🍅 Sua refeição está equilibrada, mas poderia ter mais vegetais e menos carboidratos simples.\n"
                            "💪 Com nosso *plano Premium*, você recebe análises ilimitadas, dicas personalizadas e suporte 24h pelo WhatsApp.")
            enviar_resposta(remetente,
                            "🔥 Garanta agora seu acesso Premium e continue recebendo análises instantâneas!\n"
                            f"💳 Clique aqui para assinar: {CHECKOUT_LINK}")
            return

        # Resposta para quem pergunta sobre o plano
        if 'assinar' in msg_lower or 'premium' in msg_lower:
            enviar_resposta(remetente,
                            f"💳 Aqui está seu link para assinar e liberar acesso imediato:\n{CHECKOUT_LINK}")
            return

        # Resposta padrão
        enviar_resposta(remetente,
                        "🤖 Desculpe, não entendi.\n"
                        "Envie *oi* para começar ou envie a foto do seu prato. 📸")

    except (KeyError, TypeError) as e:
        print(f"Erro ao processar os dados da mensagem: {e}")


@app.route('/webhook', methods=['POST'])
def webhook():
    """Recebe os webhooks da UltraMsg."""
    webhook_data = request.get_json()
    print("================ DADOS RECEBIDOS ===============")
    print(webhook_data)
    print("==================================================")

    # Verifica se a chave 'data' (em inglês) existe
    if webhook_data and 'data' in webhook_data:
        processa_mensagem(webhook_data['data'])
    else:
        print("Webhook recebido com formato inválido ou sem a chave 'data'.")
    
    return "OK", 200

@app.route('/', methods=['GET'])
def index():
    return "Bot NutriZap está online e funcionando!", 200

if __name__ == '__main__':
    app.run(debug=True)
