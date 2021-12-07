from django import forms
from django.views.generic.edit import FormView

class AdminForm(forms.Form):

    def SetServerAddress(self, serv_addr):
        self.server_address = serv_addr

    def SetModelData(self, projects):
        assert len(self.server_address) > 0, "Call SetServerAddress before SetModelData"
        self.data = []
        pd = projects.objects.all()
        for p in pd:
            item = {}
            item["name"] = p.Title
            item["slug"] = p.Slug
            item["search_url"] = self.GetSearchUrl(p.Slug)
            item["parse_url"] = self.GetParseUrl(p.Slug)
            item["delete_url"] = self.GetDeleteUrl(p.Slug)
            item["edit_url"] = self.GetEditUrl(p.Slug)

            self.data.append(item)

    def GetSearchUrl(self, slug_name):
        return "http://" + self.server_address + "/" + "localsrv" + "/search/" + slug_name + "/"

    def GetParseUrl(self, slug_name):
        return "http://" + self.server_address + "/" + "localsrv" + "/parse/" + slug_name + "/"

    def GetDeleteUrl(self, slug_name):
        return "http://" + self.server_address + "/" + "localsrv" + "/delete/" + slug_name + "/"


    def GetEditUrl(self, slug_name):
        return "http://" + self.server_address + "/" + "localsrv" + "/edit/" + slug_name + "/"
