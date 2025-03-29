import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class HarmonicOscillationPlotter(QWidget):
    def init(self):
        super().init()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Построение графика гармонического колебания')
        self.layout = QVBoxLayout()
        self.amplitude_input = QLineEdit(self)
        self.amplitude_input.setPlaceholderText('Введите амплитуду (м)')
        self.layout.addWidget(self.amplitude_input)
        self.frequency_input = QLineEdit(self)
        self.frequency_input.setPlaceholderText('Введите частоту (Гц)')
        self.layout.addWidget(self.frequency_input)
        self.phase_input = QLineEdit(self)
        self.phase_input.setPlaceholderText('Введите фазу (градусы)')
        self.layout.addWidget(self.phase_input)
        self.plot_button = QPushButton('Построить', self)
        self.plot_button.clicked.connect(self.plot_oscillation)
        self.layout.addWidget(self.plot_button)
        self.canvas = FigureCanvas(plt.figure())
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
    def plot_oscillation(self):
        A = float(self.amplitude_input.text())
        f = float(self.frequency_input.text())
        phi = float(self.phase_input.text())
        t = np.linspace(0, 10, 1000)
        x = A * np.cos(2 * np.pi * f * t + np.radians(phi))
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(t, x)
        ax.set_xlabel('Время (с)')
        ax.set_ylabel('Смещение (м)')
        ax.set_title(f'Гармоническое колебание: A={A} м, f={f} Гц, φ={phi}°')
        self.canvas.draw()

if __name__ == 'main':
    app = QApplication(sys.argv)
    ex = HarmonicOscillationPlotter()
    ex.show()
    sys.exit(app.exec_())