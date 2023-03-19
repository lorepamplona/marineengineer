import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


dados = pd.read_csv('./data.csv')
plt.plot(dados['Velocidade'], dados['Consumo Combustível'])
plt.xlabel('Velocidade (nós)')
plt.ylabel('Consumo de combustível (kg/h)')
plt.title('Consumo de combustível vs. Velocidade')
plt.show()

sns.scatterplot(x='Deslocamento', y='Altura de onda', hue='Velocidade', data=dados)
plt.xlabel('Deslocamento (t)')
plt.ylabel('Altura de onda (m)')
plt.title('Altura de onda vs. deslocamento por velocidade')
plt.show()

#Results

media_velocidade = dados['Velocidade'].mean()
media_consumo = dados['Consumo Combustível'].mean()
max_altura = dados['Altura de onda'].max()
relatorio = f"Resultados do teste de desempenho:\nMédia de velocidade: {media_velocidade}\nMédia de consumo de combustível: {media_consumo}\nAltura máxima de onda: {max_altura}"
print(relatorio)
