# server
基于多线索的教育类视频导航系统的后端仓库
### 环境配置
[https://www.runoob.com/django/django-tutorial.html](https://www.runoob.com/django/django-tutorial.html)
### 运行环境
* Python 3.6.8
* Django 2.2.1
* 5.7.17 MySQL Community Server
### 使用方法
所有操作都在manage.py文件目录下
1. 开启服务器
> python manage.py runserver 0.0.0.0:8000  
2. 数据迁移。修改model.py文件需要进行。
> python manage.py makemigrations  
> python manage.py migrate
3. 全局变量配置，clone以后根据本地环境配置以下信息。
```python
# GraduationProject/static/tools/global_settings.py
Database = {
    'NAME': 'loginsys',  # 数据库名字
    'USER': 'root',  # 账号
    'PASSWORD': 'password',  # 密码
    'HOST': '127.0.0.1',  # IP
    'PORT': '3306',  # 端口
}

BaseUrl = "http://127.0.0.1:8000"

```