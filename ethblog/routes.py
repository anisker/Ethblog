import os, shutil, time, secrets
from datetime import datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from ethblog import app, db, bcrypt, mail, web3, contract
from ethblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from ethblog.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
 
@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404

@app.route("/home")
@login_required
def home():
	numberOfPosts = contract.functions.getNumberOfPosts().call()
	i=numberOfPosts-1
	posts = []
	while i >= 0:
		posts.append([i,contract.functions.posts(i).call()])
		i-=1
	return render_template('home.html', posts= posts)


@app.route("/about")
def about():
	return render_template('about.html', title='About')

@app.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email = form.email.data, password= hashed_password)
		shutil.copy(os.path.join(app.root_path, 'static/profile_pics','default.jpg'),os.path.join(app.root_path, 'static/profile_pics',form.username.data+'.jpg'))
		user.image_file = form.username.data+'.jpg'
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created !', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title = 'Register', form=form)

@app.route("/", methods=['GET','POST'])
@app.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email= form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user,remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect (next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title = 'Login', form=form)
	
@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

def save_picture(username, form_picture):
	_t, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = username + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(current_user.username,form.picture.data)
			current_user.image_file = picture_file
			db.session.commit()
			flash('Your account has been updated!', 'success')
		return redirect(url_for('account'))
	image_file = url_for('static', filename= 'profile_pics/' + current_user.image_file)
	user = User.query.filter_by(username=current_user.username).first_or_404()
	numberOfUserPosts = contract.functions.ownerPostCount(current_user.username).call()
	i = numberOfUserPosts-1
	posts = []
	while i >= 0:
		temp = contract.functions.usernamesPosts(current_user.username,i).call()
		posts.append([temp,contract.functions.posts(temp).call()])
		i-=1
	return render_template('account.html', title = 'Account', image_file= image_file, form = form, posts= posts, user=user)

@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		tx_hash = contract.functions.createPost(current_user.username,datetime.now().strftime("%m-%d-%Y"),form.title.data,form.content.data).transact()
		web3.eth.waitForTransactionReceipt(tx_hash)
		flash('Your post has been created !', 'success')
		return redirect(url_for('home'))
	return render_template('create_post.html', title = 'New Post', form = form, legend = 'New post')

@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
	try:
		post = [post_id, contract.functions.getPost(post_id).call()]
	except ValueError as err:
		abort(404)
	return render_template('post.html', title= post[1][2], post = post)

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
	try:
		post = [post_id, contract.functions.getPost(post_id).call()]
	except ValueError as err:
		abort(404)
	if post[1][0] != current_user.username:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		tx_hash = contract.functions.setPost(post_id,form.title.data,form.content.data).transact()
		web3.eth.waitForTransactionReceipt(tx_hash)
		flash('Your post has been updated !', 'success')
		return redirect(url_for('post', post_id=post_id))
	elif request.method == 'GET':
		post = contract.functions.getPost(post_id).call()
		form.title.data = post[2]
		form.content.data = post[3]
	return render_template('create_post.html', title= 'Update post', form = form, legend = 'Update post')

@app.route("/user/<string:username>")
@login_required
def user_posts(username):
	user = User.query.filter_by(username=username).first_or_404()
	numberOfUserPosts = contract.functions.ownerPostCount(username).call()
	i = numberOfUserPosts-1
	posts = []
	while i >= 0:
		temp = contract.functions.usernamesPosts(username,i).call()
		posts.append([temp,contract.functions.posts(temp).call()])
		i=i-1
	return render_template('user_posts.html', posts= posts, user=user , numberOfUserPosts= numberOfUserPosts)

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password reset request', sender='anisker96@gmail.com', recipients=[user.email])
	msg.body = f''' To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email and no changes will be made
'''
	mail.send(msg)
@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password','info')
		return redirect(url_for('login'))
	return render_template('reset_request.html', title = 'Reset password', form = form)

@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password= hashed_password
		db.session.commit()
		flash('Your password has been updated ! You can log in now !', 'success')
		return redirect(url_for('login'))

	return render_template('reset_token.html', title = 'Reset password', form = form)
