from django.shortcuts import render, redirect
from .models import *
from .forms import ProjectForm, AddReview
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def projects(request):
    search_phrase = ''

    if request.GET.get('search'):
        search_phrase = request.GET.get('search')

    tags_query = Tag.objects.filter(tag__icontains=search_phrase)
    projects_query = Project.objects.distinct().filter(Q(name__icontains=search_phrase) |
                                                       Q(description__icontains=search_phrase) |
                                                       Q(tags__in=tags_query))

    paginator = Paginator(projects_query, 1)
    page = request.GET.get('page')
    try:
        projects_query = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects_query = paginator.page(page)
    except EmptyPage:
        page = paginator.count
        projects_query = paginator.page(page)

    left_index = int(page) - 2 if int(page) - 2 > 0 else 1
    right_index = int(page) + 3 if int(page) + 3 <= paginator.count else paginator.count + 1
    custom_range = range(left_index, right_index)

    context = {
        'projects': projects_query,
        'search_phrase': search_phrase,
        'custom_range': custom_range,
        'paginator': paginator
    }
    return render(request, 'projects/projects.html', context=context)


def project(request, pk):
    form = AddReview()
    if request.method == "POST":
        form = AddReview(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = Project.objects.get(pk=pk)
            review.author = request.user.profile
            review.save()
            messages.success(request, 'review was successfully added')
            return redirect('project', pk=pk)
    context = {
        'project': Project.objects.get(pk=pk),
        'reviews': Review.objects.filter(project__id=pk),
        'tags': Project.objects.get(pk=pk).tags.all(),
        'form': form,
        'positive_rate': round(len(Project.objects.get(pk=pk).review_set.filter(vote='up')) / len(Project.objects.get(pk=pk).review_set.all()) * 100) if Project.objects.get(pk=pk).review_set.all() else 0
    }
    return render(request, 'projects/project.html', context=context)


@login_required(login_url='login')
def add_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user.profile
            obj.save()
            messages.success(request, 'project was successfully added')
            return redirect('project', pk=obj.id)
    context = {'form': form}
    return render(request, 'projects/add_project.html', context)


@login_required(login_url='login')
def edit_project(request, pk):
    if Project.objects.get(pk=pk).author.id != request.user.profile.id:
        return redirect('project', pk=pk)
    form = ProjectForm(instance=Project.objects.get(id=pk))
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=Project.objects.get(id=pk))
        if form.is_valid():
            form.save()
            messages.success(request, 'project was successfully changed')
            return redirect('project', pk=pk)
    context = {'form': form}
    return render(request, 'projects/edit_project.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    if Project.objects.get(pk=pk).author.id != request.user.profile.id:
        return redirect('project', pk=pk)
    obj = Project.objects.get(id=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'user was successfully deleted')
        return redirect('projects')
    return render(request, 'projects/delete_project.html', {'obj': obj})
