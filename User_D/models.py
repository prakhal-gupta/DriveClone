from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from .models import *



class User_data(models.Model):
        user                   = models.OneToOneField(User, on_delete=models.CASCADE)
        Profile_pic            = models.ImageField(upload_to='profile_pic/', default='static/profile-default.png')
        DOB                    = models.DateField(null=True)
        Mobile_Number          = models.CharField(max_length=10, null=True)
        Gender                 = models.CharField(max_length=20, null=True)
        Used_space_mb          = models.CharField(max_length=30, null=True, default=0)
        Upload_limit_mb        = models.IntegerField(null=True,default=500)

   

class Uploaded_folder(models.Model): 

        user                   = models.ForeignKey(User, on_delete=models.CASCADE)
        Folder                 = models.CharField(max_length=50, null=True)
        Status                 = models.CharField(max_length=20, null=True, default='Available')
        Parent_id              = models.ForeignKey('self', on_delete=models.CASCADE, null=True) 
        created_at             = models.DateTimeField(auto_now_add=True, null=True)


class Uploaded_files(models.Model): 

        user                   = models.ForeignKey(User, on_delete=models.CASCADE)
        folder                 = models.ForeignKey(Uploaded_folder, on_delete=models.CASCADE, null=True)
        Uploads                = models.FileField(null=True, blank=True, upload_to='uploaded_files/')
        Default_img            = models.TextField(max_length=100, null=True)
        Status                 = models.CharField(max_length=20, null=True, default='Available') 
        Type                   = models.CharField(max_length=30, null=True)
        Size_kb                = models.CharField(max_length=30, null=True)
        Uploaded_at            = models.DateTimeField(auto_now_add=True, null=True) 

class testing(models.Model):

        test                = models.FileField(null=True, blank=True, upload_to='testing_files/')
        file_size           = models.CharField(max_length=50, null=True)
        Uploaded_at         = models.DateTimeField(auto_now_add=True, null=True)


class File_Size(models.Model):

        Type                = models.CharField(max_length=30, null=True)
        file_size_kb        = models.CharField(max_length=50, null=True)
        