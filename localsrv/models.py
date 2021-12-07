from django.db import models


# Create your models here.

class Project(models.Model):
    Title = models.CharField(max_length = 50)
    Slug = models.SlugField()
    DoxySearchPath = models.TextField()


class Topic(models.Model):
    Project = models.ForeignKey(Project, on_delete = models.CASCADE)
    Type = models.CharField(max_length = 50)
    Name = models.TextField()
    Url = models.URLField()
    SearchText = models.TextField()
