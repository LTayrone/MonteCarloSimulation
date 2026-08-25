import numpy as np
import pandas as pd


def as_series(values):
    if isinstance(values, pd.DataFrame):
        return values.iloc[:, 0]

    return values


def monte_carlo_simulation(data, T=1.0, N=10000):
    returns = as_series(data["Return"]).dropna()
    prices = as_series(data["Price"]).dropna()

    if returns.empty or prices.empty:
        raise ValueError("Dados insuficientes para executar a simulação.")

    mu = returns.mean()
    sigma = returns.std()
    S0 = prices.iloc[-1]
    dt = 1 / 252
    steps = int(T / dt)

    np.random.seed(42)
    Z = np.random.standard_normal((N, steps))
    ST = np.zeros((N, steps))
    ST[:, 0] = S0

    for t in range(1, steps):
        ST[:, t] = ST[:, t - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z[:, t - 1])

    return ST, mu, sigma
