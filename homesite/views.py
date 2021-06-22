from typing import Text
from django.db.models import base
from django.http.request import HttpHeaders
from django.shortcuts import render
import requests
from requests.api import delete
from bs4 import BeautifulSoup
from operator import itemgetter
import json
from django.core import serializers
from django.http import JsonResponse
import scrapy 
from .models import gaminglaptop, lenovo
from .models import homepagemobile
from .models import alllaptops
from .models import acer
from .models import hp
from .models import dell
from .models import asus
from .models import msi
from .models import razerblade
from .models import apple

def home(request):
    ittitotalinfolist=[]
    base_url="https://www.itti.com.np/"
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36' 
    }
    r=requests.get('https://www.itti.com.np/',headers=headers)
  
    soups=BeautifulSoup(r.content,'html.parser')
   
    
   


        
    
    

    productlist=soups.find('div',class_='product-container')
    productlist=productlist.find_all('div',class_='deals-items')
    infos=homepagemobile.objects.all()
    count=0
    for info in productlist:
      
        name = info.find('h2', class_='product-name').text.strip()
    
        price = getattr(info.find('span', class_='price'), 'text', None)
        image=info.find('img',class_='product-image-photo')
   
        forwardpage=info.find('a',class_='product-item-link')

     
        sort=price.split('NPR')[1].replace(',','').replace('.00','')
     
        count=count+1
        if count>=6:
            break
        ittitotalinfo = {
            'name': name,
            'price': price,
            'image':image['data-src'],
            'forwardpage0':forwardpage['href'],
            'arranger':sort,
            'logo':1
        }
        ittitotalinfolist.append(ittitotalinfo)
   
    return render(request,'home.html',{'infos':infos,'ittitotalinfo':ittitotalinfolist})

def laptop(request):
    
    

    #ripple laptops ---------------------------------------------------------------
    base_url='https://rippledevice.com/shop/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.95 Safari/537.36',
        'Accept-Language': 'en-GB,en;q=0.5',
    }
    r=requests.get(base_url, headers = headers)
    price=[]
    ripplelaptopfinalpage=[]
    soup=BeautifulSoup(r.content,'html.parser')
  
    productlist=soup.find_all('div',class_='product-card')
    for link in productlist:
        for links in link.find_all('a'):
            price.append(links)
    for info in price:
         ripplelaptopfinalpage.append(info['href'])     
    nameinfo=soup.find_all('h6')
 
    priceinfo=soup.find_all('span',class_='woocommerce-Price-amount')
    ripplelaptopspriceinfo=[]
    ripplelaptopsprice=[]
    for price in priceinfo:
        price=price.text
        price=price.split("\n")
        ripplelaptopspriceinfo.append(price)
    for price in ripplelaptopspriceinfo:
        price.pop(0)

    for price in ripplelaptopspriceinfo:
        for prices in price:
            ripplelaptopsprice.append(prices)
    ripplelaptopname=[]
    ripplelaptopspecs=[]
    ripplelaptopspecsinfo=[]
    names=[]
    count=0
    for name in nameinfo:
        name=name.text
        ripplelaptopname.append(name)


    ripplespecs=soup.find_all('h3')
    for name in ripplespecs:
        ripplelaptopspecsinfo.append(name.text)
    
    for name in range(len(ripplelaptopname)):
        ripplelaptopspecs.append(ripplelaptopspecsinfo[name])

    ripplelaptopimage=[]
    priceinfo=[]
   
    totalinfo={}

    for info in productlist:
        for link in info.find_all('img'):
           priceinfo.append(link)
    for info in priceinfo:
        ripplelaptopimage.append(info['src'])
  
    for a in range(0,len(ripplelaptopspriceinfo)):
        totalinfo[ripplelaptopsprice[a]]=ripplelaptopname[a],ripplelaptopspecs[a],ripplelaptopimage[a],ripplelaptopfinalpage[a]


    # Gaming Laptops Data--------------------------------------------------------------------
    infos=gaminglaptop.objects.all()
    

    return render(request,'laptop.html',{'productslist':totalinfo ,'productlists':soup,'infos':infos})



