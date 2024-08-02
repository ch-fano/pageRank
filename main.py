

from index import Index
from model import IRModel

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QWidget, QTableWidget, \
    QTableWidgetItem


class SearchApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(SearchApp, self).__init__(parent)
        self.setWindowTitle("Ricerca")
        self.setGeometry(100, 100, 800, 600)

        # Main widget
        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Search Input
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Inserisci il termine di ricerca")
        self.layout.addWidget(self.search_input)

        # Limit Input
        self.limit_input = QSpinBox(self)
        self.limit_input.setValue(10000)
        self.limit_input.setMaximum(10000)
        self.layout.addWidget(self.limit_input)

        # Search Button
        self.search_button = QPushButton("Cerca", self)
        self.search_button.clicked.connect(self.perform_search)
        self.layout.addWidget(self.search_button)

        # Table for results
        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)

    def perform_search(self):
        query = self.search_input.text()
        limit = self.limit_input.value()
        # Esegui la ricerca con il modello
        my_index = Index()
        model = IRModel(my_index)
        resDict = model.search(query, resLimit=limit)

        # Configura la tabella
        self.table_widget.setRowCount(len(resDict))
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Drug", "Condition", "Review", "Rating"])

        # Popola la tabella con i risultati
        for row, (key, values) in enumerate(resDict.items()):
            drug_item = QTableWidgetItem(values[0])
            condition_item = QTableWidgetItem(values[1])
            review_item = QTableWidgetItem(values[2])
            rating_item = QTableWidgetItem(str(values[3]))

            self.table_widget.setItem(row, 0, drug_item)
            self.table_widget.setItem(row, 1, condition_item)
            self.table_widget.setItem(row, 2, review_item)
            self.table_widget.setItem(row, 3, rating_item)

        # Ridimensiona le colonne
        self.table_widget.resizeColumnsToContents()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = SearchApp()
    mainWindow.show()
    sys.exit(app.exec_())
