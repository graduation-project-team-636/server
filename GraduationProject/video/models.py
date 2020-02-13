from django.db import models
from django import forms
# Create your models here.


class Video(models.Model):
    video_name = models.CharField(max_length=128)
    video_duration = models.IntegerField()
    video_data = models.FileField(upload_to='video/%Y/%m/%d')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_name

    class Meta:
        ordering = ["upload_time"]
        verbose_name = "视频"
        verbose_name_plural = "视频"


class UploadForm(forms.Form):
    course_id = forms.IntegerField(label="课程id")
    video_name = forms.CharField(label="视频名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    video_duration = forms.IntegerField(label="视频时长")
    video_data = forms.FileField(label="视频文件")


class ModifyForm(forms.Form):
    video_id = forms.IntegerField(label="视频id")
    video_name = forms.CharField(label="视频名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
