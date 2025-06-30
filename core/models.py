from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User


class Contact(models.Model):
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street}, {self.house_number}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class Product(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    release_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.model})"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class NetworkNode(models.Model):
    FACTORY = 0
    RETAIL = 1
    ENTREPRENEUR = 2

    NODE_TYPES = (
        (FACTORY, 'Завод'),
        (RETAIL, 'Розничная сеть'),
        (ENTREPRENEUR, 'Индивидуальный предприниматель'),
    )

    name = models.CharField(max_length=100, unique=True)
    node_type = models.PositiveSmallIntegerField(choices=NODE_TYPES)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )
    debt = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    @property
    def hierarchy_level(self):
        if self.node_type == self.FACTORY:
            return 0
        if self.supplier is None:
            return 0
        return self.supplier.hierarchy_level + 1

    def __str__(self):
        return f"{self.get_node_type_display()}: {self.name}"

    class Meta:
        verbose_name = "Элемент сети"
        verbose_name_plural = "Элементы сети"
        ordering = ['-created_at']


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    network_node = models.ForeignKey(NetworkNode, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} ({self.network_node.name})"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
