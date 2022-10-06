from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, UserMixin, current_user, logout_user, login_required
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, TelField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agenda.db'
app.config['SECRET_KEY'] = '300922'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


def save_image(picture_file):
    picture_name = picture_file.filename
    picture_path = os.path.join(
        app.root_path, 'static/picture_files', picture_name)
    picture_file.save(picture_path)
    return picture_name


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

###################################### Models #############################################


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50),
                              nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Contacts(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    surname = db.Column(db.String(length=30), nullable=False)
    phone_number = db.Column(db.String(length=14), nullable=False)
    email_address = db.Column(db.String(length=12),
                              nullable=False)
    home_address = db.Column(db.String(length=20), nullable=False)
    description = db.Column(db.String(length=1024),
                            nullable=False)
    picture = db.Column(db.String(length=20),
                        nullable=True, default='default.png')
    owner = db.Column(db.Integer(), db.ForeignKey('users.id'))


##################################### Forms #################################################

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = Users.query.filter_by(
            username=username_to_check.data).first()
        if user:
            raise ValidationError(
                'Username already exists! Please try a different username')

    username = StringField(
        label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(
        label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(
        label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    email = StringField(label='Email:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class ContactForm(FlaskForm):
    name = StringField(label='Name:', validators=[DataRequired()])
    surname = StringField(label='Surname:',
                          validators=[DataRequired()])
    phone = TelField(label='Phone Number:', validators=[
                     Length(min=11, max=15), DataRequired()])
    email_address = StringField(
        label='Email address:', validators=[DataRequired()])
    home_address = StringField(
        label='Home Address:', validators=[DataRequired()])
    description = TextAreaField(
        label='User Name:', validators=[DataRequired()])
    picture = FileField(label="Update Profile Picture",
                        validators=[FileAllowed(['jpg', 'png', 'PNG'])])
    submit = SubmitField('Save')


@app.route('/', methods=['GET', 'POST'])
def sign_page():
    form = LoginForm()
    if form.validate_on_submit():
        user_found = Users.query.filter_by(
            email_address=form.email.data).first()
        if user_found:
            if user_found and user_found.check_password_correction(attempted_password=form.password.data):
                login_user(user_found)
                flash(
                    f'Success! You are logged in as: {user_found.username}', category='success')
                return redirect(url_for('list_page'))
            else:
                flash(
                    f'Usename or password does not match', category='danger')
        else:
            flash(
                f'User does not exist', category='danger')
    return render_template('index.html', form=form)


@app.route('/contacts', methods=['POST', 'GET'])
@login_required
def list_page():
    form = ContactForm()
    user_current_id = current_user.id
    contacts_list = Contacts.query.filter_by(
        owner=user_current_id).order_by(Contacts.name).all()
    if form.validate_on_submit():
        fund_email = Contacts.query.filter_by(
            owner=user_current_id, email_address=form.email_address.data).first()
        fund_phone = Contacts.query.filter_by(
            owner=user_current_id, phone_number=form.phone.data).first()
        if fund_email:
            flash(
                f'There is a contact with {fund_email.email_address}, please try another email', category='danger')
        elif fund_phone:
            flash(
                f'There is a contact with {fund_phone.phone_number}, please try another Phone Number', category='danger')
        else:
            image = form.picture.data
            if image != None:
                image_name = save_image(image)
            else:
                image_name = 'default.png'
            new_contact = Contacts(name=form.name.data, surname=form.surname.data, phone_number=form.phone.data,
                                   email_address=form.email_address.data, home_address=form.home_address.data, description=form.description.data, picture=image_name, owner=user_current_id)
            db.session.add(new_contact)
            db.session.commit()
            flash(f'User added successfuly', category='success')
            contacts_list = Contacts.query.filter_by(
                owner=user_current_id).order_by(Contacts.name).all()
            form.name.data = form.surname.data = form.phone.data = form.phone.data = form.email_address.data = form.home_address.data = form.description.data = ''
            redirect(url_for('list_page'))
    return render_template('list_page.html', form=form, contacts_list=contacts_list)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = Users(username=form.username.data,
                         email_address=form.email_address.data,
                         password=form.password1.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('sign_page'))
    return render_template('register_page.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for("sign_page"))


@app.route('/delete/<int:id>')
def delete_page(id):
    form = ContactForm()
    Contacts.query.filter(Contacts.id == id).delete()
    db.session.commit()
    user_current_id = current_user.id
    contacts_list = Contacts.query.filter_by(
        owner=user_current_id).order_by(Contacts.name).all()
    return render_template('list_page.html', form=form, contacts_list=contacts_list)


@app.route('/contacts/edit/<name>', methods=['GET', 'POST'])
def edit_contact(name):
    contact = Contacts.query.filter(Contacts.name == name).first()
    form = ContactForm()
    if form.validate_on_submit():
        contact.name = form.name.data
        contact.surname = form.surname.data
        contact.phone_number = form.phone.data
        contact.email_address = form.email_address.data
        contact.home_address = form.home_address.data
        contact.description = form.description.data
        image = form.picture.data
        if image != None:
            image_name = save_image(image)
            contact.picture = image_name
        db.session.commit()
        return redirect(url_for('list_page'))
    form.name.data = contact.name
    form.surname.data = contact.surname
    form.phone.data = contact.phone_number
    form.email_address.data = contact.email_address
    form.home_address.data = contact.home_address
    form.description.data = contact.description
    form.picture.data = contact.picture
    return render_template('edit_contact.html', form=form)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
