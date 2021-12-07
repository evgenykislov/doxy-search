from django import forms
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from localsrv.models import Project

from .message_form import show_message


def edit_project_edit(request, project):
    item = Project.objects.filter(Slug = project).first()
    if item is None:
        return show_message(request, "/localsrv/admin/", 5, "unknown_project")
    context = {"form_type": "edit", "name": item.Title, "slug": item.Slug, "searchpath": item.DoxySearchPath}
    return render(request, "edit_project.html", context)


def edit_project_add(request):
    context = {"form_type": "add", "name": "", "slug": "", "searchpath": ""}
    return render(request, "edit_project.html", context)


def edit_project_make_add(request):
    need_add = False
    need_exit = False
    need_new = False
    if "save" in request.POST:
        need_add = True
    if "save_exit" in request.POST:
        need_add = True
        need_exit = True
    if "save_new" in request.POST:
        need_add = True
        need_new = True
    if "exit" in request.POST:
        need_exit = True

    key = None
    if need_add:
        prj = Project()
        prj.Title = request.POST["name"]
        prj.Slug = request.POST["slug"]
        prj.DoxySearchPath = request.POST["searchpath"]
        prj.save()
        key = prj.pk

    if need_exit:
        if need_add:
            return show_message(request, "/localsrv/admin/", 5, "add_success")
    return HttpResponse("Error. Unknown result")


def edit_project_make_edit(request, project):
    need_edit = False
    need_exit = False
    if "save" in request.POST:
        need_edit = True
    if "save_exit" in request.POST:
        need_edit = True
        need_exit = True
    if "exit" in request.POST:
        need_exit = True

    slug = ""
    if need_edit:
        item = Project.objects.filter(Slug=project).first()
        if item is None:
            return show_message(request, "/localsrv/admin/", 5, "unknown_project")
        item.Title = request.POST["name"]
        item.Slug = request.POST["slug"]
        item.DoxySearchPath = request.POST["searchpath"]
        item.save()
        slug = item.Slug

    if need_exit:
        return HttpResponseRedirect("/localsrv/admin/")
    return edit_project_edit(request, slug)
