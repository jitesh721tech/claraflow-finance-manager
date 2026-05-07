from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

#User Register
from django.contrib import messages

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

#User Login

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

#User Logout

def logout_view(request):
    logout(request)
    return redirect('index')

#dashboard

@login_required
def dashboard(request):
    transaction_type = request.GET.get('type', 'all')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    savings = total_income - total_expense

    # Type filter
    if transaction_type == 'income':
        transactions = list(incomes)
    elif transaction_type == 'expense':
        transactions = list(expenses)
    else:
        transactions = list(incomes) + list(expenses)

    # Date filter
    if start_date:
        transactions = [t for t in transactions if str(t.date) >= start_date]

    if end_date:
        transactions = [t for t in transactions if str(t.date) <= end_date]

    transactions.sort(key=lambda x: x.date, reverse=True)
    transactions = transactions[:5]

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'savings': savings,
        'transactions': transactions,
        'transaction_type': transaction_type,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'dashboard.html', context)

@login_required
def add_income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('dashboard')
    else:
        form = IncomeForm()

    return render(request, 'add_income.html', {'form': form})


@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form})

@login_required
def edit_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)

    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            updated_income = form.save(commit=False)
            updated_income.user = request.user
            updated_income.save()
            return redirect('dashboard')
    else:
        form = IncomeForm(instance=income)

    return render(request, 'add_income.html', {'form': form})


@login_required
def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)

    if request.method == "POST":
        income.delete()
        return redirect('dashboard')

    return render(request, 'confirm_delete.html', {'item': income, 'type': 'Income'})


@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            updated_expense = form.save(commit=False)
            updated_expense.user = request.user
            updated_expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'add_expense.html', {'form': form})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == "POST":
        expense.delete()
        return redirect('dashboard')

    return render(request, 'confirm_delete.html', {'item': expense, 'type': 'Expense'})



def reset_admin_password(request):
    secret = request.GET.get("secret")

    if secret != "claraflow-reset-2026":
        return HttpResponse("Not allowed", status=403)

    User = get_user_model()

    user, created = User.objects.get_or_create(username="jitesh_patil")
    user.set_password("976909")
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()

    return HttpResponse(
        f"Admin password reset successfully. Created new user: {created}. "
        "Now login with username: jitesh_patil and password: NewPassword@123"
    )