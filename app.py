from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, login_required, logout_user, current_user
from extensions.extensions import db, login_manager
from models.models import Users, Post
from markdown2 import markdown


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sorp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sorpcrftoken'

db.init_app(app)
login_manager.init_app(app)
csrf = CSRFProtect(app)
login_manager.login_view = 'login'


@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/reg', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        user = Users(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return render_template('auth/reg.html')


@app.route('/log', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
    flash('Invalid username or password')
    return render_template('auth/log.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        content = markdown(content, extras=['fenced-code-blocks', 'code-friendly'])
        post = Post(author=current_user.username, title=title, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('posts/create_post.html')


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get(post_id)
    return render_template('posts/post.html', post=post)


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.content = markdown(post.content, extras=['fenced-code-blocks', 'code-friendly'])
        db.session.commit()
        return redirect(url_for('post', post_id=post.id))
    return render_template('posts/edit_post.html', post=post)

@app.route("/profile")
@login_required
def profile():
    return render_template('auth/profile.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
