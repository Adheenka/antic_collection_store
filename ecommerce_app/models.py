from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    description=models.TextField(blank=True)
    imge=models.ImageField(upload_to='category',blank=True)

    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural='categories'

    def get_url(self):
        return reverse('ecommerce_app:product_by_category',args=[self.slug])

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
        name=models.CharField(max_length=250,unique=True)
        slug=models.SlugField(max_length=250,unique=True)
        description=models.TextField(blank=True)
        price=models.DecimalField(max_digits=10,decimal_places=2)
        category=models.ForeignKey('Category',on_delete=models.CASCADE)
        imge=models.ImageField(upload_to='product',blank=True)
        stock=models.IntegerField()
        available=models.BooleanField(default=True)
        created=models.DateTimeField(auto_now_add=True)
        updated=models.DateTimeField(auto_now=True)
        def get_url(self):
            return reverse('ecommerce_app:prodCatdetail',args=[self.category.slug,self.slug])


        class Meta:
            ordering=('name',)
            verbose_name='product'
            verbose_name_plural='products'

        def __str__(self):
            return '{}'.format(self.name)

class Wishlist(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)

