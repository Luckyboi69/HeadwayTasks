"""
URL configuration for Task2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from simulator_api import views
from django.views.decorators.csrf import csrf_exempt

from simulator_api.schema import schema
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_simulator/', views.create_simulator, name='create_simulator'),
    path('list_simulators/', views.list_simulators, name='list_simulators'),
    path('run_simulator/', views.run_simulator, name='run_simulator'),
    path('stop_simulator/', views.stop_simulator, name='stop_simulator'),
    path("graphql/",csrf_exempt(GraphQLView.as_view(graphiql=True,schema=schema)))
]

