from flask import Flask, render_template, redirect, request, url_for, session
from sqltools import sqltools as sq
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
from redis import Redis
from markdown2 import markdown


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
    ("avatar", "TEXT"),
    ("header_photo", "TEXT"),
    ("status", "TEXT"),
    ("about", "TEXT"),
    ("git_link", "TEXT"),
    ("other_links", "TEXT")])


sq.create_table(dbname="data.db", table_name="posts", columns=[
    ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    ("email", "TEXT"),
    ("title", "TEXT"),
    ("content", "TEXT"),
    ("date", "TEXT"),
    ("files", "TEXT"),
    ("images", "TEXT"),
    ("author_username", "TEXT"),
    ("code_theme", "TEXT"),
    ("tags", "TEXT"),
    ("veiwers", "TEXT")])


sq.create_table(dbname="data.db", table_name="comments", columns=[
    ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    ("username", "TEXT"),
    ("post_id", "INTEGER"),
    ("content", "TEXT"),
    ("date", "TEXT")])


sq.create_table(dbname="data.db", table_name="replys", columns=[
    ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    ("username", "TEXT"),
    ("comment_id", "INTEGER"),
    ("content", "TEXT")])


active_users = set()


@app.route("/add_image")
def add_image():

    return render_template("add_image.html")


@app.route("/add_reply/<int:comment_id>/<int:post_id>", methods=["GET", "POST"])
def reply(comment_id, post_id):
    email = session.get("email")
    if email:
        username = sq.get_column_value_by_name("users", "username", ("email", email), "data.db")[0][0]
        reply_cntent = request.form["reply"]
    if reply_cntent:
        sq.add_record("replys", {"username": username,
                                 "comment_id": comment_id,
                                 "content": reply_cntent},
                                 "data.db")
    return redirect(url_for("post", id=post_id))


@app.route('/profile/<username>')
def profile(username):
    current_online = len(active_users)
    email = session.get("email")
    username = sq.get_column_value_by_name("users", "username", ("email", email), "data.db")[0][0]
    name = sq.get_column_value_by_name("users", "name", ("email", email), "data.db")[0][0]
    surname = sq.get_column_value_by_name("users", "surname", ("email", email), "data.db")[0][0]
    avatar = sq.get_column_value_by_name("users", "avatar", ("email", email), "data.db")[0][0]
    header_photo = sq.get_column_value_by_name("users", "header_photo", ("email", email), "data.db")[0][0]
    about = sq.get_column_value_by_name("users", "about", ("email", email), "data.db")[0][0]
    status = sq.get_column_value_by_name("users", "status", ("email", email), "data.db")[0][0]
    posts = sq.get_column_value_by_name("posts", "id, title", ("author_username", username), "data.db")
    return render_template("profile.html", username=username, name=name, surname=surname, avatar=avatar, header_photo=header_photo, current_online=current_online, about=about, status=status, posts=posts)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    email = session.get("email")
    try:
        valid_email = sq.get_column_value_by_name("posts", "email", ("id", id), "data.db")[0][0]
        post = sq.get_column_value_by_name('posts', 'id, title, content, code_theme, tags', ('id', id), 'data.db')[0]
        if request.method == "POST":
            if email == valid_email:
                date = datetime.now().strftime("%d-%m-%y %H:%M")
                title = request.form["title"]
                content = request.form["content"]
                code_theme = request.form["code-theme"]
                tags = request.form["tags"]
                sq.update_column_value("posts", "title", title, ("id", id), "data.db")
                sq.update_column_value("posts", "content", content, ("id", id), "data.db")
                if tags != "":
                    sq.update_column_value("posts", "tags", tags, ("id", id), "data.db")
                sq.update_column_value("posts", "date", date, ("id", id), "data.db")
                if code_theme != "":
                    sq.update_column_value("posts", "code_theme", code_theme, ("id", id), "data.db")
                return redirect(url_for("post", id=id))
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


@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    email = session.get("email")
    current_username = sq.get_column_value_by_name("users", "username", ("email", email), "data.db")[0][0]
    viewers = sq.get_column_value_by_name("posts", "veiwers", ("id", id), "data.db")[0][0]
    if viewers == None:
        viewers = ""
    if current_username not in viewers:
        sq.update_column_value("posts", "veiwers", viewers + " " + current_username, ("id", id), "data.db")
    else:
        pass
    viewers = sq.get_column_value_by_name("posts", "veiwers", ("id", id), "data.db")[0][0]
    veiw_count = len(viewers.split())
    post = sq.get_column_value_by_name('posts', 'id, title, content, date, author_username, email, code_theme, tags', ('id', id), 'data.db')[0]
    post = list(post)
    post[2] = markdown(post[2], extras=['fenced-code-blocks', 'code-friendly'])
    username = post[4]
    comments = sq.get_column_value_by_name("comments", "id, content, username, date", ("post_id", id), "data.db")
    replies = sq.get_column_value_by_name("replys", "id, content, username, comment_id", (1, 1), "data.db")
    if request.method == "POST":
        comment = request.form["comment"]
        if comment:
            date = datetime.now().strftime("%d-%m-%y %H:%M")
            sq.add_record("comments", {"username": username, "post_id": id, "content": comment, "date": date}, "data.db")
            return redirect(url_for("post", id=id))
    return render_template('post.html', post=post, comments=comments, username=username, veiw_count=veiw_count, replies=replies)


@app.route("/", methods=["GET", "POST"])
def main():
    search_query = ""
    email = session.get("email")
    username = ""
    current_online = len(active_users)
    posts = sq.get_column_value_by_name("posts", "id, title, content, date, author_username, email, tags", (1, 1), "data.db")
    try:
        username = sq.get_column_value_by_name("users", "username", ("email", email), "data.db")[0][0]
    except:
        pass
    if request.method == "POST":
        search_query = request.form["search-query"]
        return render_template("index.html", posts=posts, email=email, search_query=search_query, username=username, current_online=current_online)
    return render_template("index.html", posts=posts, email=email, search_query=search_query, username=username, current_online=current_online)


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
    tags = ""
    if email is None:
        return redirect(url_for("register"))
    if request.method == "POST":
        if email is None:
            return redirect(url_for("register"))
        title = request.form["title"]
        content = request.form["content"]
        code_theme = request.form["code-theme"]
        date = datetime.now().strftime("%d-%m-%y %H:%M")
        author_username = sq.get_column_value_by_name("users", "username", ("email", email), "data.db")[0][0]
        tags = request.form["tags"]
        try:
            sq.add_record("posts", {"email": email, "title": title, "content": content, "date": date, "author_username": author_username, "code_theme": code_theme, "tags":tags}, "data.db")
            return redirect(url_for("main"))
        except:
            return redirect(url_for("create_post"))
    return render_template("create_post.html")


@app.route("/logout")
def logout():
    email = session.get("email")
    if email is not None:
        active_users.discard(request.remote_addr)
        session.clear()
    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(debug=True)
