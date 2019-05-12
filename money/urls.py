from django.urls import path

from money.views import create_views
from money.views import info_views

urlpatterns = [
    path('', info_views.IndexView.as_view(), name='index'),
    path('statistic/', info_views.StatisticView.as_view(), name='statistic'),
    path('plans/', info_views.PlanView.as_view(), name='plans'),

    path(
        'create/money-movement/',
        create_views.MoneyMovementCreateView.as_view(),
        name='create_money_movement',
    ),
    path(
        'create/plan/',
        create_views.PlanExpenseCreateView.as_view(),
        name='create_plan',
    ),
    path(
        'create/expense/',
        create_views.ExpenseCreateView.as_view(),
        name='create_expense',
    ),
]