from django import urls
from django.contrib import messages
from django.views import generic


class PlanExpenseUpdateView(generic.UpdateView):
    success_url = urls.reverse_lazy('plans')

    def form_valid(self, form):
        messages.info(self.request, 'MoneyMovement object created')
        return super().form_valid(form)
