from typing import Optional

from django.views import generic

from money import forms
from money import models


class IndexView(generic.TemplateView):
    template_name = 'money/index.html'

    def get_context_data(self, **kwargs):
        max_spend = models.MoneyMovement.objects.get_max_daily_expense_amount()
        accounts_balance = models.MoneyMovement.objects.get_accounts_balance()
        unfilled_days = models.MoneyMovement.objects.get_unfilled_expense_days()
        month_plans = models.PlanExpense.objects.get_for_month()
        kwargs.update({
            'max_spend': max_spend,
            'accounts_balance': accounts_balance,
            'unfilled_days': unfilled_days,
            'month_plans': month_plans,
        })
        return super().get_context_data(**kwargs)


class PlanView(generic.TemplateView):
    template_name = 'money/plans.html'

    def get_context_data(self, **kwargs):
        expired_plans = models.PlanExpense.objects.get_expired()
        indefinite_plans = models.PlanExpense.objects.get_indefinites()
        monthly_plans = models.PlanExpense.objects.get_monthly()
        kwargs.update({
            'expired_plans': expired_plans,
            'indefinite_plans': indefinite_plans,
            'monthly_plans': monthly_plans,
        })
        return super().get_context_data(**kwargs)


class StatisticView(generic.FormView):
    template_name = 'money/statistic.html'
    form_class = forms.ExpenseStatForm

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        form: Optional[forms.ExpenseStatForm] = kwargs.get('form')
        if form and form.is_valid():
            kwargs.update(models.Expense.objects.get_statistic(
                form.cleaned_data['date_from'],
                form.cleaned_data['date_to'],
            ))
        return super().get_context_data(**kwargs)
