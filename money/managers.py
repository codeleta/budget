import datetime
import decimal
from typing import Dict
from typing import Optional

from django.db import models

from money import choices

BALANCE_START_DAY = 20


def _get_month(date, direction):
    month_to = date.month + direction
    year_to = date.year
    if month_to < 0:
        month_to = 12
        year_to -= 1
    elif month_to > 12:
        month_to = 1
        year_to += 1
    return datetime.date(year_to, month_to, 1)


def _get_balance_period(date: datetime.date):
    if date.day >= BALANCE_START_DAY:
        start_month = date
        end_month = _get_month(date, direction=1)
    else:
        start_month = _get_month(date, direction=-1)
        end_month = date
    date_from = datetime.date(
        start_month.year, start_month.month, BALANCE_START_DAY
    )
    date_to = datetime.date(
        end_month.year, end_month.month, BALANCE_START_DAY
    )
    return date_from, date_to


class MoneyMovementManager(models.Manager):

    @staticmethod
    def _is_weekend(day: datetime.date):
        return day.weekday() > 4

    def get_balance(self, account: Optional[str] = None):
        month_ago = datetime.date.today() - datetime.timedelta(days=31)
        qs = super().get_queryset().filter(date__gte=month_ago)
        if account is not None:
            qs = qs.filter(account=account)
        return qs.annotate(
            item_balance=models.F('amount') * models.F('direction'),
        ).aggregate(balance=models.Sum(
            'item_balance',
            output_field=models.DecimalField()
        ))['balance'] or 0

    def get_accounts_balance(self):
        accounts = {}
        for choice in choices.Accounts.CHOICES:
            accounts[choice[1]] = self.get_balance(choice[0])
        return accounts

    def get_daily_history(self, date: datetime.date, direction=None):
        qs = super().get_queryset().filter(date=date)
        if direction:
            qs = qs.filter(direction=direction)
        return qs

    def get_max_daily_expense_amount(self):
        balance = self.get_balance(account=choices.Accounts.DEFAULT)
        today = datetime.date.today()
        daily_expenses = self.get_daily_history(today).filter(
            direction=choices.Directions.EXPENSE,
        )
        today_expense = daily_expenses.aggregate(expense=models.Sum('amount'))
        today_expense = today_expense['expense'] or 0
        yesterday_balance = balance + today_expense
        date_to = _get_balance_period(today)[1]
        day = today
        count_days = 0
        while day < date_to:
            # В выходные траты в два раза больше будних
            inc_days = 2 if self._is_weekend(day) else 1
            count_days += inc_days
            day += datetime.timedelta(days=1)
        daily_max_expense_amount = yesterday_balance / count_days
        if self._is_weekend(today):
            daily_max_expense_amount *= 2
        return daily_max_expense_amount

    def get_unfilled_expense_days(self):
        viewed_days = 31
        today = datetime.date.today()
        month_ago = today - datetime.timedelta(days=viewed_days)
        qs = super().get_queryset().filter(
            direction=choices.Directions.EXPENSE,
            date__gte=month_ago,
            date__lt=today
        )
        filled_days = set(qs.values_list('date', flat=True))
        unfilled_days = []
        if len(filled_days) == viewed_days:
            return unfilled_days
        day = month_ago
        while day < today:
            if day not in filled_days:
                unfilled_days.append(day)
            day += datetime.timedelta(days=1)
        return unfilled_days


class PlanExpenseManager(models.Manager):

    def get_for_month(self, year=None, month=None):
        if year is None and month is None:
            date = datetime.date.today()
        else:
            date = datetime.date(year, month, 1)
        date_from, date_to = _get_balance_period(date)
        qs = super().get_queryset()
        qs = qs.filter(date_from__lt=date_to, date_to__gte=date_from)
        return qs

    def get_expired(self):
        date_from = _get_balance_period(datetime.date.today())[0]
        return super().get_queryset().filter(date_to__lt=date_from)

    def get_indefinites(self):
        qs = super().get_queryset()
        return qs.filter(date_from__isnull=True, date_to__isnull=True)

    def get_monthly(self):
        date_from = _get_balance_period(datetime.date.today())[0]
        qs = super().get_queryset()
        qs = qs.filter(date_from__isnull=False, date_to__isnull=False)
        qs = qs.filter(date_to__gte=date_from)
        return qs


class ExpenseManager(models.Manager):

    def get_statistic(
            self, date_from, date_to,
    ) -> Dict[str, Dict[str, decimal.Decimal]]:
        qs = super().get_queryset().select_related('movement')
        qs = qs.filter(
            movement__direction=choices.Directions.EXPENSE,
            movement__date__gte=date_from,
            movement__date__lte=date_to,
            movement__account=choices.Accounts.DEFAULT,
        )
        stat = {
            'wasted': {},
            'nonwasted': {},
        }
        for item in qs:
            stat_key = 'wasted' if item.wasted else 'nonwasted'
            stat[stat_key].setdefault(item.product_type, decimal.Decimal(0))
            stat[stat_key][item.product_type] += item.amount
        return stat
