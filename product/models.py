from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Review(models.Model):
    text = models.TextField(null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='reviews')

    def __str__(self):
        return self.text
