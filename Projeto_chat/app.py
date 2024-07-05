from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Configure a chave API
try:
    genai.configure(api_key="AIzaSyBJTeFoirEKS6y1b0T5Mn95ZiBBMJN9ybg")
    model = genai.GenerativeModel('gemini-pro')
    logging.info("Modelo generativo configurado com sucesso.")
except Exception as e:
    logging.error(f"Erro ao configurar o modelo generativo: {e}")
    model = None

# Função para ler textos do arquivo
def ler_textos():
    try:
        with open('data/textos.txt', 'r', encoding='utf-8') as file:
            textos = file.read()
        return textos
    except Exception as e:
        logging.error(f"Erro ao ler textos: {e}")
        return ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_response():
    data = request.json
    user_input = data.get('message')
    textos = ler_textos()

    if not user_input:
        return jsonify({"response": "Por favor, insira uma mensagem."})

    if not model:
        return jsonify({"response": "O modelo generativo não está configurado. Tente novamente mais tarde."}), 500

    # Montar o prompt com a pergunta do usuário e os textos lidos
    prompt = f"Textos:\n{textos}\n\nPergunta:\n{user_input}\n\nResposta:"

    try:
        chat = model.start_chat(history=[])  # Iniciar um novo chat para cada requisição
        response = chat.send_message(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        logging.error(f"Erro no chat: {e}")
        return jsonify({"response": "Ocorreu um erro ao processar sua solicitação. Tente novamente mais tarde."}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
