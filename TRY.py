import sqlite3
import sys
from pathlib import Path


from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PyQt5.QtCore import Qt

DB_FILE = Path("app.db")


class FirstWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно 1")
        self.setGeometry(100, 100, 300, 200)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        self.hello_button = QPushButton("Привет")
        self.hello_button.clicked.connect(self.show_ura)

        self.bye_button = QPushButton("Пока")
        self.bye_button.clicked.connect(self.close_app)

        layout.addWidget(self.hello_button)
        layout.addWidget(self.bye_button)

    def show_ura(self):
        QMessageBox.information(self, "Привет", "Ура!")
        save_event("Привет", "Ура!")
        if second_window:
            second_window.refresh_table()

    def close_app(self):
        save_event("Пока", "Закрытие программы")
        self.close()
        QApplication.quit()


class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно 2")
        self.setGeometry(450, 100, 500, 250)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["id", "button", "message"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Лог нажатий"))
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.refresh_table()

    def refresh_table(self):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT id, button, message FROM button_log ORDER BY id DESC LIMIT 20")
        rows = cur.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_index, col_index, item)


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS button_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            button TEXT NOT NULL,
            message TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def save_event(button, message=""):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO button_log(button, message) VALUES (?, ?)",
        (button, message),
    )
    conn.commit()
    conn.close()


def main():
    global second_window
    app = QApplication(sys.argv)
    init_db()

    first_window = FirstWindow()
    second_window = SecondWindow()

    first_window.show()
    second_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    second_window = None
    main()
