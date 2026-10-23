from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=20, unique=True)
    tagline = models.CharField(max_length=50)
    image = models.ImageField(upload_to='subjects/')

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='topics/')
    model_3d = models.CharField(
        max_length=200,
        help_text="Example: models/solar_system.glb",
        blank=True
    )

    def __str__(self):
        return self.name


class Hotspot(models.Model):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="hotspots"
    )
    number = models.IntegerField()
    label = models.CharField(max_length=200)
    position = models.CharField(
        max_length=100,
        help_text='Example: "0m 0.1m 0m"'
    )
    normal = models.CharField(
        max_length=100,
        help_text='Example: "0m 1m 0m"'
    )

    def __str__(self):
        return f"{self.topic.name} - Hotspot {self.number}"
