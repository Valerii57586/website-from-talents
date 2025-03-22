from flask import Flask, render_template, redirect, request, url_for, session, jsonify, send_from_directory
from sqltools import sqltools as sq
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
from redis import Redis
from markdown2 import markdown
from werkzeug.utils import secure_filename
import os
from algorithm_tools import algorithm_tools as AlgorithmTools

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)
app.secret_key = "msk"
UPLOAD_FOLDER = "static/images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


sq.create_table(dbname="data.db", table_name="users", columns=[
    ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    ("username", "TEXT"),
    ("password", "TEXT"),
    ("email", "TEXT"),
    ("name", "TEXT"),
    ("surname", "TEXT"),
    ("avatar", "TEXT DEFAULT ''"),
    ("header_photo", "TEXT DEFAULT ''"),
    ("status", "TEXT DEFAULT ''"),
    ("about", "TEXT DEFAULT ''"),
    ("git_link", "TEXT DEFAULT ''"),
    ("other_links", "TEXT DEFAULT ''"),
    ("favorites", "TEXT DEFAULT ''"),
    ("last_seen", "TEXT DEFAULT ''"),
    ("comments_on_wall", "TEXT DEFAULT ''"),
    ("raiting", "INTEGER DEFAULT 0")])


sq.create_table(dbname="data.db", table_name="posts", columns=[
    ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    ("email", "TEXT"),
    ("title", "TEXT"),
    ("content", "TEXT"),
    ("date", "TEXT"),
    ("files", "TEXT DEFAULT ''"),
    ("images", "TEXT DEFAULT ''"),
    ("author_username", "TEXT"),
    ("code_theme", "TEXT"),
    ("tags", "TEXT"),
    ("veiwers", "TEXT DEFAULT ''"),
    ("contributors", "TEXT DEFAULT ''")])


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


@app.route("/recomendations")
def recomendations():
    email = session.get("email")
    userdata = sq.get_column_value_by_name("users", "*", ("email", email), "data.db")[0]
    recommended_posts = AlgorithmTools.get_recommendations(email)[:5]
    return render_template("recomendations.html", recommended_posts=recommended_posts, username=userdata[1], )


@app.route("/get_usernames")
def get_usernames():
    usernames = sq.get_column_value_by_name("users", "username", (1, 1), "data.db")
    return jsonify([username[0] for username in usernames]) if usernames else jsonify([])


@app.route("/porfile_edit/<username>", methods=["GET", "POST"])
def porfile_edit(username):
    email = session.get("email")
    old_user_data = list(sq.get_column_value_by_name("users", "*", ("email", email), "data.db")[0])
    old_username = old_user_data[1]
    old_name = old_user_data[4]
    old_surname = old_user_data[5]
    old_avatar = old_user_data[6]
    old_header_photo = old_user_data[7]
    old_about = old_user_data[9]
    old_status = old_user_data[8]
    old_git_link = old_user_data[10]
    old_other_links = old_user_data[11]
    avatar = old_avatar
    if email is None:
        return redirect(url_for("register"))
    if username == sq.get_column_value_by_name("users", "username", ("email", email), "data.db")[0][0]:
        if request.method == "POST":
            if "avatar" in request.files:
                try:
                    os.remove(os.path.join(app.config["UPLOAD_FOLDER"], old_avatar.rsplit("/", 1)[1]))
                except:
                    pass
                avatar_file = request.files["avatar"]
                if avatar_file and AlgorithmTools.allowed_file(avatar_file.filename, ALLOWED_EXTENSIONS):
                    filename = username + "." + avatar_file.filename.rsplit(".", 1)[1].lower()
                    avatar_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    avatar = url_for("static", filename=f"images/{filename}")
                    sq.update_column_value("users", {"avatar": avatar}, ("email", email), "data.db")
            else:
                avatar = old_avatar
            username = request.form["username"]
            # name = request.form["name"]
            # surname = request.form["surname"]
            status = request.form["status"]
            about = request.form["about"]
            git_link = request.form["git_link"]
            other_links = request.form["other_links"]
            # header_photo = request.form["header_photo"]
            if git_link is None:
                git_link = old_git_link
            if other_links is None:
                other_links = old_other_links
            if about is None:
                about = old_about
            if status is None:
                status = old_status
            sq.update_column_value("users", {"username": username, "status": status, "about": about, "git_link": git_link, "other_links": other_links, "avatar": avatar}, ("email", email), "data.db")
            return redirect(url_for("profile", username=username))
        return render_template("profile_edit.html", old_username=old_username, username=username, old_name=old_name, old_surname=old_surname, old_avatar=old_avatar, old_header_photo=old_header_photo, old_about=old_about, old_status=old_status, old_git_link=old_git_link, old_other_links=old_other_links)
    else:
        return redirect(url_for("profile", username=username))


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
    userdata = sq.get_column_value_by_name("users", "*", ("username", username), "data.db")[0]
    username = userdata[1]
    password = userdata[2]
    email = userdata[3]
    name = userdata[4]
    surname = userdata[5]
    avatar = userdata[6]
    header_photo = userdata[7]
    status = userdata[8]
    about = userdata[9]
    posts = sq.get_column_value_by_name("posts", "id, title", ("author_username", username), "data.db")
    git_link = userdata[10]
    other_links = userdata[11]
    favorites = userdata[12]
    last_seen = userdata[13]
    comments_on_wall = userdata[14]
    raiting = userdata[15]
    return render_template("profile.html", username=username, name=name, surname=surname, avatar=avatar, header_photo=header_photo, current_online=current_online, about=about, status=status, posts=posts, git_link=git_link, other_links=other_links, raiting=raiting)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    email = session.get("email")
    username = sq.get_column_value_by_name("users", "username", ("email", email), "data.db")[0][0]
    try:
        valid_email = sq.get_column_value_by_name("posts", "email", ("id", id), "data.db")[0][0]
        post = sq.get_column_value_by_name('posts', '*', ('id', id), 'data.db')[0]
        if request.method == "POST":
            if email == valid_email or username in post[11]:
                date = datetime.now().strftime("%d-%m-%y %H:%M")
                title = request.form["title"]
                content = request.form["content"]
                code_theme = request.form["code-theme"]
                tags = request.form["tags"]
                contributors = request.form["contributors"]
                sq.update_column_value("posts", {"title": title, "content": content, "code_theme": code_theme, "tags": tags, "date": date, "contributors": contributors}, ("id", id), "data.db")
                sq.update_column_value("users", {"last_seen": date}, ("email", email), "data.db")
                return redirect(url_for("post", id=id))
            return redirect(url_for("main"))
    except:
        pass
    return render_template("edit.html", post=post)


