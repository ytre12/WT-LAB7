import sqlite3
from pathlib import Path

from flask import Flask, render_template, request

DATABASE = Path(__file__).with_name("points.db")

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def index():
    return render_template("main.html.j2")


@app.get("/hello2")
def hello2():
    name = request.args.get("name", "Гість")
    return render_template("hello.html.j2", name=name)


@app.get("/students")
def students():
    rows = []
    error = None

    if not DATABASE.exists():
        error = "Файл points.db ще не створений."
    else:
        conn = get_db()
        try:
            rows = conn.execute("SELECT id, name FROM student").fetchall()
        except sqlite3.OperationalError:
            error = "Таблиця student ще не створена."
        finally:
            conn.close()

    return render_template("students.html", students=rows, error=error)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
