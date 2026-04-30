from django.shortcuts import render,redirect
from dashboard.models import FeeRecord


def manage_fees(request):
    fees = FeeRecord.objects.all()
    return render(request,'fees/manage_fees.html',{'fees':fees})


def add_fee(request):
    if request.method == "POST":
        form = FeeRecord(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_fees')
    else:
        form = FeeRecord()

    return render(request,'fees/add_fee.html',{'form':form})