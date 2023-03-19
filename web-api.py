import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request


dados_embarcacao = pd.read_csv('./Gilberto.csv')

app = Flask(__name__)
@app.route('/dados')

def obter_dados():
    colunas = request.args.get('colunas').split(',')
    dados_filtrados = dados_embarcacao[colunas]
    return jsonify(dados_filtrados.to_dict())

def analisar_dados():
    velocidade_hora = dados_embarcacao['velocidade'].resample('1H').mean()
    consumo_dia = dados_embarcacao['consumo_combustivel'].resample('1D').sum()

    plt.plot(velocidade_hora.index, velocidade_hora.values)
    plt.title('Velocidade da embarcação por hora')
    plt.xlabel('Hora')
    plt.ylabel('Velocidade')
    plt.show()

    plt.bar(consumo_dia.index, consumo_dia.values)
    plt.title('Consumo de combustível da embarcação por dia')
    plt.xlabel('Dia')
    plt.ylabel('Consumo de combustível')
    plt.show()

if __name__ == '__main__':
    analisar_dados()
    app.run()