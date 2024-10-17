from django.db import models
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, verbose_name='category')
    name = models.CharField(max_length=255, verbose_name='name product')
    slug = models.SlugField(max_length=255, verbose_name='slug')
    description = models.TextField(max_length=1200, verbose_name='product info')
    inventory = models.PositiveIntegerField(default=0, verbose_name='inventory')
    price = models.PositiveIntegerField(default=0, verbose_name='price')
    weight = models.PositiveIntegerField(default=0, verbose_name='weight')
    off = models.PositiveIntegerField(default=0, verbose_name='off')
    new_price = models.PositiveIntegerField(default=0, verbose_name="new price")
    created = models.DateTimeField(auto_now_add=True, verbose_name='created time')
    updated = models.DateTimeField(auto_now=True, verbose_name='updated time')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class ProductFeature(models.Model):
    name = models.CharField(max_length=255, verbose_name='features')
    value = models.CharField(max_length=255, verbose_name='values features')
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE, verbose_name='products')

    def __str__(self):
        return self.name + ':' + self.value


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="product")
    file = models.ImageField(upload_to="product_images/%Y/%m/%d")
    title = models.CharField(max_length=250, verbose_name="title", null=True, blank=True)
    description = models.TextField(verbose_name="description", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = "image"
        verbose_name_plural = "images"
