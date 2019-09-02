from flask import render_template, flash, redirect, url_for, abort, request
from CLEANBLOG import app, db, mail, Message
from CLEANBLOG.forms import RegisterForm,LoginForm,PostForm,ContactForm
from CLEANBLOG.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=3)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Home',posts=posts, next_url=next_url, prev_url=prev_url)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.name.data} account created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash(f'Login Unsuccessful', 'danger')
    return render_template('login.html', title='Login',form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,subtitle=form.subtitle.data,post_text=form.post_text.data, user=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Post is created', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='Create Post',form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title='post.title',post=post)


@app.route("/post/<int:post_id>/edit", methods=['GET','POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():

        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.post_text = form.post_text.data
        db.session.commit()
        flash(f'Post is edited', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.subtitle.data = post.subtitle
        form.post_text.data = post.post_text
        return render_template('create_post.html', title='Edit Post',form=form)

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Post is deleted', 'success')
    return redirect(url_for('index'))

@app.route("/contact", methods=['GET','POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            msg = Message(form.name.data,sender="Clean Blog Contact Form",recipients=["aykutalpturkay@gmail.com"])
            msg.body = """
            From: %s
            <%s>
            %s
            """ %(form.email.data, form.phone.data, form.message.data)
            mail.send(msg)
            
            flash(f'We received your message successfully','success')
            return redirect(url_for('contact'))
        else:
            flash(f'OPS There is a problem','danger')
    
    elif request.method == 'GET':
        return render_template('contact.html', title='Contact',form=form)

    
