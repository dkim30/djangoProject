from django.db import models
import re, bcrypt
from datetime import datetime, date

class UserManager(models.Manager):
    def register(self,data):
        errors = {}

        if len(data['name']) < 1:
            errors['name'] = "Your must enter a name"
        elif len(data['name']) < 3:
            errors['name'] = "Your name must be 3 characters or more"
        if len(data['username']) < 1:
            errors['username'] = "Your must enter a username"
        elif len(data['username']) < 3:
            errors['username'] = "Your username must be 3 characters or more"
        if len(data['password']) < 1:
            errors['password'] = "You must enter a password"
        elif len(data['password']) < 8:
            errors['password'] = "Your password must be 8 characters or longer"
        if data['password'] != data['confirm_password']:
            errors['confirm_password'] = "The password does not match"
        if len(data['date']) < 1:
            errors['date'] = "You must enter a date hired"
        else:
            d = datetime.strptime(data['date'],"%Y-%m-%d")
            if d > datetime.now():
                errors['date'] = "You cannot be hired from the future"
        if len(errors) == 0:
            return User.objects.create(
                name = data['name'],
                username = data['username'],
                date = data['date'],
                password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
            )
        else:
            return errors

    def login(self,data):
        errors = {}

        if len(data['username']) < 1:
            errors['username'] = "Username is required"
        elif len(data['username']) < 3:
            errors['username'] = "Your username must be 3 characters or more"
        else:
            list_of_users_with_this_username = User.objects.filter(username=data['username'])
            if len(list_of_users_with_this_username) < 1:
                errors['username'] = "Username is not in use"
        if len(data['password']) < 8:
            errors['password'] = "Password must be 8 characters or longer"
        
        if len(errors) == 0:
            stored_password = list_of_users_with_this_username[0].password
            if not bcrypt.checkpw(data['password'].encode(), stored_password.encode()):
                errors['password'] = "Incorrect Password"
                return errors
            else: 
                return list_of_users_with_this_username[0]
        else:
            return errors

        



class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    date = models.CharField(max_length = 10)

    objects = UserManager()


class WishManger(models.Manager):
    def add_item(self, data, user_id):
        print(data)
        if len(data["item"]) < 3:
            return {"item": "Item must be 3 or more characters long"}
        else:
            return Wish.objects.create(
                item = data['item'],
                user_id = user_id
            )

class Wish(models.Model):
    item = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="wishes", on_delete = models.CASCADE)
    favs = models.ManyToManyField(User, related_name="wish_list")

    objects = WishManger()

