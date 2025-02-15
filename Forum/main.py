from flask import Flask, render_template, redirect, request, url_for, session
from sqltools import sqltools as sq
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
sq.create_table(dbname="users.db", table_name="data", columns=[("id", "INTEGER PRIMARY KEY AUTOINCREMENT"), ("username", "TEXT"), ("password", "TEXT"), ("email", "TEXT")])
sq.create_table(dbname="users.db", table_name="posts", columns=[("id", "INTEGER PRIMARY KEY AUTOINCREMENT"), ("email", "TEXT"), ("title", "TEXT"), ("content", "TEXT"), ("category", "TEXT")])

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)
app.secret_key = "msk"


@app.route("/")
def main():
    email = session.get("email")
    posts = sq.get_column_value_by_name(table_name="posts", column_to_get="id, title, category, email, content", condition=(1, 1), dbname="users.db")
    return render_template("index.html", posts=posts, email=email)


@app.route("/reg", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if sq.exists_in_table(table_name="data", condition=("email", email), dbname="users.db"):
            return redirect(url_for("login"))
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
        print(password, sq.get_column_value_by_name(table_name="data", column_to_get="password", condition=("email", email), dbname="users.db"))
        if sq.get_column_value_by_name(table_name="data", column_to_get="password", condition=("email", email), dbname="users.db")[0][0] == password:
            session['email'] = email
            return redirect(url_for("create_post"))
        else:
            return redirect(url_for("register"))
    return render_template("login.html")


@app.route("/post", methods=["GET", "POST"])
def create_post():
    email = session.get("email")
    if request.method == "POST":
        if email is None:
            return redirect(url_for("register"))
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]
        try:
            sq.add_record(table_name="posts", values={"email": email, "title": title, "content": content, "category": category}, dbname="users.db")
            return redirect(url_for("main"))
        except:
            return redirect(url_for("create_post"))
    return render_template("post.html")


if __name__ == "__main__":
    app.run(debug=True)
