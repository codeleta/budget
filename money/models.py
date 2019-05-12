import datetime

from django.db import models

from money import choices
from money import managers


class MoneyMovement(models.Model):

    date = models.DateField(default=datetime.date.today)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    direction = models.SmallIntegerField(
        choices=choices.Directions.CHOICES,
        default=choices.Directions.EXPENSE,
    )
    account = models.CharField(
        choices=choices.Accounts.CHOICES,
        default=choices.Accounts.DEFAULT,
        max_length=10,
    )
    receipt_photo = models.ImageField(
        upload_to='money/receipts/%Y/%m/%d/',
        null=True,
        blank=True,
    )
    comment = models.TextField(blank=True)

    objects = managers.MoneyMovementManager()

    class Meta:
        ordering = ('date', )

    def __str__(self):
        return f'Чек на сумму {self.direction}*{self.amount} от {self.date}'


class PlanExpense(models.Model):

    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True,
    )
    is_bought = models.BooleanField(default=False)
    comment = models.TextField(blank=True)

    objects = managers.PlanExpenseManager()

    class Meta:
        ordering = ('date_from', )


class Expense(models.Model):

    movement = models.ForeignKey(
        to=MoneyMovement,
        on_delete=models.deletion.PROTECT,
    )
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    product_name = models.CharField(max_length=255)
    product_type = models.CharField(
        max_length=30, choices=choices.ProductTypes.CHOICES,
    )
    plan_expense = models.ForeignKey(
        to=PlanExpense,
        on_delete=models.deletion.PROTECT,
        null=True,
        blank=True,
    )
    wasted = models.BooleanField(default=False)
    comment = models.TextField(blank=True)

    objects = managers.ExpenseManager()

    class Meta:
        ordering = ('movement__date', )
