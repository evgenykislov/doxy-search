
from django.urls import path
from .views import project_admin, project_search, project_alert_delete, project_make_delete
from .edit_project import edit_project_add, edit_project_make_add, edit_project_edit, edit_project_make_edit
from .update_project import project_parse, project_update, project_make_update

urlpatterns = [
    path("admin/add/", edit_project_add),
    path("admin/add/make/", edit_project_make_add),
    path("admin/", project_admin),
    path("search/<str:project>/", project_search),
    path("parse/<str:project>/", project_parse),
    path("delete/<str:project>/", project_alert_delete),
    path("delete/<str:project>/make/", project_make_delete),
    path("edit/<str:project>/", edit_project_edit),
    path("edit/<str:project>/make/", edit_project_make_edit),
    path("update/<str:project>/", project_update),
    path("update/<str:project>/make/", project_make_update)
]
