from djongo.models import Model, ObjectIdField, CharField, FloatField, ForeignKey, TextField, DateField, BooleanField, JSONField, SlugField, IntegerField
from django.db.models import CASCADE


class user_ID(Model):
    _id = ObjectIdField()
    username = CharField(max_length=100)
    password = CharField(max_length=128)
    email = CharField(max_length=100)

class Order(Model):
    _id = ObjectIdField()
    user_id = ForeignKey(user_ID, on_delete=CASCADE)
    items = JSONField()  # Store the cart as JSON
    total = FloatField()
    created_at = DateField(auto_now_add=True)
    status = CharField(max_length=20, default="Pending")
    copun_code = CharField(max_length=20,  default="")

    def __str__(self):
        return f"Order #{self.id} - User {self.user_id}"

class address(Model):  
    _id = ObjectIdField()
    user_id = ForeignKey(user_ID, on_delete=CASCADE)
    name = CharField(max_length=100)
    phone = CharField(max_length=15)
    street = CharField(max_length=200)
    city = CharField(max_length=100)
    state = CharField(max_length=100)
    zipcode = CharField(max_length=10)
    country = CharField(max_length=50, default="India")