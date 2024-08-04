import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Baixando dados históricos da Ação
ticker = 'NVDA'  # Código para Ação no Yahoo Finance
data = yf.download(ticker, start='2022-01-01', end='2024-01-01')

# Calculando retornos diários
data['Return'] = data['Adj Close'].pct_change() # A função pct_change() calcula a variação percentual entre o preço de fechamento ajustado de um dia e o preço do dia anterior.
mu = data['Return'].mean()  # Retorno médio diário
sigma = data['Return'].std()  # Volatilidade diária, utilizando o desvio padrão dos retornos diarios

# Parâmetros para a Simulação de Monte Carlo
S0 = data['Adj Close'][-1]  # Último preço de fechamento ajustado
T = 1.0  # X anos
dt = 1/252  # Passo de tempo (1 dia de negociação)
N = 10000  # Número de simulações
steps = int(T / dt)  # Número de passos

# Simulação de Monte Carlo
np.random.seed(42)  # Para reprodutibilidade
Z = np.random.standard_normal((N, steps))  # Números aleatórios da distribuição normal padrão
ST = np.zeros((N, steps))
ST[:, 0] = S0

# Simulação de preços
for t in range(1, steps):
    ST[:, t] = ST[:, t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[:, t-1])

# Plot de alguns caminhos simulados
plt.plot(ST.T, lw=1)
plt.title(f'Simulação de Preços de Ações {ticker}')
plt.xlabel('Dias de Negociação')
plt.ylabel('Preço')
plt.show()

# Cálculo do preço médio final e desvio padrão
mean_price = np.mean(ST[:, -1])
std_dev = np.std(ST[:, -1])

print(f"O preço médio final estimado é: {mean_price:.2f}")
print(f"O desvio padrão dos preços finais é: {std_dev:.2f}")

# Plot do histograma dos preços finais com curva de probabilidade acumulada
plt.figure(figsize=(10, 6))
counts, bins, patches = plt.hist(ST[:, -1], bins=50, alpha=0.75, color='blue', density=True)
cumulative = np.cumsum(counts)
plt.plot(bins[1:], cumulative/cumulative[-1], color='red', label='Probabilidade Acumulada')

plt.title('Histograma dos Preços Finais Simulados com Curva de Probabilidade Acumulada')
plt.xlabel('Preço Final')
plt.ylabel('Frequência')
plt.grid(True)
plt.legend()
plt.show()