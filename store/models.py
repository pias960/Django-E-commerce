from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from login.models import *
from django.core import validators
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False )
    image = models.ImageField(upload_to='category', blank=True, null =True)
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', related_name= 'children', on_delete= models.CASCADE, blank=True, null = True )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Categories'




class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False )
    category= models.ForeignKey(Category, on_delete =models.CASCADE, related_name='category')
    image = models.ImageField(upload_to='products', blank=False, null =False)
    sort_des = models.CharField(max_length =100, null= False,blank=False )
    description = models.TextField(max_length=1000, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    slug = models.SlugField(unique=True)
    old_price = models.FloatField(blank =True, null=True )
    is_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Products'

    def get_product_url(self):
        return reverse('product_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
       if not self.slug:
           self.slug = slugify(self.name)
       return super(Product, self).save(*args, **kwargs)

class ProductImage(models.Model):
    image = models.ImageField(upload_to='image_gallery', blank=True, null =True, )
    product = models.ForeignKey(Product, on_delete =models.CASCADE, related_name='product_image')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Carts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, on_delete =models.CASCADE, related_name='carts')
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username




class Banner(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name='banner')
    image = models.ImageField(upload_to='banner', blank=True, null =True)
    is_active = models.BooleanField(default=True),
    created = models.DateTimeField(auto_now_add=True),

    def __str__(self):
        return f"{self.product.name} Banner"

class BillingDetails(models.Model):

    first_name = models.TextField(validators=[validators.MaxLengthValidator(10)])
    last_name = models.TextField(validators=[validators.MaxLengthValidator(10)])
    street_address = models.CharField(max_length=255)
    town_city = models.CharField(max_length=10)
    postcode_zip = models.CharField(max_length=8)
    notes = models.TextField(max_length=500)
    phone = models.CharField(max_length=11)


    def __str__(self):
        return f"{self.first_name}informations --- Details No: {self.id} "

class Orders(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, related_name='orders' , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        default='proccesing',
        max_length=20,
        choices=[
            ('proccesing', 'Proccesing'),
            ('parcel', 'Parceled'),
            ('on the way', 'On the way'),
            ('delivered', 'Delivered'),
             ('cancaled', 'Cancaled'),
        ]
    )

    order = models.ForeignKey(BillingDetails, on_delete=models.CASCADE)

    def __str__(self):
        return f" Order No:{self.id} -- Order by -> {self.user.username} -- Billing Details No : { self.order.id } "
    class Meta:
        ordering = ['-created']
    @property
    def get_total_price(self):
        piash = 150
        pias = self.product.price * self.quantity
        im = piash + pias
        return im




