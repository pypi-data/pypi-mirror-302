from numpy import exp, round
# from scipy.stats import norm

from .utils import dOne, dTwo



def europeanCall(
    stockPrice,
    strikePrice,
    expiration,
    riskFreeRate,
    volatility,
    roundOutput=True
):
    dOneVar = dOne(
        stockPrice,
        strikePrice,
        expiration,
        riskFreeRate,
        volatility
    )
    tOne = stockPrice * dOneVar
    dTwoVar = dTwo(
        dOneVar,
        expiration,
        volatility
    )
    fvDiscount = exp(-riskFreeRate * expiration)
    tTwo = strikePrice * fvDiscount * dTwoVar

    output = (tOne - tTwo)

    return round(output, decimals=4) if roundOutput else output


def europeanPut(
    stockPrice,
    strikePrice,
    expiration,
    riskFreeRate,
    volatility,
    roundOutput=True
):
    dOneVar = dOne(
        stockPrice,
        strikePrice,
        expiration,
        riskFreeRate,
        volatility
    )
    tOne = stockPrice * (-1 * dOneVar)


    dTwoVar = dTwo(
        dOneVar,
        expiration,
        volatility
    )
    fvDiscount = exp(-riskFreeRate * expiration)
    tTwo = strikePrice * fvDiscount * (-1 * dTwoVar)

    output = (tTwo - tOne)

    return round(output, decimals=4) if roundOutput else output