import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from webapp import app, db
from webapp.forms import RegistrationForm, LoginForm, UpdateProfileForm, NewQuestionForm
from webapp.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from datetime import timedelta

@app.route('/')
@app.route('/doubtville')
def doubtville():
    return render_template('doubtville.html')

@app.route('/home')
@login_required
def home():
    posts = Post.query.filter_by(post_std=current_user.std).all()
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # noinspection PyArgumentList
        user = User(name=form.name.data, email=form.email.data, adm_no=form.adm_no.data, std=form.std.data)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(adm_no=form.adm_no.data).first()
        os.mkdir('C:\\Users\\user\\Projects\\DoubtVille\\webapp\static\\Users\\'+str(user.id))
        login_user(user, remember=True, duration=timedelta(days=100))
        flash(f'Account has been created for {form.name.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.adm_no == form.adm_no.data:
            login_user(user, remember=True, duration=timedelta(days=100))
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and admission number', 'fail')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('doubtville'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.std = form.std.data
        db.session.commit()
        flash('Your account info has been updated!', 'success-profile')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.std.data = current_user.std
    return render_template('profile.html', form=form)

def save_image(form_picture, post_id):
    name = str(post_id) + '-' + secrets.token_hex(4)
    _, ext = os.path.splitext(form_picture.filename)
    picture_fn = name + ext
    path = os.path.join(app.root_path, 'static/Users/' + str(current_user.id), picture_fn)
    if bool(form_picture):
        img = Image.open(form_picture)
        w = int(img.width*0.7)
        h = int(img.height*0.7)
        i = img.resize((w, h))
        i.save(path)
    return picture_fn

@app.route('/new_question', methods=['GET', 'POST'])
@login_required
def new_question():
    form = NewQuestionForm()
    if form.validate_on_submit():
        if bool(form.post_image.data):
            images = []
            post_id = len(current_user.posts)+1
            for image in form.post_image.data:
                image_name = save_image(image, post_id)
                images.append(image_name)
            post_images = ', '.join(images)
        else:
            post_images = ''
        post = Post(question=form.question.data, content=form.content.data, post_std=form.post_std.data,
                    subject=form.subject.data, post_image=post_images, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('new_question.html', title='New Question', legend='Post a New Question', form=form)

@app.route('/update_<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_question(post_id):
    post = Post.query.get_or_404(int(post_id))
    old_images = post.post_image
    if post.author != current_user:
        abort(403)
    form = NewQuestionForm()
    if form.validate_on_submit():
        # Looping through the image files to join their names in a string
        if bool(form.post_image.data):
            images = []
            for image in form.post_image.data:
                image_name = save_image(image, post.id)
                images.append(image_name)
            post_images = ', '.join(images)
        else:
            post_images = ''
        # Deleting the old images associated with the post
        old_img_list = old_images.split(', ')
        if bool(old_img_list):
            for img in old_img_list:
                path = os.path.join(app.root_path, 'static/Users/' + str(post.author.id), img)
                os.remove(path)
        # Updating the fields with the new values
        post.question = form.question.data
        post.content = form.content.data
        post.post_std = form.post_std.data
        post.subject = form.subject.data
        post.post_image = post_images
        # Committing the changes to the database
        db.session.commit()
        flash('Your question has been updated!', 'success')
        return redirect(url_for('view_question', post_id=post.id))
    # Populating the fields with existing data
    elif request.method == 'GET':
        form.question.data = post.question
        form.content.data = post.content
        form.post_std.data = post.post_std
        form.subject.data = post.subject
    return render_template('new_question.html', title='Update Question', legend='Update Question', form=form)

@app.route('/delete_<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_question(post_id):
    post = Post.query.get_or_404(int(post_id))
    old_images = post.post_image
    if post.author != current_user:
        abort(403)
    # Deleting the old images associated with the post
    old_img_list = old_images.split(', ')
    if bool(old_img_list):
        for img in old_img_list:
            path = os.path.join(app.root_path, 'static/Users/' + str(post.author.id), img)
            os.remove(path)
    # Deleting the post
    db.session.delete(post)
    db.session.commit()
    flash('Your question has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/question_<int:post_id>')
@login_required
def view_question(post_id):
    post = Post.query.get_or_404(int(post_id))
    user_id = str(post.author.id) + '/'
    images = post.post_image
    images = images.split(', ')
    return render_template('question.html', user_id=user_id, post=post, images=images)

# URL for different classes
@app.route('/class6')
def class6():
    return render_template('class 6-10.html', title='Class 6')

@app.route('/class7')
def class7():
    return render_template('class 6-10.html', title='Class 7')

@app.route('/class8')
def class8():
    return render_template('class 6-10.html', title='Class 8')

@app.route('/class9')
def class9():
    return render_template('class 6-10.html', title='Class 9')

@app.route('/class10')
def class10():
    return render_template('class 6-10.html', title='Class 10')

@app.route('/class11')
def class11():
    return render_template('class 11-12.html', title='Class 11')

@app.route('/class12')
def class12():
    return render_template('class 11-12.html', title='Class 12')