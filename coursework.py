import numpy as np

# Инициализация параметров модели
params = {
    "αE": 0.999,  # Параметр заражения между бессимптомной и восприимчивой группами населения
    "αI": 0.999,  # Параметр заражения между инфицированным и восприимчивым населением
    "κ": 0.042,   # Частота появления симптомов у бессимптомных инфицированных
    "ρ": 0.952,   # Скорость восстановления выявленных бессимптомных случаев
    "β": 0.999,   # Скорость выздоровления инфицированных случаев
    "μ": 0.0188,  # Смертность в результате COVID-19
    "cisol": 0,   # Коэффициент влияния индекса самоизоляции на заражаемость
    "E0": 99,     # Начальное количество бессимптомных инфицированных
    "R0": 24,     # Начальное количество вылеченных индивидуумов
    "S0": 2798047,  # Начальное количество восприимчивых индивидуумов
    "I0": 0,      # Начальное количество инфицированных с симптомами
    "D0": 0,      # Начальное количество умерших
    "N": 2798047 + 99 + 24,  # Общая популяция
    "γ": 0,       # Скорость повторного заражения (устойчивый иммунитет)
}

# Временной интервал
t_start = 0  # Начальное время
t_end = 90   # Конечное время
h = 1        # Шаг по времени

# Создание массивов для хранения решений
t = np.arange(t_start, t_end + h, h, dtype=float)  # Массив времени
S = np.zeros_like(t)  # Массив для восприимчивых
E = np.zeros_like(t)  # Массив для бессимптомных инфицированных
I = np.zeros_like(t)  # Массив для инфицированных с симптомами
R = np.zeros_like(t)  # Массив для вылеченных
D = np.zeros_like(t)  # Массив для умерших

# Начальные условия
S[0] = params["S0"]
E[0] = params["E0"]
I[0] = params["I0"]
R[0] = params["R0"]
D[0] = params["D0"]

# Метод Эйлера
for i in range(len(t) - 1):
    # Функция ограничения передвижения
    c = 1 + params["cisol"] * (1 - 2 / 5 * 0)

    # Вычисление производных на текущем шаге
    dS = -c * (params["αI"] * S[i] * I[i] / params["N"] + params["αE"] * S[i] * E[i] / params["N"]) + params["γ"] * R[i]
    dE = c * (params["αI"] * S[i] * I[i] / params["N"] + params["αE"] * S[i] * E[i] / params["N"]) - (params["κ"] + params["ρ"]) * E[i]
    dI = params["κ"] * E[i] - params["β"] * I[i] - params["μ"] * I[i]
    dR = params["β"] * I[i] + params["ρ"] * E[i] - params["γ"] * R[i]
    dD = params["μ"] * I[i]

    # Обновление решений на следующем шаге
    S[i + 1] = S[i] + h * dS
    E[i + 1] = E[i] + h * dE
    I[i + 1] = I[i] + h * dI
    R[i + 1] = R[i] + h * dR
    D[i + 1] = D[i] + h * dD

# Вывод решения
print("Решение системы уравнений модели SEIR-D для Новосибирской области:")
print("t\tS\tE\tI\tR\tD")
for i in range(len(t)):
    print(f"{t[i]}\t{S[i]:.2f}\t{E[i]:.2f}\t{I[i]:.2f}\t{R[i]:.2f}\t{D[i]:.2f}")
