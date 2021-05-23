import sys
from PyQt5.QtWidgets import QApplication

# 窗口实例
import main_window


def main():
    app = QApplication(sys.argv)
    ui_main_window_ = main_window.MainWindow()  # 实例化
    ui_main_window_.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
