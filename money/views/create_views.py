from django import urls
from django.contrib import messages
from django.views import generic

from money import forms
from money import models


class MoneyMovementCreateView(generic.CreateView):
    model = models.MoneyMovement
    form_class = forms.MoneyMovementForm
    success_url = urls.reverse_lazy('create_money_movement')
    template_name = 'money/create_money_movement.html'

    def form_valid(self, form):
        messages.info(self.request, 'MoneyMovement object created')
        return super().form_valid(form)


class PlanExpenseCreateView(generic.CreateView):
    model = models.PlanExpense
    form_class = forms.PlanExpenseForm
    success_url = urls.reverse_lazy('create_plan')
    template_name = 'money/create_plan.html'

    def form_valid(self, form):
        messages.info(self.request, 'PlanExpense object created')
        return super().form_valid(form)


class ExpenseCreateView(generic.CreateView):
    model = models.Expense
    form_class = forms.ExpenseForm
    success_url = urls.reverse_lazy('create_expense')
    template_name = 'money/create_expense.html'

    def form_valid(self, form):
        messages.info(self.request, 'Expense object created')
        return super().form_valid(form)
