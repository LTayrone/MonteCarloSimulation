import streamlit as st
import numpy as np
import pandas as pd
from data.downloader import download_data, normalize_columns
from simulation.monte_carlo import monte_carlo_simulation
from visualization.plots import plot_simulated_paths, plot_histogram


def select_price_column(data):
    if "Adj Close" in data.columns:
        return data["Adj Close"], "Adj Close"

    if "Close" in data.columns:
        return data["Close"], "Close"

    return None, None


st.title("Simulação Monte Carlo de Preços de Ações")

st.write("[Para pesquisar o código das ações acesse](https://finance.yahoo.com/quote/VALE3.SA/)")
st.write("Lucas Tayrone Moreira Ribeiro")
st.write("[LinkedIn](https://www.linkedin.com/in/lucastayrone/)")
st.write(f"Atualizado em {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}")

ticker = st.text_input("Digite o código da ação (ex: NVDA ou VALE3.SA):")
start_date = st.date_input("Data de início", value=pd.to_datetime("2022-01-01"))
end_date = st.date_input("Data de término", value=pd.to_datetime("2024-01-01"))

if ticker:
    ticker = ticker.strip().upper()

    if start_date >= end_date:
        st.error("A data de início deve ser anterior à data de término.")
        st.stop()

    data = normalize_columns(download_data(ticker, start_date, end_date))

    if data.empty:
        st.error(
            "Nenhum dado foi encontrado para esse código e período. "
            "Para ações brasileiras, use o formato com número e sufixo .SA, por exemplo: VALE3.SA."
        )
        st.stop()

    price, price_column = select_price_column(data)

    if price is None:
        st.error("Nenhuma coluna de preço foi encontrada nos dados retornados pelo Yahoo Finance.")
        st.stop()

    if isinstance(price, pd.DataFrame):
        price = price.iloc[:, 0]

    data["Price"] = price
    data["Return"] = data["Price"].pct_change()

    if data["Return"].dropna().empty:
        st.error("Não há dados suficientes para calcular os retornos.")
        st.stop()

    if price_column == "Close":
        st.info("A coluna 'Adj Close' não veio no retorno do Yahoo Finance. Usando 'Close' no cálculo.")

    ST, mu, sigma = monte_carlo_simulation(data)

    st.write(f"Simulação para {ticker} de {start_date} a {end_date}")
    st.write(f"Retorno médio diário: {mu:.4f}")
    st.write(f"Volatilidade diária: {sigma:.4f}")
    st.write(f"O preço médio final estimado é: {np.mean(ST[:, -1]):.2f}")
    st.write(f"O desvio padrão dos preços finais é: {np.std(ST[:, -1]):.2f}")

    st.pyplot(plot_simulated_paths(ST, ticker))
    st.pyplot(plot_histogram(ST))
