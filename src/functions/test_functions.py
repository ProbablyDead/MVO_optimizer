import math
import sys
import inspect
import numpy
from .function import Function

inf = float(numpy.finfo(numpy.float64).max)


def prod(it):
    p = 1
    for n in it:
        p *= n
    return p


def Ufun(x, a, k, m):
    y = k * ((x - a) ** m) * (x > a) + k * ((-x - a) ** m) * (x < (-a))
    return y


def F_TCSD(x):
    d_w, D, n = x

    f_X = (n + 2) * D * d_w**2

    g1 = 1 - (D**3*n)/(71785*d_w**4)
    g2 = (4*D**2 - d_w*D)/(12566*(D*d_w**3-d_w**4)) + 1/(5108*d_w**2) - 1
    g3 = 1 - (140.45*d_w)/(D**2*n)
    g4 = (D + d_w)/1.5 - 1

    return f_X if g1 <= 0 and g2 <= 0 and g3 <= 0 and g4 <= 0 else inf


def F_AJM(x):
    x1, x2, x3 = x

    rho_a = 2.48e-6
    rho_w = 2.7e-6
    delta_cw = 1.5
    H_dw = 1150
    zeta = 1.6
    R_a_max = 2

    f_X = 1.0436*(10**(-6)) * zeta * \
        (rho_w/((delta_cw**2)*(H_dw**1.5)*(rho_a**0.5))) * \
        x1*(x3**3)

    g = 1 - (25.82/R_a_max)*((rho_a/H_dw)**0.5)*x2*x3
    return f_X if g >= 0 else -inf


def F_1(x):
    s = numpy.sum(x ** 2)
    return s


def F_2(x):
    o = sum(abs(x)) + prod(abs(x))
    return o


def F_3(x):
    dim = len(x) + 1
    o = 0
    for i in range(1, dim):
        o = o + (numpy.sum(x[0:i])) ** 2
    return o


def F_4(x):
    o = max(abs(x))
    return o


def F_5(x):
    dim = len(x)
    o = numpy.sum(
        100 * (x[1:dim] - (x[0: dim - 1] ** 2)) ** 2 + (x[0: dim - 1] - 1) ** 2
    )
    return o


def F_6(x):
    o = numpy.sum(abs((x + 0.5)) ** 2)
    return o


def F_7(x):
    dim = len(x)

    w = [i for i in range(len(x))]
    for i in range(0, dim):
        w[i] = i + 1
    o = numpy.sum(w * (x ** 4)) + numpy.random.uniform(0, 1)
    return o


def F_8(x):
    o = sum(-x * (numpy.sin(numpy.sqrt(abs(x)))))
    return o


def F_9(x):
    dim = len(x)
    o = numpy.sum(x ** 2 - 10 * numpy.cos(2 * math.pi * x)) + 10 * dim
    return o


def F_10(x):
    dim = len(x)
    o = (
        -20 * numpy.exp(-0.2 * numpy.sqrt(numpy.sum(x ** 2) / dim))
        - numpy.exp(numpy.sum(numpy.cos(2 * math.pi * x)) / dim)
        + 20
        + numpy.exp(1)
    )
    return o


def F_11(x):
    w = [i for i in range(len(x))]
    w = [i + 1 for i in w]
    o = numpy.sum(x ** 2) / 4000 - prod(numpy.cos(x / numpy.sqrt(w))) + 1
    return o


def F_12(x):
    dim = len(x)
    o = (math.pi / dim) * (
        10 * ((numpy.sin(math.pi * (1 + (x[0] + 1) / 4))) ** 2)
        + numpy.sum(
            (((x[: dim - 1] + 1) / 4) ** 2)
            * (1 + 10 * ((numpy.sin(math.pi * (1 + (x[1:] + 1) / 4)))) ** 2)
        )
        + ((x[dim - 1] + 1) / 4) ** 2
    ) + numpy.sum(Ufun(x, 10, 100, 4))
    return o


def F_13(x):
    if x.ndim == 1:
        x = x.reshape(1, -1)

    o = 0.1 * (
        (numpy.sin(3 * numpy.pi * x[:, 0])) ** 2
        + numpy.sum(
            (x[:, :-1] - 1) ** 2
            * (1 + (numpy.sin(3 * numpy.pi * x[:, 1:])) ** 2), axis=1
        )
        + ((x[:, -1] - 1) ** 2) *
        (1 + (numpy.sin(2 * numpy.pi * x[:, -1])) ** 2)
    ) + numpy.sum(Ufun(x, 5, 100, 4))
    return o


