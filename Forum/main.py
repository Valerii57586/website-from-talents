from flask import Flask, render_template, redirect, request, url_for
from sqltools import sqltools as sq


app = Flask(__name__)
sq.create_table(dbname="users.db", table_name="data", columns=[("id", "INTEGER PRIMARY KEY AUTOINCREMENT"), ("username", "TEXT"), ("password", "TEXT"), ("email", "TEXT")])


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/reg", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if sq.exists_in_table(table_name="data", condition=("email", email), dbname="users.db"):
            return "Такой email существует"
        try:
            sq.add_record(table_name="data", values={"username": username, "password": password, "email": email}, dbname="users.db")
            return redirect(url_for("login"))
        except:
            return "Error"
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if sq.get_column_value_by_name(table_name="data", column_to_get="password", condition=("email", email), dbname="users.db") == password:
            return redirect(url_for("main"))
        else:
            return redirect(url_for("register"))
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)

