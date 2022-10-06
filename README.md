# Contact Book

It is an application that in the first place to log in to the page you need to create a user account, After that, you be able to create contacts that will be automatically listed on your page after saving it. the user can see the details of the created contact, as well as edit it and delete contact.

### Language of Project:

- Python
- Flask framework
- HTML
- CSS
- Bootstrap framwork
- Sqlite3

### Developed Features:

1. Login for diferent User
   - Create User
2. Dashboard
   - List all Contact automatically
   - Create Contacts
   - Edit Contact
   - Delet Contact

### Database Diagram:

![Database Diagram](static/picture_files/db_diagram.PNG)

### app.py
```Python
###################### database #########################
#class that represent Users table in database
class Users(db.Model, UserMixin):
   pass
   
#class that represent Contacts table in database
class Contacts(db.Model):
   pass
######################## Forms #########################

# Those are class form that I use to render form in the HTML templates

# Form to creat User for my application with 'username, email, and password'
class RegisterForm(FlaskForm):
   pss
 
 # Form that will render log in form in the application with an email and password and login button
 class LoginForm(FlaskForm):
   pass
 
 # Form that will render form to creat Contact on your in the application. And I use the same form to edit contact
 class ContactForm(FlaskForm):
   pass
 
######################## Routes ##########################
# Home route that render log in page for User log in the application
@app.route('/', methods=['GET', 'POST'])
def sign_page():
   pass
  
# Dashboard page that will list all your Contact automatically
@app.route('/contacts', methods=['POST', 'GET'])
@login_required
def list_page():
   pass

# Route thar render html tamplate page to register User in the  application
@app.route('/register', methods=['GET', 'POST'])
def register_page():
   pass
   
# Route responsible to log out the User in the application
@app.route('/logout')
def logout_page():
   pass

# Route responsible for delete the Contact. The Id of Contact is passed in url to the route
@app.route('/delete/<int:id>')
def delete_page(id):
   pass

# Route responsible to edit the details of Contant. The name of Contact is passed in url to the route
@app.route('/contacts/edit/<name>', methods=['GET', 'POST'])
def edit_contact(name):
```