def F_14(x):
    aS = [
        [
            -32, -16, 0, 16, 32,
            -32, -16, 0, 16, 32,
            -32, -16, 0, 16, 32,
            -32, -16, 0, 16, 32,
            -32, -16, 0, 16, 32,
        ],
        [
            -32, -32, -32, -32, -32,
            -16, -16, -16, -16, -16,
            0, 0, 0, 0, 0,
            16, 16, 16, 16, 16,
            32, 32, 32, 32, 32,
        ],
    ]
    aS = numpy.asarray(aS)
    bS = numpy.zeros(25)
    v = numpy.matrix(x)
    for i in range(0, 25):
        H = v - aS[:, i]
        bS[i] = numpy.sum((numpy.power(H, 6)))
    w = [i for i in range(25)]
    for i in range(0, 24):
        w[i] = i + 1
    o = ((1.0 / 500) + numpy.sum(1.0 / (w + bS))) ** (-1)
    return o


def F_15(L):
    aK = [
        0.1957, 0.1947, 0.1735, 0.16, 0.0844, 0.0627,
        0.0456, 0.0342, 0.0323, 0.0235, 0.0246,
    ]
    bK = [0.25, 0.5, 1, 2, 4, 6, 8, 10, 12, 14, 16]
    aK = numpy.asarray(aK)
    bK = numpy.asarray(bK)
    bK = 1 / bK
    fit = numpy.sum(
        (aK - ((L[0] * (bK ** 2 + L[1] * bK)) /
         (bK ** 2 + L[2] * bK + L[3]))) ** 2
    )
    return fit


def F_16(L):
    o = (
        4 * (L[0] ** 2)
        - 2.1 * (L[0] ** 4)
        + (L[0] ** 6) / 3
        + L[0] * L[1]
        - 4 * (L[1] ** 2)
        + 4 * (L[1] ** 4)
    )
    return o


def F_17(L):
    o = (
        (L[1] - (L[0] ** 2) * 5.1 / (4 * (numpy.pi ** 2)) + 5 / numpy.pi * L[0] - 6)
        ** 2
        + 10 * (1 - 1 / (8 * numpy.pi)) * numpy.cos(L[0])
        + 10
    )
    return o


def F_18(L):
    o = (
        1
        + (L[0] + L[1] + 1) ** 2
        * (
            19
            - 14 * L[0]
            + 3 * (L[0] ** 2)
            - 14 * L[1]
            + 6 * L[0] * L[1]
            + 3 * L[1] ** 2
        )
    ) * (
        30
        + (2 * L[0] - 3 * L[1]) ** 2
        * (
            18
            - 32 * L[0]
            + 12 * (L[0] ** 2)
            + 48 * L[1]
            - 36 * L[0] * L[1]
            + 27 * (L[1] ** 2)
        )
    )
    return o


# map the inputs to the function blocks
def F_19(L):
    aH = [[3, 10, 30], [0.1, 10, 35], [3, 10, 30], [0.1, 10, 35]]
    aH = numpy.asarray(aH)
    cH = [1, 1.2, 3, 3.2]
    cH = numpy.asarray(cH)
    pH = [
        [0.3689, 0.117, 0.2673],
        [0.4699, 0.4387, 0.747],
        [0.1091, 0.8732, 0.5547],
        [0.03815, 0.5743, 0.8828],
    ]
    pH = numpy.asarray(pH)
    o = 0
    for i in range(0, 4):
        o = o - cH[i] * \
            numpy.exp(-(numpy.sum(aH[i, :] * ((L - pH[i, :]) ** 2))))
    return o


def F_20(L):
    aH = [
        [10, 3, 17, 3.5, 1.7, 8],
        [0.05, 10, 17, 0.1, 8, 14],
        [3, 3.5, 1.7, 10, 17, 8],
        [17, 8, 0.05, 10, 0.1, 14],
    ]
    aH = numpy.asarray(aH)
    cH = [1, 1.2, 3, 3.2]
    cH = numpy.asarray(cH)
    pH = [
        [0.1312, 0.1696, 0.5569, 0.0124, 0.8283, 0.5886],
        [0.2329, 0.4135, 0.8307, 0.3736, 0.1004, 0.9991],
        [0.2348, 0.1415, 0.3522, 0.2883, 0.3047, 0.6650],
        [0.4047, 0.8828, 0.8732, 0.5743, 0.1091, 0.0381],
    ]
    pH = numpy.asarray(pH)
    o = 0
    for i in range(0, 4):
        o = o - cH[i] * \
            numpy.exp(-(numpy.sum(aH[i, :] * ((L - pH[i, :]) ** 2))))
    return o


