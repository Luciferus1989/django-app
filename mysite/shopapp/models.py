from django.contrib.auth.models import User
from django.db import models


def product_preview_directory_path(instance: 'Product', filename: str) -> str:
    return 'products/product_{pk}/preview/{filename}'.format(pk=instance.pk, filename=filename)


class Product(models.Model):
    """
    Model Product show products which can be sold in shop.

    Orders here: :model:`shopapp.Order`
    """
    class Meta:
        ordering = ['name', 'price']

    name = models.CharField(max_length=100, db_index=True, verbose_name='name of product')
    description = models.TextField(null=False, blank=True, db_index=True, verbose_name='description of product')
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='price of product')
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)

    # @property
    # def description_short(self) -> str:
    #     if len(self.description) < 10:
    #         return self.description
    #     return self.description[:10] + '...'

    @property
    def discount_short(self) -> str:
        if self.discount:
            return self.discount
        return '...'

    def __str__(self) -> str:
        return self.name


def product_image_directory_path(instance: 'ProductImage', filename: str) -> str:
    return 'products/product_{pk}/images/{filename}'.format(pk=instance.product.pk,
                                                            filename=filename,)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_directory_path)
    description = models.CharField(max_length=100, null=False, blank=True,)

class Order(models.Model):
    """
    Model Order is presented by orders which is created by users
    """
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')
    receipt = models.FileField(null=True, upload_to='orders/receipts')