def companys(request,brandslug):
    brand=brandslug
    if brand=='acer':
        branddata=acer.objects.all().order_by('price')
      
    if brand=='asus':
        branddata=asus.objects.all().order_by('price')
    if brand=='apple':
        branddata=apple.objects.all().order_by('price')
    if brand=='msi':
        branddata=msi.objects.all().order_by('price')
    if brand=='hp':
        branddata=hp.objects.all().order_by('price')
    if brand=='lenovo':
        branddata=lenovo.objects.all().order_by('price')
    if brand=='razerblade':
        branddata=razerblade.objects.all().order_by('price')
    if brand=='dell':
        branddata=dell.objects.all().order_by('price')
    count=len(branddata)
    
    try:
        filtered_data=[]
        if request.method=='GET':
            upperlimit=int(request.GET.get('upperlimits'))
            lowerlimit=int(request.GET.get('lowerlimits'))

        for infos in branddata:
          
            if infos.price >= lowerlimit and infos.price <= upperlimit:
                filtered_data.append(infos)
        count=len(filtered_data)
        return render(request, 'laptopbrand.html',{'ittinepal':filtered_data,'brand':brandslug.capitalize(),'count':count})
    except:   
        return render(request, 'laptopbrand.html',{'ittinepal':branddata,'brand':brandslug.capitalize(),'count':count})

def pricerange(request,priceslug):
    pricerangeinfolist=[]
    price=priceslug

    price=price.split('-')
  
    lowerprice=price[1]
    upperprice=price[2]
    lowerprice=int(lowerprice)
    upperprice=int(upperprice)
    filtered_data=[]

    alllaptopdata=alllaptops.objects.all().order_by('price')

    for infos in alllaptopdata:
        if infos.price>=lowerprice and infos.price <=upperprice:
            filtered_data.append(infos)
    
    count=len(filtered_data)
 
    try:
        filtered_data2=[]
        if request.method=='GET':
            upperlimit=int(request.GET.get('upperlimits'))
            lowerlimit=int(request.GET.get('lowerlimits'))

            for infos in filtered_data:
                if infos.price>=lowerlimit  and infos.price <=upperlimit:
                    filtered_data2.append(infos)
                    print(infos.price)   
               
            count=len(filtered_data)

        return render(request,'laptopbrand.html',{'ittinepal':filtered_data2,'count':count})
    except:
           
        return render(request,'laptopbrand.html',{'ittinepal':filtered_data,'count':count})
    

def mobile(request):
    return render(request,'mobile.html')

def mobilecompany(request,brandslug):
    count=0
    prices=[]
    for i in range(1,4):
        i=str(i)
        baseurl='https://www.dealayo.com/mobile/samsung.html?mode=grid&p='+i
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.95 Safari/537.36',
            'Accept-Language': 'en-GB,en;q=0.5',
        }
        d=requests.get(baseurl, headers = headers)
        soup=BeautifulSoup(d.content,'html.parser')
        dealayoproduct=soup.find('div','products-grid amda-block-product01')
        dealayoproduct=dealayoproduct.find_all('li','item product-item col-desktop-4 col-tablet-l-3 col-tablet-p-2 col-mobile-2')
    
        for infos in dealayoproduct:
            name=infos.find('h2').text
            try:
                price=infos.find('p', class_='special-price')
                price=price.find('span',class_='price').text.strip()
                prices.append(price)
                count=count+1
            except:
                price=infos.find('span',class_='regular-price').text.strip()
                count=count+1
                prices.append(price)
            imagelink=infos.find('div',class_='amda-product-top')
            imagelink=imagelink.find('img',class_='img-responsive')['src']
            forwardlink=infos.find('div',class_='amda-product-top')
            forwardlink=forwardlink.find('a',class_='product-image no-alt-img')['href']
           
            prices.append(forwardlink)
        

    print(prices)
    print(count)

    return render(request,'mobilebrand.html')