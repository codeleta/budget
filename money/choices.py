class Directions:
    INCOME = 1
    EXPENSE = -1

    CHOICES = (
        (INCOME, 'Доход'),
        (EXPENSE, 'Расход'),
    )


class Accounts:
    DEFAULT = 'default'
    STORAGE = 'storage'
    UNEXPECTED = 'unexpected'

    CHOICES = (
        (DEFAULT, 'Дефолтный'),
        (STORAGE, 'Сбережения'),
        (UNEXPECTED, 'Неожиданные траты'),
    )


class ProductTypes:
    CLOTHES = 'clothes'
    FOODSTUFF = 'foodstuff'
    REQUIRED_PERIODIC = 'required_periodic'
    BABY = 'baby'
    PLAN = 'plan'
    DEBT = 'debt'
    MEDICINE = 'medicine'
    PERSONAL = 'personal'
    GIFTS = 'gifts'
    LEISURE = 'leisure'

    CHOICES = (
        (CLOTHES, 'Одежда'),
        (FOODSTUFF, 'Продукты'),
        (REQUIRED_PERIODIC, 'Обязательные периодические'),
        (BABY, 'На Макса'),
        (PLAN, 'Запланированные траты'),
        (DEBT, 'Долги'),
        (MEDICINE, 'Медицина'),
        (PERSONAL, 'Личные'),
        (GIFTS, 'Подарки'),
        (LEISURE, 'Развлечения'),
    )
