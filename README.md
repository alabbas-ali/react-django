# React Django Project skelaton 

Integrate REACT and DJANGO. There is no “OFFICIAL” way to do this. 
This is my approach, which I feel can be counted in best practices.

React and Django will be two separated projects, For production, we can run `npm build` (so as to bundle the entire React app into a single folder), which can be then served at Django to render.

## Frontend App: 

- package.json contains the following: 
```
{
  ...
  "proxy": "http://localhost:8000",
  "homepage": "/dist",
  ...
}
```

 - 1nd line → proxy: It will help in tunnelling API requests to http://localhost:8000 where the Django application will handle them, so we can simplify writing the requests like this in React:
 ```
    axios.get("/webapi/accounts/")
 ```
 Instead of this:
 ```
    axios.get("http://localhost:8000/webapi/accounts/")
 ```
 - 3rd line → homepage: So that all the static files in the bundled react project, which is in the build folder can match the URLPATTERN of Django (must be same as STATIC_URL variable of settings.py in Django)


## Django Backend App

### Creating Virtual Environment for Python
Open the command-line shell in `backend` folder and run `$ pip install pipenv`

`$ pipenv shell` (this will create a virtual environment)

This step is optional, though it is recommended to have a Virtual Env, as you will probably push your code somewhere in the future.

Actual Django installation
I recommend you to first read Django Rest Framework docs
```
$ pipenv install django djangorestframework djangorestframework-simplejwt django-cors-headers
$ django-admin startproject backend .
$ python manage.py startapp accounts
$ python manage.py migrate
$ python manage.py createsuperuser --username admin
  Email: ......
  Password: ........
```
Edit settings.py in backend (main). These settings are as important as they appear. Especially that DRF Authentication one, it configures the permission of your API for the entire app, but you can set it manually for every view as well.
But remember, these are NOT production settings, there will be some situations where you have to change some of the variables.

[https://www.django-rest-framework.org/api-guide/authentication/#setting-the-authentication-scheme](DRF Authentication Scheme) 

```
ALLOWED_HOSTS = ['localhost', 'localhost:3000']
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
]

INSTALLED_APPS = [
    ...
    # Third party apps
    'rest_framework',
    'corsheaders',
    
    # My apps
    'accounts.apps.AccountsConfig',
]

# (DRF Authentication Scheme) 
# set permission according to your requirements
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions',
        'rest_framework.permissions.IsAdminUser'
    ]
}

MIDDLEWARE = [
    ...,
    'corsheaders.middleware.CorsMiddleware',
    ...,
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'frontend' ],
        ...
        },
    },
]
...
STATIC_URL = '/dist'
# Extra places for collectstatic to find static files.
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'frontend/build',
]
```

- Now run these commands to make sure that all tables are created.
```
$ python manage.py makemigrations
$ python manage.py migrate
```
- In ./accounts folder
Serializers in Django REST Framework are responsible for converting objects into data types understandable by javascript and front-end frameworks.

Create serializers.py in accounts

```
from rest_framework import serializers
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
```

Edit views.py in accounts

```
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer
# To make password encryption
from django.contrib.auth.hashers import make_password
# API view for django.contrib.auth.models.User
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # it takes recent instance from serialzer and uses `make_password` to encrypt
    def perform_create(self, serializer):
        # Hash password but passwords are not required
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()
    def perform_update(self, serializer):
        # Hash password but passwords are not required
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()
```

Edit urls.py in accounts

```
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# Registering Rest-API routes for Accounts
router = DefaultRouter()
router.register(r'user', views.UserViewSet, 'user')
urlpatterns = [
    path('', include(router.urls), name='accounts_api'),
]
```

- In `./backend` (main) project folder
Create views.py in `backend` (main)
NOTE: You can change “build” to “public” in the development, for that you need to have webpack.config.js and .babelrcconfigured to convert all the src code in one js file.
Read more about webpack and babel

```
from django.shortcuts import render
def index(request):
    return render(request, 'build/index.html')
```

- Edit urls.py in `backend` (main)

Finally all the URLs (from other apps are included in this main one)

Notice we are also using “auth” for rest_framework, from where we can authorize the user to use our webapi.

```
from django.contrib import admin
from django.urls import path, include
# Static files
from . import settings
from django.conf.urls.static import static
# DRF Simple JWT library
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    
    # For REST login
    path('auth/', include('rest_framework.urls'), name='rest_login'),
    # For accessing Token to authenticate
    path('get-auth-token/', TokenObtainPairView.as_view(), name='get_auth_token'),
    path('refresh-auth-token/', TokenRefreshView.as_view(), name='refresh_auth_token'),
    path('verify-auth-token/', TokenVerifyView.as_view(), name='verify_auth_token'),
    
    # API for other apps
    path('webapi/accounts/', include('accounts.urls'), name='webapi_accounts'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

Output


## Deployment

Just run npm build and it will bundle an optimized React application into the build folder.

Now you only need to run python manage.py runserver to run the entire app.

Now technically you are just using a Django application. But who knows that you have created your full frontend in React JS. 😎

To follow full deployment to the server (which is easiest in Heroku), check this out Heroku Django app deployment.

But I recommend don’t just depend on Heroku, try to learn the concept behind it, don’t just copy-paste the commands.