@app.route("/delete/<int:id>")
def delete(id):
    email = session.get("email")
    date = datetime.now().strftime("%d-%m-%y %H:%M")
    try:
        valid_email = sq.get_column_value_by_name("posts", "email", ("id", id), "data.db")[0][0]
        if email == valid_email:
            sq.delete_record("posts", ("id", id), "data.db")
            sq.update_column_value("users", {"last_seen": date}, ("email", email), "data.db")
    except:
        pass
    return redirect(url_for("main"))


@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    email = session.get("email")
    if email:
        date = datetime.now().strftime("%d-%m-%y %H:%M")
        sq.update_column_value("users", {"last_seen": date}, ("email", email), "data.db")
    current_username = sq.get_column_value_by_name("users", "username", ("email", email), "data.db")[0][0]
    post = sq.get_column_value_by_name('posts', '*', ('id', id), 'data.db')[0]
    post = list(post)
    post_tags = post[9]
    viewers = post[10]
    if current_username not in (viewers or ""):
        sq.update_column_value("posts", {"veiwers": viewers + " " + current_username}, ("id", id), "data.db")
        current_favorites = sq.get_column_value_by_name("users", "favorites", ("email", email), "data.db")[0][0]
        new_favorites = current_favorites + " " + post_tags if current_favorites else post_tags
        sq.update_column_value("users", {"favorites": new_favorites}, ("email", email), "data.db")
    else:
        pass
    viewers = post[10]
    if viewers == None:
        veiw_count = 0
    else:
        veiw_count = len(viewers.split())
    post[3] = markdown(post[3], extras=['fenced-code-blocks', 'code-friendly'])
    username = post[7]
    comments = sq.get_column_value_by_name("comments", "*", ("post_id", id), "data.db")
    replies = sq.get_column_value_by_name("replys", "*", (1, 1), "data.db")
    contributors = post[11]
    if request.method == "POST":
        comment = request.form["comment"]
        if comment:
            date = datetime.now().strftime("%d-%m-%y %H:%M")
            sq.add_record("comments", {"username": username, "post_id": id, "content": comment, "date": date}, "data.db")
            return redirect(url_for("post", id=id))
    return render_template('post.html', post=post, comments=comments, username=username, veiw_count=veiw_count, replies=replies, contributors=contributors)


@app.route("/", methods=["GET", "POST"])
def main():
    search_query = ""
    username = ""
    email = session.get("email")
    if email:
        date = datetime.now().strftime("%d-%m-%y %H:%M")
        sq.update_column_value("users", {"last_seen": date}, ("email", email), "data.db")
    else:
        return redirect(url_for("register"))
    current_online = len(active_users)
    try:
        posts = sq.get_column_value_by_name("posts", "*", (1, 1), "data.db")
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
        name = request.form["name"]
        surname = request.form["surname"]
        if sq.exists_in_table(table_name="users", condition=("email", email), dbname="data.db") or sq.exists_in_table(table_name="users", condition=("username", username), dbname="data.db"):
            return render_template("register.html", message="Accaunt with this username or email already exists")
        try:
            sq.add_record("users", {"username": username, "password": password, "email": email, "name": name, "surname": surname}, "data.db")
            return redirect(url_for("login"))
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
    date = datetime.now().strftime("%d-%m-%y %H:%M")
    sq.update_column_value("users", {"last_seen": date}, ("email", email), "data.db")
    if request.method == "POST":
        if email is None:
            return redirect(url_for("register"))
        title = request.form["title"]
        content = request.form["content"]
        code_theme = request.form["code-theme"]
        date = datetime.now().strftime("%d-%m-%y %H:%M")
        author_username = sq.get_column_value_by_name("users", "username", ("email", email), "data.db")[0][0]
        tags = request.form["tags"]
        contributors = request.form["contributors"]
        sq.add_record("posts", {"email": email, "title": title, "content": content, "date": date, "author_username": author_username, "code_theme": code_theme, "tags":tags, "contributors": contributors}, "data.db")
        return redirect(url_for("main"))
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
