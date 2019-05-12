from django import forms

from money import choices
from money import models


class MoneyMovementForm(forms.ModelForm):

    class Meta:
        model = models.MoneyMovement
        fields = '__all__'


class PlanExpenseForm(forms.ModelForm):

    def clean(self):
        data = self.cleaned_data
        dates = {data.get('date_from'), data.get('date_to')}
        if None in dates and len(dates) != 1:
            raise forms.ValidationError('One of dates is None')
        return data

    class Meta:
        model = models.PlanExpense
        fields = '__all__'


class ExpenseForm(forms.ModelForm):

    def clean(self):
        data = self.cleaned_data
        if (
                data['product_type'] == choices.ProductTypes.PLAN and
                data.get('plan_expense') is None
        ):
            raise forms.ValidationError('need set plan_expense')
        return data

    class Meta:
        model = models.Expense
        fields = '__all__'


class ExpenseStatForm(forms.Form):

    date_from = forms.DateField()
    date_to = forms.DateField()
