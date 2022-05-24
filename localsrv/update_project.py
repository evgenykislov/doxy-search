
from django.conf import settings

from django.http import HttpResponse

from django.shortcuts import render

from .edit_project import modify_available
from .message_form import show_message, alert_file_not_found

from localsrv.models import Project, Topic

import xml.etree.ElementTree as eltree


def project_make_parsing(project, filename, filedata):
    try:
        if filename:
            rnode = eltree.parse(filename).getroot()
        elif filedata:
            rnode = eltree.fromstring(filedata)
        else:
            return "hasnt_data"
    except eltree.ParseError:
        return "cant_parse"
    except (FileNotFoundError, NotADirectoryError):
        return "file_not_found"

    prj = Project.objects.get(Slug = project)
    Topic.objects.filter(Project = prj).delete()
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
        elif item_type == "file":
            continue
        else:
            # return "unknown type: " + item_type
            continue
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
    return None


def project_parse(request, project):
    local_srv = False
    try:
        if settings.LOCAL_SRV:
            local_srv = True
    except AttributeError:
        pass
    if not local_srv:
        return show_message(request, "/localsrv/admin/", 10, "local_parsing_only")

    prj = Project.objects.get(Slug = project)
    filename = prj.DoxySearchPath
    filename += "/searchdata.xml"
    res = project_make_parsing(project, filename)
    if res == None:
        return show_message(request, "/localsrv/admin/", 3, "parse_success")
    elif res == "cant_parse":
        return show_message(request, "/localsrv/admin/", 10, "cant_parse_file")
    elif res == "file_not_found":
        return alert_file_not_found(request, "/localsrv/admin/", 10, filename)

    return HttpResponse("Unknown error: " + res)


def project_update(request, project):
    if not modify_available(request.user):
        return alert_access_deny(request)

    item = Project.objects.filter(Slug = project).first()
    if item is None:
        return show_message(request, "/localsrv/admin/", 5, "unknown_project")
    context = {"name": item.Title}
    return render(request, "update_project.html", context)


def project_make_update(request, project):
    if not modify_available(request.user):
        return alert_access_deny(request)

    prj = Project.objects.get(Slug = project)
    fileobj = request.FILES["searchfile"]
    filename = None
    filedata = None
    try:
        filename = fileobj.file.name
    except AttributeError:
        filedata = fileobj.read()

    res = project_make_parsing(project, filename, filedata)
    if res == None:
        return show_message(request, "/localsrv/admin/", 3, "parse_success")
    elif res == "cant_parse":
        return show_message(request, "/localsrv/admin/", 10, "cant_parse_file")
    elif res == "file_not_found":
        return alert_file_not_found(request, "/localsrv/admin/", 10, filename)

    return HttpResponse("Unknown error: " + res)
