import json

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from .edit_project import modify_available
from .message_form import alert_delete_project, show_message, alert_access_deny

from localsrv.models import Project, Topic
from localsrv.admin_form import AdminForm
# from localsrv.add_form import AddForm

import xml.etree.ElementTree as eltree

kFragmentMargin = 3

# Create your views here.

def find_text_pretail(txt, pos):
    begpos = pos
    spcounter = 0
    while begpos >= 0 and (not txt[begpos] == "\n"):
        if txt[begpos].isspace():
            spcounter += 1
            if spcounter >= kFragmentMargin:
                break
        begpos -= 1
    begpos += 1
    return begpos, spcounter >= kFragmentMargin

def find_text_posttail(txt, pos):
    endpos = pos
    spcounter = 0
    while endpos < len(txt) and (not txt[endpos] == "\n"):
        if txt[endpos].isspace():
            spcounter += 1
            if spcounter >= kFragmentMargin:
                break
        endpos += 1
    return endpos, spcounter >= kFragmentMargin


def project_search(request, project):
    prj = Project.objects.get(Slug = project)
    try:
        query = request.GET["q"]
        ql = query.lower()
        callback = request.GET["cb"]
    except MultiValueDictKeyError:
        # It is not search request
        return render(request, "search_help.html", {})
    # Process search request
    items = []
    for tpc in Topic.objects.filter(Project=prj):
        utxt = tpc.SearchText
        stxt = utxt.lower()
        spos = stxt.find(ql, 0)
        frg = []
        fcounter = 0
        while spos >= 0 and fcounter < 3:
            begpos, begdots = find_text_pretail(stxt, spos)
            endpos, enddots = find_text_posttail(stxt, spos + len(ql))
            txt = ""
            if begdots:
                txt += "... "
            txt += utxt[begpos: spos]
            txt += "<span class=\"hl\">"
            txt += utxt[spos: spos + len(ql)]
            txt += "</span>"
            txt += utxt[spos + len(ql): endpos]
            if enddots:
                txt += " ..."
            frg.append(txt)
            spos = stxt.find(ql, endpos)
            fcounter += 1
        if len(frg) > 0:
            item = {}
            item["type"] = tpc.Type
            item["name"] = tpc.Name
            item["tag"] = ""
            item["url"] = tpc.Url
            item["fragments"] = frg
            items.append(item)

    result = {}
    result["hits"] = len(items)
    result["first"] = 0
    result["count"] = len(items)
    result["page"] = 0
    result["pages"] = 1
    result["query"] = query
    result["items"] = items

    rt = callback + "(" + json.dumps(result) + ");"
    return HttpResponse(rt, content_type = "application/javascript")

#    prj = Project.objects.get(Slug = project)
#    for tpc in Topic.objects.filter(Project = prj):
#        print(tpc.ItemFormatText)



# TODO Relocate into edit_project.py

def project_alert_delete(request, project):
    return alert_delete_project(request, "/localsrv/delete/" + project + "/make/",
        "/localsrv/admin/", project)

# TODO Relocate into edit_project.py

def project_make_delete(request, project):
    if not modify_available(request.user):
        return alert_access_deny(request)

    recs = Project.objects.filter(Slug=project).delete()
    return show_message(request, "/localsrv/admin/", 5, "delete_success")


def project_admin(request):
    if not modify_available(request.user):
        return alert_access_deny(request)

    pf = AdminForm()
    pf.SetServerAddress(request.get_host())
    pf.SetModelData(Project)
    context = {"form": pf}
    return render(request, "admin_form.html", context)
