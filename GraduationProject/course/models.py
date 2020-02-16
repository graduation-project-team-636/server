from django.db import models
from django import forms
# Create your models here.


class Course(models.Model):
    course_name = models.CharField(max_length=128)
    course_introduction = models.CharField(max_length=128)
    course_category = models.CharField(max_length=128)
    course_tag = models.CharField(max_length=32)
    course_cover = models.FileField(upload_to='cover/%Y/%m/%d',
                                    default="/cover/default.png")
    course_attendance = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    course_attendance_id = models.CharField(
        max_length=256, blank=True, default="")
    video_id = models.CharField(
        max_length=256, blank=True, default="")

    def __str__(self):
        return self.course_name

    class Meta:
        ordering = ["create_time"]
        verbose_name = "课程"
        verbose_name_plural = "课程"


class CreateForm(forms.Form):
    course_name = forms.CharField(label="课程名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    course_introduction = forms.CharField(label="课程简介", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    course_category = forms.CharField(label="课程分区", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    course_tag = forms.CharField(label="课程标签", max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    course_cover = forms.FileField(label="封面图片")


class ModifyForm(forms.Form):
    course_id = forms.IntegerField(label="课程id")
    course_name = forms.CharField(label="课程名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    course_introduction = forms.CharField(label="课程简介", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    course_category = forms.CharField(label="课程分区", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    course_tag = forms.CharField(label="课程标签", max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    course_cover = forms.FileField(label="封面图片")
