from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import BonafideRequest

@login_required
def bonafide_index(request):
    if request.method == 'POST':
        purpose = request.POST.get('purpose')
        addressed_to = request.POST.get('addressed_to')
        note = request.POST.get('note', '')

        if purpose and addressed_to:
            BonafideRequest.objects.create(
                student=request.user,
                purpose=purpose,
                addressed_to=addressed_to,
                note=note
            )
            messages.success(request, 'Request submitted successfully!')
            return redirect('bonafide:index')
        else:
            messages.error(request, 'Please fill all required fields.')

    requests_list = BonafideRequest.objects.filter(student=request.user)
    context = {
        'requests_list': requests_list,
        'purpose_choices': BonafideRequest.PURPOSE_CHOICES,
    }
    return render(request, 'bonafide/bonafide.html', context)


@staff_member_required
def admin_bonafide(request):
    all_requests = BonafideRequest.objects.all()
    context = {'all_requests': all_requests}
    return render(request, 'bonafide/admin_bonafide.html', context)


@staff_member_required
def update_status(request, request_id):
    bon_request = get_object_or_404(BonafideRequest, id=request_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['approved', 'rejected']:
            bon_request.status = status
            bon_request.save()
            messages.success(request, f'Request {status} successfully!')
    return redirect('bonafide:admin_bonafide')