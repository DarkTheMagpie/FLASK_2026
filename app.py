from flask  import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    return conn 

@app.route("/")
def index():
    conn = get_db()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()

    return render_template("index.html", books = books)

def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

@app.route("/add", methods = ["GET", "POST"])
def add_books():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        year = request.form["year"]

        conn = get_db()
        conn.execute(
            "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
            (title, author, year)
        )
        conn.commit()
        conn.close()

        return redirect("/")
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_book(id):

    conn = get_db()

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        year = request.form["year"]

        conn.execute(
            "UPDATE books SET title=?, author=?, year=? WHERE id=?",
            (title, author, year, id)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    book = conn.execute(
        "SELECT * FROM books WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template("edit.html", book=book)

@app.route("/delete/<int:id>")
def delete_books(id):
    conn = get_db()
    conn.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    # create_table()
    app.run(debug = True)

