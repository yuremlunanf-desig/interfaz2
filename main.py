import sys
from pathlib import Path

sys.path.insert(0, r"C:\qt\pyside6")

from PySide6.QtCore import QFile
from PySide6.QtWidgets import QApplication, QMessageBox, QPushButton, QTextEdit
from PySide6.QtUiTools import QUiLoader


def main():
    app = QApplication(sys.argv)

    ui_file = QFile(str(Path(__file__).with_name("interfaz.ui")))
    if not ui_file.open(QFile.OpenModeFlag.ReadOnly):
        raise RuntimeError(f"No se pudo abrir el formulario: {ui_file.fileName()}")

    window = QUiLoader().load(ui_file)
    ui_file.close()
    if window is None:
        raise RuntimeError(f"No se pudo cargar el formulario: {ui_file.fileName()}")

    num1_field = window.findChild(QTextEdit, "textNum1")
    num2_field = window.findChild(QTextEdit, "textNum2")
    suma_button = window.findChild(QPushButton, "pushSuma")
    resta_button = window.findChild(QPushButton, "pushResta")
    multiplicacion_button = window.findChild(QPushButton, "pushMultipliacion")
    division_button = window.findChild(QPushButton, "pushDivision")
    if (
        num1_field is None
        or num2_field is None
        or suma_button is None
        or resta_button is None
        or multiplicacion_button is None
        or division_button is None
    ):
        raise RuntimeError("No se encontraron los campos o botones esperados en interfaz.ui")

    def calcular(operacion):
        try:
            num1 = float(num1_field.toPlainText().strip())
            num2 = float(num2_field.toPlainText().strip())
        except ValueError:
            QMessageBox.warning(
                window,
                "Dato inválido",
                "Escribe un número válido en ambos campos.",
            )
            return

        if operacion == "división" and num2 == 0:
            QMessageBox.warning(window, "Operación inválida", "No se puede dividir entre cero.")
            return

        operaciones = {
            "suma": lambda: num1 + num2,
            "resta": lambda: num1 - num2,
            "multiplicación": lambda: num1 * num2,
            "división": lambda: num1 / num2,
        }
        QMessageBox.information(
            window,
            "Resultado",
            f"La {operacion} es: {operaciones[operacion]()}",
        )

    suma_button.clicked.connect(lambda: calcular("suma"))
    resta_button.clicked.connect(lambda: calcular("resta"))
    multiplicacion_button.clicked.connect(lambda: calcular("multiplicación"))
    division_button.clicked.connect(lambda: calcular("división"))

    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
