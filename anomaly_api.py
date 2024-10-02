#!/usr/bin/env python3

#
# author : Gabriel Francisco
# email  : gabriel.francisco@ibm.com
# date   : 01/10/2024
# version: 0.2b

##########################
# SETUP INICIAL
##########################

from flask import Flask, request, jsonify
import joblib, smtplib, threading, time, configparser
from email.mime.text import MIMEText
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler

##########################
# FUNÇÕES
##########################

# Função para ler configurações
def read_config() -> configparser.ConfigParser:
    '''
    Função para ler as configurações do arquivo 'conf.cfg' utilizando a classe ConfigParser.

    Parâmetros:
    Nenhum

    Retorna:
    configparser.ConfigParser
        Um objeto ConfigParser contendo as configurações lidas do arquivo 'conf.cfg'.
    '''
    config = configparser.ConfigParser()  # Cria um objeto ConfigParser
    config.read('conf.cfg')  # Lê o arquivo de configuração 'conf.cfg'
    return config  # Retorna o objeto ConfigParser contendo as configurações lidas

# Função para atualizar configurações on-the-fly
def update_config() -> None:
    '''
    Função para atualizar as configurações do sistema dinamicamente.

    Parâmetros:
    Nenhum

    Retorna:
    None
        Não retorna nenhum valor. A função atualiza a variável global 'global_config' com as novas configurações.
    '''
    global global_config  # Declara a variável global 'global_config'
    while True:
        global_config = read_config()  # Lê e atualiza as configurações
        time.sleep(60)  # Pausa de 60 segundos antes de atualizar novamente

# Função para enviar alerta
def send_alert(message, equipamento) -> None:
    '''
    Função para enviar um alerta por e-mail com a mensagem e o equipamento especificado.

    Parâmetros:
    message : str
        A mensagem a ser enviada no alerta.
    equipamento : str
        O nome do equipamento relacionado à mensagem.

    Retorna:
    None
        Não retorna nenhum valor. A função envia um e-mail com o alerta.
    '''
    config = global_config  # Obtém as configurações globais
    smtp_server = config['email']['smtp_server']  # Servidor SMTP
    smtp_port = config['email']['smtp_port']  # Porta do servidor SMTP
    username = config['email']['username']  # Nome de usuário do e-mail
    password = config['email']['password']  # Senha do e-mail
    recipient = config['email']['recipient']  # Destinatário do e-mail

    msg = MIMEText(f'{message}\nEquipamento: {equipamento}')  # Cria a mensagem de e-mail
    msg['Subject'] = 'Alerta de Anomalia'  # Assunto do e-mail
    msg['From'] = username  # Remetente do e-mail
    msg['To'] = recipient  # Destinatário do e-mail

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Inicia o TLS para segurança
        server.login(username, password)  # Faz login no servidor de e-mail
        server.send_message(msg)  # Envia a mensagem de e-mail

# Nova função para treinar o modelo
def train_model(data, model_name, n_neighbors=20, contamination=0.1) -> None:
    '''
    Treina um modelo LOF com os dados fornecidos e salva o modelo em um arquivo pkl.

    Parâmetros:
    data : array-like
        Dados de treinamento.
    model_name : str
        Nome do arquivo para salvar o modelo.
    n_neighbors : int
        Número de vizinhos para o LOF.
    contamination : float
        Proporção esperada de outliers nos dados.

    Retorna:
    None
        Não retorna nenhum valor. O modelo treinado é salvo em um arquivo pkl.
    '''
    scaler = StandardScaler()  # Cria um objeto StandardScaler para normalizar os dados
    X_scaled = scaler.fit_transform(data)  # Normaliza os dados de treinamento

    lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination, novelty=True)  # Cria o modelo LOF
    lof.fit(X_scaled)  # Treina o modelo LOF

    joblib.dump((lof, scaler), f'{model_name}.pkl')  # Salva o modelo e o scaler em um arquivo pkl
    print(f"Modelo treinado e salvo como '{model_name}.pkl'")  # Mensagem de confirmação

# Função para iniciar servidor Flask para cada equipamento
def start_server(port, equipamento) -> None:
    '''
    Função para iniciar um servidor Flask para monitorar cada equipamento específico.

    Parâmetros:
    port : int
        A porta na qual o servidor Flask irá rodar.
    equipamento : str
        O nome do equipamento que está sendo monitorado.

    Retorna:
    None
        Não retorna nenhum valor. A função inicia um servidor Flask que escuta na porta especificada.
    '''
    app = Flask(__name__)  # Cria uma instância do Flask
    model, scaler = joblib.load(f'modelo_lof_{equipamento}.pkl')  # Carrega o modelo de machine learning e o scaler

    @app.route('/predict', methods=['POST'])
    def predict():
        data = request.json['data']  # Obtém os dados JSON da requisição
        data_scaled = scaler.transform(data)  # Normaliza os dados da requisição
        prediction = model.predict(data_scaled)  # Faz a predição com o modelo
        if -1 in prediction:  # Detecção de anomalia
            send_alert('Anomalia detectada no sistema! Verifique imediatamente.', equipamento)
        return jsonify({'prediction': prediction.tolist()})  # Retorna a predição em formato JSON

    app.run(debug=True, host='0.0.0.0', port=port)  # Inicia o servidor Flask na porta especificada

# Função principal para iniciar threads
def main() -> None:
    '''
    Função principal para iniciar threads que atualizam as configurações e iniciam servidores Flask para cada equipamento.

    Parâmetros:
    Nenhum

    Retorna:
    None
        Não retorna nenhum valor. A função inicia threads que lidam com a atualização das configurações e o monitoramento dos equipamentos.
    '''
    config_thread = threading.Thread(target=update_config)  # Cria uma thread para atualizar as configurações
    config_thread.start()  # Inicia a thread de atualização das configurações

    config = global_config  # Obtém as configurações globais
    ports = [config['server']['port_equipment1'], config['server']['port_equipment2']]  # Define as portas dos servidores Flask
    equipamentos = ['Equipamento1', 'Equipamento2']  # Define os nomes dos equipamentos

    server_threads = []  # Lista para armazenar as threads dos servidores Flask
    for port, equipamento in zip(ports, equipamentos):
        thread = threading.Thread(target=start_server, args=(port, equipamento))  # Cria uma thread para cada servidor Flask
        server_threads.append(thread)  # Adiciona a thread à lista de threads
        thread.start()  # Inicia a thread do servidor Flask

    for thread in server_threads:
        thread.join()  # Aguarda todas as threads dos servidores Flask terminarem

##########################
# VARIAVEIS
##########################
global_config = read_config()

# Inicialização da API
if __name__ == '__main__':
    main()
