from django.db import models

class PrevRoadmap(models.Model):
    prompt = models.TextField()
    response = models.JSONField()

    def __str__(self):
        return f"Prompt: {self.prompt}"