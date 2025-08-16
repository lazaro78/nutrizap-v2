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

def processa_mensagem(mensagem_texto, destinatario):
    """Processa a mensagem recebida e dispara as respostas apropriadas."""
    msg_lower = mensagem_texto.lower()

    # Fluxo de Boas-vindas
    if 'oi' in msg_lower or 'olá' in msg_lower:
        enviar_resposta(destinatario,
                        "👋 Olá! Seja bem-vindo(a) ao *NutriZap*.\n\n"
                        "💡 Fazemos *uma avaliação nutricional grátis* da sua refeição para você conhecer nosso serviço.\n"
                        "📸 Envie agora a foto do seu prato para começarmos!")

    # Simulação de recebimento de foto (o webhook de texto é o gatilho)
    elif 'foto' in msg_lower or 'prato' in msg_lower or 'refeição' in msg_lower:
        enviar_resposta(destinatario, "🔍 Analisando sua refeição... 🍽️")
        # Aqui você poderia adicionar um delay ou uma lógica de análise real no futuro
        enviar_resposta(destinatario,
                        "✅ Avaliação concluída!\n\n"
                        "🍅 Sua refeição está equilibrada, mas poderia ter mais vegetais e menos carboidratos simples.\n"
                        "💪 Com nosso *plano Premium*, você recebe análises ilimitadas, dicas personalizadas e suporte 24h pelo WhatsApp.")
        # Gatilho para venda
        enviar_resposta(destinatario,
                        "🔥 Garanta agora seu acesso Premium e continue recebendo análises instantâneas!\n"
                        f"💳 Clique aqui para assinar: {CHECKOUT_LINK}")

    # Resposta para quem pergunta sobre o plano
    elif 'assinar' in msg_lower or 'premium' in msg_lower:
        enviar_resposta(destinatario,
                        f"💳 Aqui está seu link para assinar e liberar acesso imediato:\n{CHECKOUT_LINK}")

    # Resposta padrão para mensagens não compreendidas
    else:
        enviar_resposta(destinatario,
                        "🤖 Desculpe, não entendi.\n"
                        "Envie *oi* para começar ou envie a foto do seu prato. 📸")

@app.route('/webhook', methods=['POST'])
def webhook():
    """Recebe os webhooks da UltraMsg."""
    data = request.get_json()
    print("================ DADOS RECEBIDOS ===============")
    print(data)
    print("==================================================")

    # Verifica se a estrutura de dados recebida é válida
    if data and 'dados' in data and 'de' in data['dados'] and 'corpo' in data['dados']:
        remetente = data['dados']['de']
        mensagem_recebida = data['dados']['corpo']
        
        # Ignora mensagens do próprio bot para evitar loops
        if data['dados'].get('fromMe') is True:
            return "Mensagem do próprio bot ignorada", 200
            
        processa_mensagem(mensagem_recebida, remetente)
        return "OK", 200
    else:
        print("Webhook recebido com formato inválido ou sem dados.")
        return "Formato de dados inválido", 400

@app.route('/', methods=['GET'])
def index():
    return "Bot NutriZap está online e funcionando!", 200

if __name__ == '__main__':
    # Esta parte é para testes locais e não é usada pelo Render
    app.run(debug=True)


