# Contact Book

It is an application that in the first place to log in to the page you need to create a user account, After that, you be able to create contacts that will be automatically listed on your page after saving it. the user can see the details of the created contact, as well as edit it and delete contact.

### Language of Project:

- Python Flask
- HTML
- CSS
- Bootstrap
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
#class that represent web page users
class Users(db.Model, UserMixin):
   pass
   
#class that represent contact that user can creat
class Contacts(db.Model):
   pass
 

```




