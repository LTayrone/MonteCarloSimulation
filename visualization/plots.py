import matplotlib.pyplot as plt
import numpy as np

def plot_simulated_paths(ST, ticker):
    fig, ax = plt.subplots()
    ax.plot(ST.T, lw=1)
    ax.set_title(f'Simulação de Preços de Ações {ticker}')
    ax.set_xlabel('Dias de Negociação')
    ax.set_ylabel('Preço')
    return fig

def plot_histogram(ST):
    fig, ax = plt.subplots(figsize=(10, 6))
    counts, bins, _ = ax.hist(ST[:, -1], bins=50, alpha=0.75, color='blue', density=True)
    cumulative = np.cumsum(counts)
    ax.plot(bins[1:], cumulative/cumulative[-1], color='red', label='Probabilidade Acumulada')
    ax.set_title('Histograma dos Preços Finais Simulados com Curva de Probabilidade Acumulada')
    ax.set_xlabel('Preço Final')
    ax.set_ylabel('Frequência')
    ax.grid(True)
    ax.legend()
    return fig
