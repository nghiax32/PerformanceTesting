from django.db import models

class TestPlan(models.Model):
    target_url = models.URLField()
    request_type = models.CharField(max_length=10, choices=[("GET", "GET"), ("POST", "POST")])
    num_users = models.IntegerField()
    spawn_rate = models.FloatField()
    duration = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")  # running, done, failed
    log_path = models.CharField(max_length=255, blank=True, null=True)