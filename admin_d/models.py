from djongo.models import Model, ObjectIdField, CharField, FloatField, ForeignKey, TextField, DateField, BooleanField, JSONField, SlugField, IntegerField
from django.db.models import CASCADE


class Admin(Model):
    _id = ObjectIdField()
    username = CharField(max_length=100)
    password = CharField(max_length=128)

class email(Model):
    _id = ObjectIdField()
    email_id = CharField(max_length=100)
    app_pass = CharField(max_length=100)
    updated_date = DateField(auto_now_add=True)

class telegram_cr(Model):
    _id = ObjectIdField()
    name = CharField(max_length=100)
    bot_cr = CharField(max_length=100)
    channel_cr = CharField(max_length=100)  

class banner(Model):
    _id = ObjectIdField()
    name = CharField(max_length=100)
    image = CharField(max_length=100)

class n_category(Model):
    _id = ObjectIdField()
    name = CharField(max_length=100)
    image = CharField(max_length=100)
    description = TextField(default='')
    visibility_status = CharField(max_length=100)
    url_key = CharField(max_length=100)
    meta_title = CharField(max_length=100)  
    meta_keyword = CharField(max_length=100)
    meta_description = CharField(max_length=100)  
    created_date = DateField(auto_now_add=True)

class N_collection(Model):
    _id = ObjectIdField()
    name = CharField(max_length=100)
    slug = SlugField(unique=True)
    description = TextField(blank=True, null=True)
    image = CharField(max_length=100)
    is_active = BooleanField(default=True)
    created_date = DateField(auto_now_add=True)

class N_product(Model):
    _id = ObjectIdField()
    name = CharField(max_length=100)
    category = ForeignKey(n_category, on_delete=CASCADE)
    collection = ForeignKey(N_collection, on_delete=CASCADE)
    price = CharField(max_length=100)
    f_price = CharField(max_length=100)
    patterns = CharField(max_length=100)
    Pocket = CharField(max_length=10)
    fabric = CharField(max_length=100)
    hight = CharField(max_length=100)
    sleeves = CharField(max_length=100)
    wash_car = CharField(max_length=100)
    description = TextField(default='')
    image = CharField(max_length=100)
    free_delivery = CharField(max_length=10)
    visibility = CharField(max_length=20)
    url_key = CharField(max_length=100, unique=True)
    meta_title = CharField(max_length=60)
    meta_keywords = CharField(max_length=255)
    meta_description = CharField(max_length=160)
    created_date = DateField(auto_now_add=True)
    variants = JSONField()

class N_coupon(Model):
    _id = ObjectIdField()
    code = CharField(max_length=50, unique=True)
    description = TextField(blank=True, null=True)

    # Status toggle
    is_active = BooleanField(default=True)

    # Discount fields
    discount_type = CharField(max_length=50, choices=[
        ('fixed_order', 'Fixed discount to entire order'),
        ('percent_order', 'Percentage discount to entire order'),
        ('fixed_product', 'Fixed discount to specific products'),
        ('percent_product', 'Percentage discount to specific products'),
        ('bxgy', 'Buy X get Y')
    ])
    discount_value = FloatField()

    # Date range
    start_date = DateField()
    end_date = DateField()

    # Free shipping
    free_shipping = BooleanField(default=False)

class home_page(Model):
    _id = ObjectIdField()
    collection_name = ForeignKey(N_collection, on_delete=CASCADE)
    Tagline = CharField(max_length=100)
    position = IntegerField()
    created_date = DateField(auto_now_add=True)

class footer(Model):
    _id = ObjectIdField()
    qotes = CharField(max_length=100)
    quotes = CharField(max_length=100)
    em = CharField(max_length=100)
    phone_no = CharField(max_length=100)
    email_id = CharField(max_length=100)
    fb = CharField(max_length=100)
    insta = CharField(max_length=100)
    youtube = CharField(max_length=100)
    whatsapp = CharField(max_length=100)
    wno = CharField(max_length=100)
