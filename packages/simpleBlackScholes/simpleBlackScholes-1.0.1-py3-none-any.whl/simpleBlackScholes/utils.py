from numpy import log, square, sqrt


def dOne(
        stockPrice,
        strikePrice,
        expiration,
        riskFreeRate,
        volatility
):
    ratio = log((stockPrice/strikePrice))
    tTwo = expiration * (riskFreeRate + (square(volatility) / 2))
    return (ratio + tTwo) / (volatility * sqrt(expiration))

def dTwo(dOneVar, expiration, volatility):
    return dOneVar - (volatility * sqrt(expiration))