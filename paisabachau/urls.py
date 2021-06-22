"""paisabachau URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
import homesite.views
import homesite.views2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homesite.views.home,name='homepage'),
    path('laptop',homesite.views.laptop,name='laptoppage'),
    path('<slug:priceslug>/',homesite.views.pricerange,name='price'),
    path('mobile',homesite.views.mobile,name='mobilepage'),
    path('laptopscrape',homesite.views2.laptopscrape,name='laptopscrape'),

    path('laptop/<slug:brandslug>/',homesite.views.companys,name='company'),
    path('mobile/<slug:brandslug>/',homesite.views.mobilecompany,name='mobilecompany')
    ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

 