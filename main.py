from PyQt6 import QtWidgets
from windows.mainw import MainWindow
from database.models import create_tables


if __name__ == '__main__':
    import sys
    # sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    # app.setWindowIcon(QtGui.QIcon('ui/main.ico'))
    create_tables()
    main = MainWindow()
    main.resize(1000, 700)
    main.show()

    sys.exit(app.exec())
