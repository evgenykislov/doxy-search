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
