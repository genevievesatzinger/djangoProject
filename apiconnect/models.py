from django.db import models
from django.contrib.auth.models import User

class Save_Search(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    search_dict = models.TextField(null=False, blank=False, default="")
    query = models.TextField(null=False, blank=False)
    saved = models.DateField(auto_now=True)

    class Meta:
            ordering = ['-saved']

class Save_Study(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nctId = models.TextField(null=False, blank = False)
    save_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-save_date']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)


class Share_Search(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    query = models.TextField(null=False, blank=False)
    uid = models.TextField(null=False, blank=False)
    save_date = models.DateField(auto_now=True)

class Share_Study(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nctId = models.TextField(null=False, blank = False)
    uid = models.TextField(null=False, blank=False)
    save_date = models.DateField(auto_now=True)