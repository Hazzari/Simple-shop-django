from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model

# Хотим использовать юзера который указан в
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Покупатель')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='related_products', verbose_name='Корзина')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Общая цена')

    class Meta:
        abstract = True

    def __str__(self):
        return f'Продукт: {self.product.title} (Для корзины)'


class Cart(models.Model):
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Владелец')
    product = models.ManyToManyField('CartProduct', blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Окончательная цена')

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return self.id


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f'Покупатель {self.user.first_name} {self.user.last_name}'
