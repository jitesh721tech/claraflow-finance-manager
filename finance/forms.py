from django import forms
from .models import Income, Expense

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'amount', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Please enter valid amount")
        return amount


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Please enter valid amount")
        return amount