from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
from .models import *
from .forms import *
from django import http
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
@login_required(login_url='/login')
def home(request):
    if request.user.reporter.first_use:
        return redirect('/newuser')
    issues_list = Issue.objects.all().order_by('-create_time')
    paginator = Paginator(issues_list, 10)
    page = request.GET.get('page')
    try:
        issues = paginator.page(page)
    except PageNotAnInteger:
        issues = paginator.page(1)
    except EmptyPage:
        issues = paginator.page(paginator.num_pages)
    context = {
        'user':request.user,
        'issues':issues
    }
    return render(request, 'home.html', context)

@login_required(login_url='/login')
def signout(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def newuser(request):
    form = PasswordForm()
    context = {
        'form':form,
        'error':''
    }
    return render(request, 'newuser.html', context)

@login_required(login_url='/login')
def validate_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if form.cleaned_data['password'] == form.cleaned_data['conf_password']:
                user.set_password(form.cleaned_data['password'])
                user.reporter.first_use = False
                user.reporter.save()
                return redirect('/home')
            else:
                context = {
                    'form':form,
                    'error':'passwords dont match'
                }
                return render(request, 'newuser.html', context)
        else:
            return redirect('/newuser')

@login_required(login_url='/login')
def add(request):
    if request.method == 'POST':
        f = IssueForm(request.POST)
        if f.is_valid():
            print('valid')
            issue = Issue()
            issue.title = f.cleaned_data['title']
            issue.description = f.cleaned_data['description']
            issue.platform = f.cleaned_data['platform']
            issue.reporter = request.user.reporter
            issue.save()
            return redirect('/home/')
    form = IssueForm()
    return render(request, 'add.html', {'form':form})

@login_required(login_url='/login')
def detail_issue(request,pk):
    issue = Issue.objects.get(pk=pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            ctext = form.cleaned_data['text']
            cmt = Comment.objects.create(text=ctext, issue=issue, reporter=request.user.reporter)
            cmt.save()
            form = CommentForm()
            context = {
                'issue':issue,
                'form':form
            }
            return render(request, 'issue-detail.html', context)
    form = CommentForm()
    context = {
        'issue':issue,
        'form':form
    }
    print(issue.reporter.is_admin)
    return render(request, 'issue-detail.html', context)

@login_required(login_url='/login')
def edit_issue(request,pk):
    if not request.user.reporter.is_admin:
        return redirect('/home')
    issue = Issue.objects.get(pk=pk)
    if request.method == 'POST':
        form = IssueEditForm(request.POST)
        if form.is_valid():
            issue.kind = form.cleaned_data['kind']
            issue.stage = form.cleaned_data['stage']
            issue.criticality = form.cleaned_data['criticality']
            issue.save()
            return redirect('/issue/'+str(pk))
    form = IssueEditForm(instance=issue)
    context = {
            'form':form,
            'issue':issue
        }    
    return render(request, 'edit-issue.html', context)

