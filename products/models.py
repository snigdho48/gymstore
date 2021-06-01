from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=250)
    friendly_name = models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('product_detail', args=[self.friendly_name])

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    sku = models.CharField(max_length=250, blank=True)
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    has_sizes = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
