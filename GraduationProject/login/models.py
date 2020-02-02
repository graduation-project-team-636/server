from django.db import models
from django import forms
# Create your models here.


class User(models.Model):
    # username必填，最长不超过128个字符，并且唯一，也就是不能有相同姓名；
    # password必填，最长不超过256个字符（实际可能不需要这么长）；
    # email使用Django内置的邮箱类型，并且唯一；
    # 性别使用了一个choice，只能选择男或者女，默认为男；
    # 使用__str__帮助人性化显示对象信息；
    # 元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；
    username = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128, unique=False, default="name")
    password = models.CharField(max_length=256)
    reg_time = models.DateTimeField(auto_now_add=True)
    groupid = models.IntegerField(default="2")
    email = models.CharField(max_length=128, blank=True)
    telephone = models.CharField(max_length=50, blank=True)
    sex = models.CharField(max_length=32, default="1")
    signature = models.CharField(max_length=128, default="这个人很懒，什么都没有留下")
    city = models.CharField(max_length=128, blank=True)
    occupation = models.CharField(max_length=128, blank=True)
    hobby = models.CharField(max_length=256, blank=True)
    avatar = models.FileField(upload_to='avatars/%Y/%m/%d',
                              default="/avatars/default.png")

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["reg_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    name = forms.CharField(label="昵称", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    # gender = (
    #     ('male', "男"),
    #     ('female', "女"),
    # )
    # email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(
    #     attrs={'class': 'form-control'}))
    # sex = forms.ChoiceField(label='性别', choices=gender)


class ProfileForm(forms.Form):
    name = forms.CharField(label="昵称", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    sex = forms.CharField(label="性别", max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    city = forms.CharField(label="城市", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    occupation = forms.CharField(label="职业", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    hobby = forms.CharField(label="爱好", max_length=256, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    signature = forms.CharField(label="个性签名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

