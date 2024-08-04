import numpy as np


def monte_carlo_simulation(data, T=1.0, N=10000):
    mu = data['Return'].mean()
    sigma = data['Return'].std()
    S0 = data['Adj Close'][-1]
    dt = 1 / 252
    steps = int(T / dt)

    np.random.seed(42)
    Z = np.random.standard_normal((N, steps))
    ST = np.zeros((N, steps))
    ST[:, 0] = S0

    for t in range(1, steps):
        ST[:, t] = ST[:, t - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z[:, t - 1])

    return ST, mu, sigma
