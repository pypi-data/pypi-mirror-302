from PySide6.QtWidgets import QApplication, QComboBox, QVBoxLayout, QWidget


class CustomComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 设置为不可编辑
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)

        # 移除下拉箭头和边框
        self.setStyleSheet("""
            QComboBox {
                border: none; 
                padding: 0px; 
                min-width: 100px;  /* 根据需要设置宽度 */
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 0px;  /* 隐藏下拉箭头 */
                border: none; 
            }
        """)

        # 添加示例选项
        self.addItems(["选项 1", "选项 2", "选项 3"])


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        combo_box = CustomComboBox()

        layout.addWidget(combo_box)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
