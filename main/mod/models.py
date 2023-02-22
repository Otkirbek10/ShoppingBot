from django.db import models

class User(models.Model):
    tg_id = models.BigIntegerField(unique=True,verbose_name='Telegram ID')
    name = models.CharField(max_length=150)
    user_name = models.CharField(max_length=150,null=True,verbose_name='Tg user_name')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=150,verbose_name='Kategoriya nomi')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100,verbose_name='Product nomi')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos')
    description = models.TextField()
    price = models.DecimalField(max_digits=8,decimal_places=2)

    def __str__(self):
        return self.name

class Cart(models.Model):
    tg_id = models.IntegerField()
    product = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.product