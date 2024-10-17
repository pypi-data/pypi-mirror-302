import sys

from mango_ui import *
from mango_ui.init import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("多选下拉框示例")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout(self)

        options = ["选项1", "选项2", "选项3", "选项4"]
        self.combo = MangoComboBoxMany(placeholder="选择项目", data=options, value="选项2")
        self.layout.addWidget(self.combo)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
