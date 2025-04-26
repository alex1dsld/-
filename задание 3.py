import numpy as np
import matplotlib.pyplot as plt

subjects = ["Математический анализ", "Физика", "Инженерная графика", "Химия"]
months = ["Сент", "Окт", "Нояб", "Дек", "Янв", "Фев"]

grades = {
    "Математический анализ": [4, 5, 5, 3, 4, 4],
    "Физика": [4, 5, 4, 5, 5, 5],
    "Инженерная графика": [4, 3, 3, 5, 4, 4],
    "Химия": [4, 4, 3, 5, 4, 4]
}

plt.figure(figsize=(10, 6))
for subject, marks in grades.items():
    plt.plot(months, marks, marker='o', label=subject)

plt.xlabel("Месяцы")
plt.ylabel("Оценки")
plt.title("Графики оценок за полугодие")
plt.legend()
plt.grid(True)
plt.ylim(2, 5.5)
plt.show()
