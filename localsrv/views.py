import json

from django.http import HttpResponse
from django.shortcuts import render

from localsrv.models import Project, Topic

# Create your views here.

def project_search(request, project):



    d = json.loads("""{"hits":1, "first":0, "count":1, "page":0, "pages":1, "query": "включить", "items":[{"type": "function",   "name": "ABONENT_CON_PHONE_STATE::StateClientChanged(LIST_ID *pItem)", "tag": "", "url": "class_a_b_o_n_e_n_t___c_o_n___p_h_o_n_e___s_t_a_t_e.html#af7f73119ee295379b29f4b796f6253ff", "fragments":["Причины включить удержание"]}]}""")
    td = json.dumps(d)
    rt = request.GET["cb"] + "(" + td + ");"
    return HttpResponse(rt, content_type = "application/javascript")

#    prj = Project.objects.get(Slug = project)
#    for tpc in Topic.objects.filter(Project = prj):
#        print(tpc.ItemFormatText)

