from django.shortcuts import render

def show_message(request, url, timeout, message):
    content = {"url": url,
        "timeout": timeout,
        "message": message}
    return render(request, "message_form.html", content)


def alert_delete_project(request, url_yes, url_no, project):
    content = {"url_yes": url_yes,
        "url_no": url_no,
        "project": project}
    return render(request, "alert_delete_project.html", content)


def alert_file_not_found(request, url, timeout, filename):
    content = {"url": url,
        "timeout": timeout,
        "message": "file_not_found",
        "filename": filename}
    return render(request, "message_form.html", content)


def alert_cant_parse_file(request, url, timeout, description):
    content = {"url": url,
        "timeout": timeout,
        "message": "cant_parse_data",
        "description": description}
    return render(request, "message_form.html", content)


def alert_access_deny(request):
    return show_message(request, "/accounts/login/", 5, "access_deny")
