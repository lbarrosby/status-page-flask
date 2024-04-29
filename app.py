from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

# Função para verificar o status do Google
def check_google_status():
    try:
        response = requests.get('https://www.google.com')
        if response.status_code == 200:
            return 'Healthy'
        else:
            return 'Unhealthy'
    except:
        return 'Unhealthy'

# Função para verificar o status do Rancher
def check_rancher_status():
    try:
        response = requests.get('https://www.rancher.com/')
        if response.status_code == 200:
            return 'Healthy'
        else:
            return 'Unhealthy'
    except:
        return 'Unhealthy'

# Função para carregar os eventos do arquivo eventos.txt
def carregar_eventos():
    try:
        with open('eventos.txt', 'r') as file:
            eventos = []
            for linha in file:
                partes = linha.strip().split(':')
                if len(partes) == 3:
                    nome, descricao = partes[1:]
                    eventos.append({'nome': nome, 'descricao': descricao})
                else:
                    print(f"Aviso: linha inválida no arquivo eventos.txt: {linha}")
            return eventos
    except FileNotFoundError:
        return []

# Função para salvar os eventos no arquivo eventos.txt
def salvar_eventos(eventos):
    with open('eventos.txt', 'w') as file:
        for idx, evento in enumerate(eventos, start=1):
            file.write(f"{idx}:{evento['nome']}:{evento['descricao']}\n")

# Função para adicionar um evento
def adicionar_evento(nome, descricao):
    eventos = carregar_eventos()
    novo_evento = {'nome': nome, 'descricao': descricao}
    eventos.append(novo_evento)
    salvar_eventos(eventos)

# Função para excluir um evento
def excluir_evento(evento_id):
    try:
        idx = int(evento_id) - 1
        eventos = carregar_eventos()
        if 0 <= idx < len(eventos):
            del eventos[idx]
            salvar_eventos(eventos)
            return True
        else:
            return False
    except ValueError:
        return False

# Rota para a página inicial
@app.route('/')
def index():
    google_status = check_google_status()
    rancher_status = check_rancher_status()
    eventos = carregar_eventos()
    return render_template('status_page.html', google_status=google_status, rancher_status=rancher_status, eventos=eventos)

# Rota para a página de adição de evento
@app.route('/adicionar_evento', methods=['GET'])
def mostrar_formulario_adicionar_evento():
    return render_template('adicionar_evento.html')

# Rota para adicionar um evento
@app.route('/adicionar_evento', methods=['POST'])
def adicionar_evento_rota():
    nome = request.form['nome']
    descricao = request.form['descricao']
    adicionar_evento(nome, descricao)
    return redirect('/')

# Rota para a página de exclusão de evento
@app.route('/delete_evento', methods=['GET'])
def mostrar_formulario_excluir_evento():
    return render_template('delete_evento.html')

# Rota para excluir um evento
@app.route('/delete_evento', methods=['POST'])
def excluir_evento_rota():
    evento_id = request.form['evento_id']
    if excluir_evento(evento_id):
        return redirect('/')
    else:
        return "Evento não encontrado ou ID inválido."

if __name__ == '__main__':
    app.run(debug=True)
