
from django.db import models
from .users.models import *
    
class Save_Search(models.Model):
    owner = models.ForeignKey(BaseUser, on_delete=models.CASCADE, null=True)
    search_dict = models.TextField(null=False, blank=False, default="")
    query = models.TextField(null=False, blank=False)
    saved = models.DateField(auto_now=True)

    class Meta:
            ordering = ['-saved']

class Save_Study(models.Model):
    owner = models.ForeignKey(BaseUser, on_delete=models.CASCADE, null=True)
    nctId = models.TextField(null=False, blank = False)
    title = models.TextField(null=False, blank = False, default="")
    save_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-save_date']

class Profile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    bio = models.TextField(default='')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)


class Share_Search(models.Model):
    owner = models.ForeignKey(BaseUser, on_delete=models.CASCADE, null=True)
    query = models.TextField(null=False, blank=False)
    uid = models.TextField(null=False, blank=False)
    save_date = models.DateField(auto_now=True)

class Share_Study(models.Model):
    owner = models.ForeignKey(BaseUser, on_delete=models.CASCADE, null=True)
    nctId = models.TextField(null=False, blank = False)
    uid = models.TextField(null=False, blank=False)
    save_date = models.DateField(auto_now=True)