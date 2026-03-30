from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Choices for Income
INCOME_CHOICES = [
    ('salary', 'Salary'),
    ('freelance', 'Freelancing'),
    ('business', 'Business'),
    ('investment', 'Investment'),
    ('gift', 'Gift'),
    ('other', 'Other'),
]

# Choices for Expense
EXPENSE_CHOICES = [
    ('food', 'Food & Dining'),
    ('rent', 'Rent'),
    ('travel', 'Travel'),
    ('shopping', 'Shopping'),
    ('bills', 'Bills & Utilities'),
    ('health', 'Healthcare'),
    ('education', 'Education'),
    ('entertainment', 'Entertainment'),
    ('other', 'Other'),
]


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=50, choices=INCOME_CHOICES)
    amount = models.FloatField()
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} - {self.amount}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=EXPENSE_CHOICES)
    amount = models.FloatField()
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"