def F_21(L):
    aSH = [
        [4, 4, 4, 4],
        [1, 1, 1, 1],
        [8, 8, 8, 8],
        [6, 6, 6, 6],
        [3, 7, 3, 7],
        [2, 9, 2, 9],
        [5, 5, 3, 3],
        [8, 1, 8, 1],
        [6, 2, 6, 2],
        [7, 3.6, 7, 3.6],
    ]
    cSH = [0.1, 0.2, 0.2, 0.4, 0.4, 0.6, 0.3, 0.7, 0.5, 0.5]
    aSH = numpy.asarray(aSH)
    cSH = numpy.asarray(cSH)
    fit = 0
    for i in range(5):
        v = numpy.matrix(L - aSH[i, :])
        fit = fit - ((v) * (v.T) + cSH[i]) ** (-1)
    o = fit.item(0)
    return o


def F_22(L):
    aSH = [
        [4, 4, 4, 4],
        [1, 1, 1, 1],
        [8, 8, 8, 8],
        [6, 6, 6, 6],
        [3, 7, 3, 7],
        [2, 9, 2, 9],
        [5, 5, 3, 3],
        [8, 1, 8, 1],
        [6, 2, 6, 2],
        [7, 3.6, 7, 3.6],
    ]
    cSH = [0.1, 0.2, 0.2, 0.4, 0.4, 0.6, 0.3, 0.7, 0.5, 0.5]
    aSH = numpy.asarray(aSH)
    cSH = numpy.asarray(cSH)
    fit = 0
    for i in range(7):
        v = numpy.matrix(L - aSH[i, :])
        fit = fit - ((v) * (v.T) + cSH[i]) ** (-1)
    o = fit.item(0)
    return o


def F_23(L):
    aSH = [
        [4, 4, 4, 4],
        [1, 1, 1, 1],
        [8, 8, 8, 8],
        [6, 6, 6, 6],
        [3, 7, 3, 7],
        [2, 9, 2, 9],
        [5, 5, 3, 3],
        [8, 1, 8, 1],
        [6, 2, 6, 2],
        [7, 3.6, 7, 3.6],
    ]
    cSH = [0.1, 0.2, 0.2, 0.4, 0.4, 0.6, 0.3, 0.7, 0.5, 0.5]
    aSH = numpy.asarray(aSH)
    cSH = numpy.asarray(cSH)
    fit = 0
    for i in range(10):
        v = numpy.matrix(L - aSH[i, :])
        fit = fit - ((v) * (v.T) + cSH[i]) ** (-1)
    o = fit.item(0)
    return o


def getFunctionDetails(a):
    # [name, lb, ub, dim]
    param = {
        F_TCSD: ["Tension/compression spring design problem", 3,
                 [0.05, 0.25, 2.], [2., 1.3, 15.], r"$E = mc^2$"],
        F_AJM: ["Optimization of Abrasive Jet machining process parameters", 3,
                [0.0000167, 0.005, 15000], [0.0005, 0.075, 400000], r"$E = mc^2$"],
        F_1: ["F_1", 30, -100, 100, r"$E = mc^2$"],
        F_2: ["F_2", 30, -10, 10, r"$E = mc^2$"],
        F_3: ["F_3", 30, -100, 100, r"$E = mc^2$"],
        F_4: ["F_4", 30, -100, 100, r"$E = mc^2$"],
        F_5: ["F_5", 30, -30, 30, r"$E = mc^2$"],
        F_6: ["F_6", 30, -100, 100, r"$E = mc^2$"],
        F_7: ["F_7", 30, -1.28, 1.28, r"$E = mc^2$"],
        F_8: ["F_8", 30, -500, 500, r"$E = mc^2$"],
        F_9: ["F_9", 30, -5.12, 5.12, r"$E = mc^2$"],
        F_10: ["F_10", 30, -32, 32, r"$E = mc^2$"],
        F_11: ["F_11", 30, -600, 600, r"$E = mc^2$"],
        F_12: ["F_12", 30, -50, 50, r"$E = mc^2$"],
        F_13: ["F_13", 30, -50, 50, r"$E = mc^2$"],
        F_14: ["F_14", 2, -65.536, 65.536, r"$E = mc^2$"],
        F_15: ["F_15", 4, -5, 5, r"$E = mc^2$"],
        F_16: ["F_16", 2, -5, 5, r"$E = mc^2$"],
        F_17: ["F_17", 2, -5, 15, r"$E = mc^2$"],
        F_18: ["F_18", 2, -2, 2, r"$E = mc^2$"],
        F_19: ["F_19", 3, 0, 1, r"$E = mc^2$"],
        F_20: ["F_20", 6, 0, 1, r"$E = mc^2$"],
        F_21: ["F_21", 4, 0, 10, r"$E = mc^2$"],
        F_22: ["F_22", 4, 0, 10, r"$E = mc^2$"],
        F_23: ["F_23", 4, 0, 10, r"$E = mc^2$"],
    }
    return param.get(a, "nothing")


def get_functions():
    return [Function(f, *getFunctionDetails(f)) for _, f in inspect.getmembers(
        sys.modules[__name__],
        lambda m: hasattr(m, "__name__") and m.__name__.startswith("F_")
    )]
