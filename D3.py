import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class NewtonCooling(QWidget):
    def init(self):
        super().init()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Закон охлаждения Ньютона')
        self.layout = QVBoxLayout()
        self.T0_input = QLineEdit(self)
        self.T0_input.setPlaceholderText('Введите начальную температуру объекта (°C)')
        self.layout.addWidget(self.T0_input)
        self.Tenv_input = QLineEdit(self)
        self.Tenv_input.setPlaceholderText('Введите температуру окружающей среды (°C)')
        self.layout.addWidget(self.Tenv_input)
        self.k_input = QLineEdit(self)
        self.k_input.setPlaceholderText('Введите коэффициент теплообмена (1/с)')
        self.layout.addWidget(self.k_input)
        self.plot_button = QPushButton('Построить', self)
        self.plot_button.clicked.connect(self.plot_cooling)
        self.layout.addWidget(self.plot_button)
        self.canvas = FigureCanvas(plt.figure())
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
    def plot_cooling(self):
        T0 = float(self.T0_input.text())
        Tenv = float(self.Tenv_input.text())
        k = float(self.k_input.text())
        t = np.linspace(0, 10, 1000)
        T = Tenv + (T0 - Tenv) * np.exp(-k * t)
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(t, T)
        ax.set_xlabel('Время (с)')
        ax.set_ylabel('Температура тела (°C)')
        ax.set_title(f'Охлаждение: T0={T0}°C, Tenv={Tenv}°C, k={k} 1/с')
        self.canvas.draw()

if __name__ == 'main':
    app = QApplication(sys.argv)
    ex = NewtonCooling()
    ex.show()
    sys.exit(app.exec_())