# Documentação Completa do Anomaly API

## Índice

1. [Introdução](#1-introdução)
   1.1. [Visão Geral](#11-visão-geral)
   1.2. [Funcionalidades](#12-funcionalidades)

2. [Requisitos do Sistema](#2-requisitos-do-sistema)
   2.1. [Hardware](#21-hardware)
   2.2. [Software](#22-software)

3. [Instalação](#3-instalação)
   3.1. [Preparação do Ambiente](#31-preparação-do-ambiente)
   3.2. [Download do Código](#32-download-do-código)
   3.3. [Instalação de Dependências](#33-instalação-de-dependências)

4. [Configuração](#4-configuração)
   4.1. [Arquivo de Configuração](#41-arquivo-de-configuração)
   4.2. [Configuração de E-mail](#42-configuração-de-e-mail)
   4.3. [Configuração de Portas](#43-configuração-de-portas)

5. [Execução](#5-execução)
   5.1. [Inicialização do Sistema](#51-inicialização-do-sistema)
   5.2. [Verificação de Logs](#52-verificação-de-logs)

6. [Uso da API](#6-uso-da-api)
   6.1. [Treinamento do Modelo](#61-treinamento-do-modelo)
      6.1.1. [Preparação dos Dados](#611-preparação-dos-dados)
      6.1.2. [Envio de Dados para Treinamento](#612-envio-de-dados-para-treinamento)
      6.1.3. [Parâmetros de Treinamento](#613-parâmetros-de-treinamento)
   6.2. [Detecção de Anomalias](#62-detecção-de-anomalias)
      6.2.1. [Formato dos Dados](#621-formato-dos-dados)
      6.2.2. [Envio de Dados para Análise](#622-envio-de-dados-para-análise)
      6.2.3. [Interpretação dos Resultados](#623-interpretação-dos-resultados)

7. [Monitoramento e Alertas](#7-monitoramento-e-alertas)
   7.1. [Sistema de Alertas por E-mail](#71-sistema-de-alertas-por-e-mail)
   7.2. [Personalização de Alertas](#72-personalização-de-alertas)

8. [Manutenção](#8-manutenção)
   8.1. [Atualização do Modelo](#81-atualização-do-modelo)
   8.2. [Backup de Dados](#82-backup-de-dados)
   8.3. [Monitoramento de Desempenho](#83-monitoramento-de-desempenho)

9. [Resolução de Problemas](#9-resolução-de-problemas)
   9.1. [Problemas Comuns](#91-problemas-comuns)
   9.2. [Logs de Erro](#92-logs-de-erro)
   9.3. [Suporte Técnico](#93-suporte-técnico)

10. [Apêndices](#10-apêndices)
    10.1. [Glossário](#101-glossário)
    10.2. [Referências](#102-referências)

## 1. Introdução

### 1.1. Visão Geral

O Anomaly API é um sistema de detecção de anomalias baseado em aprendizado de máquina, projetado para monitorar e identificar comportamentos anormais em equipamentos industriais. Utilizando o algoritmo Local Outlier Factor (LOF), o sistema é capaz de aprender padrões normais de operação e detectar desvios significativos que podem indicar falhas ou problemas potenciais.

### 1.2. Funcionalidades

- Treinamento de modelos de detecção de anomalias via API HTTP
- Detecção de anomalias em tempo real
- Sistema de alertas por e-mail para notificação imediata de anomalias
- Suporte a múltiplos equipamentos
- Configuração flexível e atualizações dinâmicas

## 2. Requisitos do Sistema

### 2.1. Hardware

- Processador: Intel Core i5 ou equivalente (mínimo)
- Memória RAM: 8GB (mínimo), 16GB (recomendado)
- Espaço em disco: 10GB de espaço livre

### 2.2. Software

- Sistema Operacional: Linux (Qualquer distro baseada em Debian ou RedHat)
- Python 3.7 ou superior
- Bibliotecas Python: Flask, NumPy, Pandas, Scikit-learn, Joblib

## 3. Instalação

### 3.1. Preparação do Ambiente

1. Instale o Python 3.7 ou superior em seu sistema.
2. Verifique a instalação executando:
   ```
   python --version
   ```

### 3.2. Download do Código

1. Clone o repositório ou baixe o arquivo ZIP do projeto.
2. Descompacte o arquivo (se necessário) e navegue até o diretório do projeto.

### 3.3. Instalação de Dependências

1. Abra um terminal no diretório do projeto.
2. Execute o seguinte comando para instalar as dependências:
   ```
   pip install -r requirements.txt
   ```

## 4. Configuração

### 4.1. Arquivo de Configuração

1. Localize o arquivo `conf.cfg` no diretório do projeto.
2. Abra o arquivo com um editor de texto.

### 4.2. Configuração de E-mail

1. No arquivo `conf.cfg`, localize a seção [email].
2. Preencha os seguintes campos:
   ```
   smtp_server = seu_servidor_smtp.com
   smtp_port = 587
   username = seu_email@exemplo.com
   password = sua_senha
   recipient = destinatario@exemplo.com
   ```

### 4.3. Configuração de Portas

1. No arquivo `conf.cfg`, localize a seção [server].
2. Configure as portas para cada equipamento:
   ```
   port_equipment1 = 5001
   port_equipment2 = 5002
   ```

## 5. Execução

### 5.1. Inicialização do Sistema

1. Abra um terminal no diretório do projeto.
2. Execute o seguinte comando:
   ```
   python anomaly_api.py >> log.txt
   ```
3. O sistema iniciará e você verá mensagens de log indicando que os servidores estão rodando.

### 5.2. Verificação de Logs

1. Observe o terminal para mensagens de inicialização e logs em tempo real.
2. Verifique se não há erros durante a inicialização.
3. Valide as informações no arquivo log.txt executado pelo comando 2 no item 5.1

## 6. Uso da API

### 6.1. Treinamento do Modelo

#### 6.1.1. Preparação dos Dados

1. Prepare um arquivo CSV com os dados de treinamento.
2. Certifique-se de que cada linha representa uma observação e cada coluna uma característica do equipamento.
3. Não inclua cabeçalhos no arquivo CSV.

#### 6.1.2. Envio de Dados para Treinamento

1. Use uma ferramenta como cURL ou um script Python para enviar o arquivo CSV.
2. Exemplo com cURL:
   ```
   curl -X POST -F "file=@seus_dados.csv" -F "n_neighbors=20" -F "contamination=0.1" http://localhost:5001/train
   ```
3. Exemplo com Python requests:
   ```python
   import requests

   url = 'http://localhost:5001/train'
   files = {'file': open('seus_dados.csv', 'rb')}
   data = {'n_neighbors': '20', 'contamination': '0.1'}

   response = requests.post(url, files=files, data=data)
   print(response.json())
   ```

#### 6.1.3. Parâmetros de Treinamento

- `n_neighbors`: Número de vizinhos para o algoritmo LOF (padrão: 20)
- `contamination`: Proporção esperada de outliers nos dados (padrão: 0.1)

### 6.2. Detecção de Anomalias

#### 6.2.1. Formato dos Dados

1. Prepare os dados em formato JSON.
2. Exemplo de estrutura:
   ```json
   {
     "data": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
   }
   ```

#### 6.2.2. Envio de Dados para Análise

1. Envie uma requisição POST para o endpoint `/predict`.
2. Exemplo com cURL:
   ```
   curl -X POST -H "Content-Type: application/json" -d '{"data": [[1.0, 2.0, 3.0]]}' http://localhost:5001/predict
   ```

#### 6.2.3. Interpretação dos Resultados

- A API retornará um JSON com as previsões.
- Valores 1 indicam comportamento normal.
- Valores -1 indicam anomalias.

## 7. Monitoramento e Alertas

### 7.1. Sistema de Alertas por E-mail

- O sistema enviará automaticamente um e-mail quando uma anomalia for detectada.
- Verifique as configurações de e-mail no arquivo `conf.cfg`.

### 7.2. Personalização de Alertas

- Para personalizar o conteúdo dos alertas, modifique a função `send_alert` no arquivo `anomaly_api.py`.

## 8. Manutenção

### 8.1. Atualização do Modelo

- Realize o treinamento periodicamente com novos dados para manter o modelo atualizado.
- Recomenda-se retreinar o modelo mensalmente ou quando houver mudanças significativas no equipamento.

### 8.2. Backup de Dados

- Faça backups regulares dos arquivos de modelo (.pkl) e do arquivo de configuração.

### 8.3. Monitoramento de Desempenho

- Monitore o uso de CPU e memória do sistema.
- Verifique os logs regularmente para identificar possíveis problemas.

## 9. Resolução de Problemas

### 9.1. Problemas Comuns

1. Erro de conexão SMTP: Verifique as configurações de e-mail no arquivo `conf.cfg`.
2. Modelo não encontrado: Certifique-se de que o arquivo de modelo (.pkl) está no diretório correto.
3. Erro ao iniciar o servidor: Verifique se as portas especificadas estão disponíveis.

### 9.2. Logs de Erro

- Consulte o terminal onde o sistema está sendo executado para ver logs detalhados.
- Erros específicos serão exibidos no console.

### 9.3. Suporte Técnico

- Para suporte adicional, entre em contato com gabriel.francisco@ibm.com.

## 10. Apêndices

### 10.1. Glossário

- LOF: Local Outlier Factor
- Anomalia: Padrão de dados que desvia significativamente do comportamento normal esperado
- API: Application Programming Interface

### 10.2. Referências

- Documentação do Scikit-learn: https://scikit-learn.org/stable/
- Documentação do Flask: https://flask.palletsprojects.com/
- Documentação do Python: https://docs.python.org/3/

