from django.shortcuts import render, HttpResponse, redirect
from .models import Component, Request
from .forms import ComponenentForm, UpdateComponentForm, RequestForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from RoboClub.decorators import has_role_head_or_coordinator
from django.contrib.auth.decorators import login_required


# Create your views here.

@has_role_head_or_coordinator
def test(request, id):
    context = {}
    component = Request.objects.filter(component_id=id).filter(status=0)
    othcomp = Request.objects.filter(component_id=id).filter(status=1)
    context['component'] = Component.objects.get(pk=id)  # changed
    context['component_requests'] = component
    context['approved'] = othcomp
    return render(request, 'component/component_issue_list.html', context)


@login_required
def componentlist(request):
    context = {}
    context['components_0'] = Component.objects.filter(type=0)
    context['components_1'] = Component.objects.filter(type=1)
    context['components_2'] = Component.objects.filter(type=2)
    context['components_3'] = Component.objects.filter(type=3)
    context['components_4'] = Component.objects.filter(type=4)
    context['components_5'] = Component.objects.filter(type=5)
    context['components_6'] = Component.objects.filter(type=6)
    # context['components_7'] = Component.objects.filter(type=7)
    context['form'] = RequestForm()
    return render(request, 'component/component_list.html', context)


@has_role_head_or_coordinator
def addcomponent(request):
    context = {}
    if request.method == 'POST':
        form = ComponenentForm(request.POST, request.FILES)
        form.save()
        return redirect('component_list')
    else:
        form = ComponenentForm()
        context['form'] = form
    return render(request, 'component/component_form.html', context)


@has_role_head_or_coordinator
def deletecomponent(request, pk):
    component = Component.objects.get(pk=pk)
    component.delete()
    return redirect('component_list')


@has_role_head_or_coordinator
def updatecomponent(request, pk):
    component = Component.objects.get(pk=pk)
    context = {}
    if request.method == 'POST':
        form = UpdateComponentForm(request.POST, request.FILES, instance=component)
        form.save()
        return redirect('component_list')
    else:
        form = UpdateComponentForm(instance=component)
        context['form'] = form
    return render(request, 'component/component_form.html', context)


@has_role_head_or_coordinator
def handlerequest(request):
    context = {}
    cid = request.GET.get('id')
    user = request.GET.get('user')
    type = request.GET.get('r_type')
    status = request.GET.get('status')
    comp = Component.objects.get(pk=cid)
    user = User.objects.get(username__exact=user)
    req = Request.objects.filter(request_user=user, component=comp).first()
    if req is not None:
        if type == '0':  # approve
            req.status = 1
            add = req.request_num
            if add > comp.available():
                messages.info(request, "Not enough component!")
            else:
                req.save()
                comp.issued_num = comp.issued_num + add
                comp.save()
                messages.success(request, "Request accepted successfully")
        elif type == '1':  # reject
            req.delete()
        elif type == '2':
            add = req.request_num
            if (req.status == 1):
                comp.issued_num = comp.issued_num - add
            comp.save()
            req.delete()
        else:
            print("this should not be happening")
    if request.is_ajax():
        if status == '1':
            context['component'] = comp
            context['approved'] = Request.objects.filter(component=comp).filter(status=1)
            html = render_to_string('Component/component_issue_list_update.html', context, request=request)
        elif status == '2':
            context['components'] = Request.objects.filter(request_user=request.user)
            html = render_to_string('user/user_comp.html',context,request=request)
        else:
            context['requests'] = Request.objects.filter(status=0)
            html = render_to_string('user/admin_comp.html', context, request=request)
        return JsonResponse({'html': html}, status=200)
    else:
        return HttpResponse("This is unexpected :(")


@login_required
def createrequest(request):
    context = {}
    if request.is_ajax():
        cid = request.POST.get('cid')
        component = Component.objects.get(pk=cid)
        req_num = request.POST.get('req_num')
        reas = request.POST.get('reason')
        print(reas)
        if int(req_num) < 0:
            return JsonResponse({'request': '2'})
        if Request.objects.filter(request_user=request.user, component=component).exists():
            req = Request.objects.get(request_user=request.user, component=component)
            if req.status == 0:
                if int(req_num) > component.available():
                    messages.info(request, "Not Enough components!")
                else:
                    req.request_num = req_num
                    req.reason=reas
                    req.save()
                    messages.success(request, "Request Updated Successfully!")
            else:
                messages.info(request, "Request Already Accepted!")
        elif int(req_num) > component.available():
            messages.error(request, "Not Enough Components!")
        else:
            req = Request(request_num=req_num, request_user=request.user,reason=reas, component=component)
            req.save()
            messages.success(request, "Request Sent Successfully!")
        html = render_to_string('spinnets/message.html', context, request=request)
        return JsonResponse({'html': html}, status=200)
    else:
        return HttpResponse("woops")
