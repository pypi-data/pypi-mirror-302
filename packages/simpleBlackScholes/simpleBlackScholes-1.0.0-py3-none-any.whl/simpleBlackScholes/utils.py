import numpy as np


def dOne(
        stockPrice,
        strikePrice,
        expiration,
        riskFreeRate,
        volatility
):
    ratio = np.log((stockPrice/strikePrice))
    tTwo = expiration * (riskFreeRate + (np.square(volatility) / 2))
    return (ratio + tTwo) / (volatility * np.sqrt(expiration))

def dTwo(dOneVar, expiration, volatility):
    return dOneVar - (volatility * np.sqrt(expiration))