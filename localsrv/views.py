import json

from django.http import HttpResponse
from django.shortcuts import render

from .message_form import alert_delete_project, show_message

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
    query = request.GET["q"]
    ql = query.lower()
    callback = request.GET["cb"]
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


def project_parse(request, project):
    prj = Project.objects.get(Slug = project)
    Topic.objects.filter(Project = prj).delete()
    rnode = eltree.parse(prj.DoxySearchPath).getroot()
    for doc in rnode:
        item_type = ""
        item_name = ""
        item_url = ""
        item_keywords = ""
        item_text = ""
        item_args = ""
        for fld in doc.findall("field"):
            tag = fld.get("name")
            if tag is None:
                continue
            if tag == "type":
                item_type = fld.text
            if tag == "name":
                item_name = fld.text
            if tag == "url":
                item_url = fld.text
            if tag == "keywords" and fld.text is not None:
                item_keywords = fld.text
            if tag == "text" and fld.text is not None:
                item_text = fld.text
            if tag == "args" and fld.text is not None:
                item_args = fld.text
        txt = ""
        if item_type == "class" or item_type == "struct" or item_type == "variable":
            dummy_tmp = 0
        elif item_type == "source":
            continue
        elif item_type == "function":
            item_name = item_name + item_args
            txt += item_name + "\n"
        else:
            return HttpResponse("Unknown type: " + item_type)
        tpc = Topic()
        tpc.Project = prj
        tpc.Type = item_type
        tpc.Name = item_name
        tpc.Url = item_url
        # Add keywords
        # TODO detect duplicates
        for kw in item_keywords.split():
            txt += kw + "\n"
        txt += item_text
        tpc.SearchText = txt
        tpc.save()

    return HttpResponse("ok")


def project_alert_delete(request, project):
    return alert_delete_project(request, "/localsrv/delete/" + project + "/make/",
        "/localsrv/admin/", project)


def project_make_delete(request, project):
    recs = Project.objects.filter(Slug=project).delete()
    return show_message(request, "/localsrv/admin/", 5, "delete_success")


def project_admin(request):
    pf = AdminForm()
    pf.SetServerAddress(request.get_host())
    pf.SetModelData(Project)
    context = {"form": pf}
    return render(request, "admin_form.html", context)
