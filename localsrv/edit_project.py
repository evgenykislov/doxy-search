from django import forms
from django.conf import settings
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.utils.text import slugify

from localsrv.models import Project

from .message_form import show_message, alert_access_deny

# Checks the user can modify something
def modify_available(user):
    try:
        if settings.LOCAL_SRV:
            return True
    except AttributeError:
        pass

    if user.is_authenticated:
        return True

    return False


def generate_slug(name):
    slug = slugify(name)
    if len(slug) == 0:
        slug = "ds"
    item = Project.objects.filter(Slug=slug).first()
    if item is None:
        return slug
    # need to generate new slug
    for i in range(1, 100):
        sl = slug + "-" + str(i)
        if Project.objects.filter(Slug=sl).first() is None:
            return sl
    return None



def edit_project_edit(request, project):
    item = Project.objects.filter(Slug = project).first()
    if item is None:
        return show_message(request, "/localsrv/admin/", 5, "unknown_project")
    context = {"form_type": "edit", "name": item.Title, "searchpath": item.DoxySearchPath}
    return render(request, "edit_project.html", context)


def edit_project_add(request):
    context = {"form_type": "add", "name": "", "searchpath": ""}
    return render(request, "edit_project.html", context)


def edit_project_make_add(request):
    if not modify_available(request.user):
        return alert_access_deny(request)

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
        slug = generate_slug(prj.Title)
        if slug is None:
            return HttpResponse("Error. Can't generate unique slug")
        prj.Slug = slug
        prj.DoxySearchPath = request.POST["searchpath"]
        prj.save()
        key = prj.pk

    if need_exit:
        if need_add:
            return show_message(request, "/localsrv/admin/", 5, "add_success")
        else:
            return HttpResponseRedirect("/localsrv/admin/")
    return HttpResponse("Error. Unknown result")


def edit_project_make_edit(request, project):
    if not modify_available(request.user):
        return alert_access_deny(request)

    need_edit = False
    need_exit = False
    if "save" in request.POST:
        need_edit = True
    if "save_exit" in request.POST:
        need_edit = True
        need_exit = True
    if "exit" in request.POST:
        need_exit = True

    if need_edit:
        item = Project.objects.filter(Slug=project).first()
        if item is None:
            return show_message(request, "/localsrv/admin/", 5, "unknown_project")
        item.Title = request.POST["name"]
        item.DoxySearchPath = request.POST["searchpath"]
        item.save()

    if need_exit:
        return HttpResponseRedirect("/localsrv/admin/")
    return edit_project_edit(request, project)
