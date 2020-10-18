from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model

# Хотим использовать юзера который указан в
User = get_user_model()


class Customer(models.Model):
    """Покупатель"""
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)


class Meta:
    verbose_name = "Customer"
    verbose_name_plural = "Customers"


def __str__(self):
    return f'Покупатель {self.user.first_name} {self.user.last_name}'


class Category(models.Model):
    """
    Категория продукта
    """
    name = models.CharField(max_length=50, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Абстрактная модель - продукт
    """
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class CartProduct(models.Model):
    """Продукты в корзине"""
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Покупатель')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='related_products', )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return f"Продукт: {self.content_object.title} (для корзины)"


class Cart(models.Model):
    """Корзина"""
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Владелец')
    product = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return str(self.id)


class NoteBook(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ', )
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея', )
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора', )
    ram = models.CharField(max_length=255, verbose_name='Оперативная память', )
    video = models.CharField(max_length=255, verbose_name='Видеокарта', )
    time_without_charge = models.CharField(max_length=255, verbose_name='Время работы аккумулятора', )

    def __str__(self):
        return f'{self.category.name} : {self.title}'


class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    accum_volume = models.CharField(max_length=255, verbose_name='Объем батареи')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    sd = models.BooleanField(default=True, verbose_name='Наличие SD карты')
    sd_volume_max = models.CharField(max_length=255, null=True, blank=True, verbose_name='Объем SD памяти')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)
