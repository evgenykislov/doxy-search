
from django.http import HttpResponse

from .message_form import show_message, alert_file_not_found

from localsrv.models import Project, Topic

import xml.etree.ElementTree as eltree



def project_parse(request, project):
    prj = Project.objects.get(Slug = project)
    filename = prj.DoxySearchPath
    try:
        rnode = eltree.parse(filename).getroot()
    except eltree.ParseError:
        return show_message(request, "/localsrv/admin/", 10, "cant_parse_file")
    except FileNotFoundError:
        return alert_file_not_found(request, "/localsrv/admin/", 10, filename)

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
#            return HttpResponse("Unknown type: " + item_type)
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

    return HttpResponse("ok")
