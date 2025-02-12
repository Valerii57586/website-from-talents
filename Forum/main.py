from flask import Flask, render_template, redirect, request
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
        try:
            sq.add_record(table_name="data", values={"username": username, "password": password, "email": email}, dbname="users.db")
            return "It works"
        except:
            return "Error"
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)

