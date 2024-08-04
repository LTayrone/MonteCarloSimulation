import streamlit as st
import numpy as np
import pandas as pd
from data.downloader import download_data
from simulation.monte_carlo import monte_carlo_simulation
from visualization.plots import plot_simulated_paths, plot_histogram

st.title('Simulação Monte Carlo de Preços de Ações')
st.subheader("Lucas Tayrone Moreira Ribeiro - Universidade Federal de Ouro Preto")

ticker = st.text_input('Digite o código da ação (ex: NVDA ou BEEF3.SA):')
start_date = st.date_input('Data de início', value=pd.to_datetime('2022-01-01'))
end_date = st.date_input('Data de término', value=pd.to_datetime('2024-01-01'))

if ticker:
    data = download_data(ticker, start_date, end_date)
    data['Return'] = data['Adj Close'].pct_change()

    ST, mu, sigma = monte_carlo_simulation(data)

    st.write(f"Simulação para {ticker} de {start_date} a {end_date}")
    st.write(f"Retorno médio diário: {mu:.4f}")
    st.write(f"Volatilidade diária: {sigma:.4f}")
    st.write(f"O preço médio final estimado é: {np.mean(ST[:, -1]):.2f}")
    st.write(f"O desvio padrão dos preços finais é: {np.std(ST[:, -1]):.2f}")

    st.pyplot(plot_simulated_paths(ST, ticker))
    st.pyplot(plot_histogram(ST))
