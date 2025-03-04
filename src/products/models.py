from django.db import models

from users.models import User

SIZE_CHOICES = [
    ('?', 'Unknown'),
    ('XXS', 'XXS (38-40)'),
    ('XS', 'XS (40-42)'),
    ('S', 'S (44-46)'),
    ('M', 'M (46-48)'),
    ('L', 'L (48-50)'),
    ('XL', 'XL (50-52)'),
    ('XXL', 'XXL (52-54)'),
    ('XXXL', 'XXXL (54-56)'),
]

GENDER_CHOICES = [
    ('M', 'Мужское'),
    ('F', 'Женское'),
]


class ProductCategory(models.Model):
    name = models.CharField(max_length=31, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    size = models.CharField(max_length=15, choices=SIZE_CHOICES, default='Unknown')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    reservation = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'
        ordering = ['id']

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name}'


class ProductImage(models.Model):
    image = models.ImageField(upload_to='gallery')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='img')


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.email} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

    def first_img(self):
        first_img = self.product.img.first()
        return first_img.image.url if first_img else None
