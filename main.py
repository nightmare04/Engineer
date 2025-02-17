from PyQt6 import QtWidgets

from database.models import create_tables
from windows import MainWindow


if __name__ == '__main__':
    import sys
    # sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon('ui/main.ico'))
    main = MainWindow()
    main.show()

    sys.exit(app.exec())
