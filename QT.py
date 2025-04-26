import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super(MatplotlibCanvas, self).__init__(fig)

class FunctionPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("График функции")
        self._main = QWidget()
        self.setCentralWidget(self._main)
        layout = QVBoxLayout(self._main)

        func_layout = QHBoxLayout()
        func_layout.addWidget(QLabel("f(x) ="))
        self.func_input = QLineEdit()
        func_layout.addWidget(self.func_input)
        layout.addLayout(func_layout)

        range_layout = QHBoxLayout()
        range_layout.addWidget(QLabel("X_min:"))
        self.xmin_input = QLineEdit()
        range_layout.addWidget(self.xmin_input)
        range_layout.addWidget(QLabel("X_max:"))
        self.xmax_input = QLineEdit()
        range_layout.addWidget(self.xmax_input)
        layout.addLayout(range_layout)

        self.plot_button = QPushButton("Построить график")
        self.plot_button.clicked.connect(self.plot)
        layout.addWidget(self.plot_button)

        self.canvas = MatplotlibCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.canvas)

    def plot(self):
        func_text = self.func_input.text().strip()
        xmin_text = self.xmin_input.text().strip()
        xmax_text = self.xmax_input.text().strip()

        try:
            xmin = float(xmin_text)
            xmax = float(xmax_text)
            if xmin >= xmax:
                raise ValueError("X_min должен быть меньше X_max")
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка диапазона", str(e))
            return

        try:
            x = np.linspace(xmin, xmax, 400)
            allowed_names = {k: getattr(np, k) for k in dir(np) if not k.startswith("__")}
            allowed_names['x'] = x
            y = eval(func_text, {"__builtins__": {}}, allowed_names)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка функции", f"Невозможно вычислить функцию:\n{e}")
            return

        self.canvas.ax.clear()
        self.canvas.ax.plot(x, y)
        self.canvas.ax.set_title(f"f(x) = {func_text}")
        self.canvas.ax.grid(True)
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FunctionPlotter()
    window.show()
    sys.exit(app.exec_())