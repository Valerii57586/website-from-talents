from flask import Flask, render_template, redirect, request, url_for, session
from sqltools import sqltools as sq
from werkzeug.middleware.proxy_fix import ProxyFix
import datetime
from redis import Redis


redis_client = Redis(host='localhost', port=6379, db=0)


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)
app.secret_key = "msk"


sq.create_table(dbname="data.db", table_name="users", columns=[
    ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    ("username", "TEXT"),
    ("password", "TEXT"),
    ("email", "TEXT"),
    ("name", "TEXT"),
    ("surname", "TEXT"),
    ("profile_photo_url", "TEXT")])


sq.create_table(dbname="data.db", table_name="posts", columns=[
    ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    ("email", "TEXT"),
    ("title", "TEXT"),
    ("content", "TEXT"),
    ("category", "TEXT"),
    ("date", "TEXT"),
    ("files", "TEXT"),
    ("images", "TEXT"),
    ("author_username", "TEXT")])


sq.create_table(dbname="data.db", table_name="comments", columns=[
    ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    ("email", "TEXT"),
    ("post_id", "INTEGER"),
    ("content", "TEXT")])


active_users = set()


@app.route("/profile/<username>")
def profile(username):
    name = sq.get_column_value_by_name("users", "name", ("username", username), "data.db")[0][0]
    surname = sq.get_column_value_by_name("users", "surname", ("username", username), "data.db")[0][0]
    return render_template("profile.html", username=username, name=name, surname=surname)


@app.route('/myprofile')
def my_profile():
    email = session.get("email")
    username = sq.get_column_value_by_name("users", "username", ("email", email), "data.db")[0][0]
    name = sq.get_column_value_by_name("users", "name", ("email", email), "data.db")[0][0]
    surname = sq.get_column_value_by_name("users", "surname", ("email", email), "data.db")[0][0]
    return render_template("profile.html", username=username, name=name, surname=surname)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    email = session.get("email")
    try:
        valid_email = sq.get_column_value_by_name("posts", "email", ("id", id), "data.db")[0][0]
        post = sq.get_column_value_by_name('posts', 'id, title, content, category', ('id', id), 'data.db')[0]
        if request.method == "POST":
            if email == valid_email:
                date = datetime.datetime.now().strftime("%d-%m-%y %H:%M")
                title = request.form["title"]
                content = request.form["content"]
                category = request.form["category"]
                sq.update_column_value("posts", "title", title, ("id", id), "data.db")
                sq.update_column_value("posts", "content", content, ("id", id), "data.db")
                sq.update_column_value("posts", "category", category, ("id", id), "data.db")
                sq.update_column_value("posts", "date", date, ("id", id), "data.db")
                return redirect(url_for("main"))
            return redirect(url_for("main"))
    except:
        pass
    return render_template("edit.html", post=post)


@app.route("/delete/<int:id>")
def delete(id):
    email = session.get("email")
    try:
        valid_email = sq.get_column_value_by_name("posts", "email", ("id", id), "data.db")[0][0]
        if email == valid_email:
            sq.delete_record("posts", ("id", id), "data.db")
    except:
        pass
    return redirect(url_for("main"))


@app.route('/post/<int:id>')
def post(id):
    views_key = ""
    email = session.get("email")
    if email:
        views_key = f"post:{id}:views"
        if not redis_client.sismember(views_key, email):
            redis_client.sadd(views_key, email)
            redis_client.incr(f"post:{id}:view_count")
    view_count = int(redis_client.get(f"post:{id}:view_count") or 0)
    post = sq.get_column_value_by_name('posts', 'id, title, content, category, date, author_username, email', ('id', id), 'data.db')[0]
    username = post[5]
    comments = sq.get_column_value_by_name("comments", "id, content, email", ("post_id", id), "data.db")
    return render_template('post.html', post=post, comments=comments, username=username, veiw_count=view_count)


@app.route("/", methods=["GET", "POST"])
def main():
    search_query = ""
    category = 'all'
    email = session.get("email")
    username = ""
    current_online = len(active_users)
    posts = sq.get_column_value_by_name("posts", "id, title, content, category, date, author_username, email", (1, 1), "data.db")
    try:
        username = sq.get_column_value_by_name("users", "username", ("email", email), "data.db")[0][0]
    except:
        pass
    if request.method == "POST":
        search_query = request.form["search-query"]
        category = request.form["category-select"]
        return render_template("index.html", posts=posts, email=email, search_query=search_query, category=category, username=username, current_online=current_online)
    return render_template("index.html", posts=posts, email=email, search_query=search_query, category=category, username=username, current_online=current_online)


@app.route("/reg", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        name = request.form["name"]
        surname = request.form["surname"]
        if password != confirm_password:
            return render_template("register.html", message="Passwords do not match")
        if sq.exists_in_table(table_name="users", condition=("email", email), dbname="data.db") and sq.exists_in_table(table_name="users", condition=("username", username), dbname="data.db"):
            return render_template("register.html", message="Accaunt with this username or email already exists")
        try:
            sq.add_record("users", {"username": username, "password": password, "email": email, "name": name, "surname": surname}, "data.db")
            return render_template("register.html", message="Success")
        except:
            return render_template("register.html", message="Something went wrong")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            if sq.get_column_value_by_name(table_name="users", column_to_get="password", condition=("email", email), dbname="data.db")[0][0] == password:
                session['email'] = email
                active_users.add(request.remote_addr)
                return redirect(url_for("main"))
            else:
                return render_template("login.html", message="Invalid email or password")
        except:
            return render_template("login.html", message="Invalid email or password")
    return render_template("login.html")


@app.route("/create_post", methods=["GET", "POST"])
def create_post():
    email = session.get("email")
    if email is None:
        return redirect(url_for("register"))
    if request.method == "POST":
        if email is None:
            return redirect(url_for("register"))
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]
        date = datetime.datetime.now().strftime("%d-%m-%y %H:%M")
        author_username = sq.get_column_value_by_name("users", "username", ("email", email), "data.db")[0][0]
        try:
            sq.add_record("posts", {"email": email, "title": title, "content": content, "category": category, "date": date, "author_username": author_username}, "data.db")
            return redirect(url_for("main"))
        except:
            return redirect(url_for("create_post"))
    return render_template("create_post.html")


@app.route("/logout")
def logout():
    active_users.discard(request.remote_addr)
    session.clear()
    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(debug=True)
