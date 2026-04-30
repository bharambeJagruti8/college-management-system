from django.shortcuts import render
from django.shortcuts import render,redirect
from .models import FeeRecord
from .forms import FeeForm

def manage_fees(request):
    fees = FeeRecord.objects.all()
    return render(request,'fees/manage_fees.html',{'fees':fees})


def add_fee(request):
    if request.method == "POST":
        form = FeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_fees')
    else:
        form = FeeForm()

    return render(request,'fees/add_fee.html',{'form':form})
# Create your views here.
