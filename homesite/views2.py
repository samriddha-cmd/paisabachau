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
from .models import alllaptops, gaminglaptop
from .models import homepagemobile
from .models import dell
from .models import msi
from .models import hp
from .models import asus
from .models import lenovo
from .models import apple
from .models import razerblade
from .models import acer



def laptopscrape(request):
    password='Sam8359'

    if request.method=='POST':
        inputpassword=request.POST.get('password')
        if password==inputpassword:
            step1="password was correct"
            step2="site is being scraped please wait........................................."
            headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.95 Safari/537.36',
            'Accept-Language': 'en-GB,en;q=0.5',}
            acer.objects.all().delete()
            asus.objects.all().delete()
            hp.objects.all().delete()
            dell.objects.all().delete()
            msi.objects.all().delete()
            lenovo.objects.all().delete()
            razerblade.objects.all().delete()
            apple.objects.all().delete()
            alllaptops.objects.all().delete()


         
           
            brands = ['apple','dell','hp','lenovo','msi','acer','razerblade','asus']
           
           #ittisitescrape


            for branditti in brands:
                if branditti=='acer' or branditti=='asus' :
                     baseurlitti = 'https://itti.com.np/laptops-by-brands/'+branditti+'-laptop-nepal?product_list_limit=36'
        
                elif branditti=='apple':
                    branditti='apple-macbook'
                    baseurlitti = 'https://itti.com.np/laptops-by-brands/'+branditti+'-laptops-nepal?product_list_limit=36'
                    branditti='apple'
                elif branditti=='dell':
                    baseurlitti = 'https://itti.com.np/laptops-by-brands/'+branditti+'?product_list_limit=36'
                else:
                    baseurlitti = 'https://itti.com.np/laptops-by-brands/'+branditti+'-laptops-nepal?product_list_limit=36'
                i = requests.get(baseurlitti, headers=headers)
                ittisite = BeautifulSoup(i.content, 'html.parser')
                productitti = ittisite.find('ol', class_='products list items product-items row')
                productitti = productitti.find_all('li', class_='item product product-item')
                for infos in productitti:
                    name = infos.find('h2', class_='product-name').text.strip()
                    price = getattr(infos.find('span', class_='price'), 'text', None)
                    image=infos.find('img',class_='product-image-photo')
            
                    forwardpage=infos.find('a',class_='product-item-link')

                
                    sort=price.split('NPR')[1].replace(',','').replace('.00','')
                    sort=int(sort)
                    site='ittinepal'
                    alllaptops.objects.create(forwardlink=forwardpage['href'],photolink=image['data-src'],site=site,laptopname=name,price=sort)
                    if branditti=='acer':
                     
                        acer.objects.create(forwardlink=forwardpage['href'],photolink=image['data-src'],site=site,laptopname=name,price=sort)
                    elif branditti=='asus':
                     
                        asus.objects.create(forwardlink=forwardpage['href'],photolink=image['data-src'],site=site,laptopname=name,price=sort)   
                    elif branditti=='hp':
                        hp.objects.create(forwardlink=forwardpage['href'],photolink=image['data-src'],site=site,laptopname=name,price=sort)           
                    elif branditti=='dell':
                        dell.objects.create(forwardlink=forwardpage['href'],photolink=image['data-src'],site=site,laptopname=name,price=sort)           
                    elif branditti=='razerblade':
                        razerblade.objects.create(forwardlink=forwardpage['href'],photolink=image['data-src'],site=site,laptopname=name,price=sort)           
                    elif branditti=='apple':
                       
                        apple.objects.create(forwardlink=forwardpage['href'],photolink=image['data-src'],site=site,laptopname=name,price=sort)           
                    elif branditti=='lenovo':
                       lenovo.objects.create(forwardlink=forwardpage['href'],photolink=image['data-src'],site=site,laptopname=name,price=sort)           
                    elif branditti=='msi':
                       msi.objects.create(forwardlink=forwardpage['href'],photolink=image['data-src'],site=site,laptopname=name,price=sort)           

                print('itti scrape suceesful')


            #zozohubscrape    
            brandszozo = ['apple','dell','hp','lenovo','msi','acer','asus']
  
            for brandzozo in brandszozo:
                if brandzozo=='acer':
                    brandzozo='17' 
                    position=1
                elif brandzozo=='asus':
                    brandzozo='18'
                    position=1
                elif brandzozo=='hp':
                    brandzozo='19' 
                    position=1
                elif brandzozo=='lenovo':
                    brandzozo='21'
                    position=1
                elif brandzozo=='msi':
                    brandzozo='22'
                    position=1
                elif brandzozo=='dell':
                    brandzozo='20'
                    position=1
                elif brandzozo=='apple':
                    brandzozo='16'
                    position=1
                if position==1:
                    baseurlzozohub='https://zozohub.com/category-products/'+brandzozo+'?limit=50'
                    zozohubsite=requests.get(baseurlzozohub,headers=headers).text
                
                    zozohubsite=json.loads(zozohubsite)

                    productszozo=zozohubsite['products']['data']
                

                    for infos in productszozo:
                        print("zozohubsite data")
                        selector = scrapy.Selector(text=infos['priceHTML'], type="html")
                        
                        selector=selector.xpath('//span/text()').extract()

                        price=selector[1]
                        price=price.split('Rs. ')[1].replace(',','')
                        price=int(price)
                        slug='https://zozohub.com/'+infos['slug']
                        site='zozohub'
                        alllaptops.objects.create(forwardlink=slug,photolink=infos['image'],site=site,laptopname=infos['name'],price=price)
                        if brandzozo=='17':
                            print('scraping acer')
                            acer.objects.create(forwardlink=slug,photolink=infos['image'],site=site,laptopname=infos['name'],price=price)
                        elif brandzozo=='18':
                            print('scraping asus')
                            asus.objects.create(forwardlink=slug,photolink=infos['image'],site=site,laptopname=infos['name'],price=price)
                        elif brandzozo=='19':
                            print('scraping hp')
                            hp.objects.create(forwardlink=slug,photolink=infos['image'],site=site,laptopname=infos['name'],price=price)
                        elif brandzozo=='20':
                            dell.objects.create(forwardlink=slug,photolink=infos['image'],site=site,laptopname=infos['name'],price=price)
                        
                        elif brandzozo=='16':
                            apple.objects.create(forwardlink=slug,photolink=infos['image'],site=site,laptopname=infos['name'],price=price)
                        elif brandzozo=='21':
                            lenovo.objects.create(forwardlink=slug,photolink=infos['image'],site=site,laptopname=infos['name'],price=price)
                        elif brandzozo=='22':
                            msi.objects.create(forwardlink=slug,photolink=infos['image'],site=site,laptopname=infos['name'],price=price)



            #LDS scrape-----------------------------------------------------
            brandsldss = ['apple','dell','hp','lenovo','msi','acer','razerblade','asus']
            print("lds scraping started.....................")
            for brandlds in brandsldss:
                ldscount=0
                if brandlds=='acer' or brandlds=='hp' or brandzozo=='dell' or brandlds=='lenovo' or brandlds=='msi' or brandlds=='asus':
                    ldscount=1
                    baseurllds = 'https://lds.com.np/laptop/laptop-'+brandlds+'?limit=36'
                    
                elif brandlds=='apple':
                    brandlds='Apple'
                    ldscount=1
                    baseurllds='https://lds.com.np/laptop/Laptops-'+brandlds+'?limit=36'
                    brandlds='apple'
                
                if ldscount== 1:
                    l=requests.get(baseurllds,headers=headers)
                    ldssite=BeautifulSoup(l.content,'html.parser')
                    productlds=ldssite.find('div',class_='products-block')
                    productlds=productlds.find_all('div',class_='product-block')
                    
                    for infos in productlds:
                        name=infos.find('h6',class_='name').text
                        price=infos.find('span',class_='price-new').text
                        image=infos.find('img',class_='img-responsive')
                        forwardpage=infos.find('a',class_='img')
                    
                        pricesort=price.split('NPR')[1].replace(',','').replace('.00','')
                        pricesort=int(pricesort)
                        site='ldsnepal'
                        print('scraping lds data')
                        alllaptops.objects.create(forwardlink=forwardpage['href'],photolink=image['src'],site=site,laptopname=name,price=pricesort)
                        if brandlds=='acer':
                            print('scraping lds acer ')
                            acer.objects.create(forwardlink=forwardpage['href'],photolink=image['src'],site=site,laptopname=name,price=pricesort)
                        elif brandlds=='asus':
                            asus.objects.create(forwardlink=forwardpage['href'],photolink=image['src'],site=site,laptopname=name,price=pricesort)   
                        elif brandlds=='hp':
                            hp.objects.create(forwardlink=forwardpage['href'],photolink=image['src'],site=site,laptopname=name,price=pricesort)           
                        elif brandlds=='dell':
                            dell.objects.create(forwardlink=forwardpage['href'],photolink=image['src'],site=site,laptopname=name,price=pricesort)           
                        elif brandlds=='razerblade':
                            razerblade.objects.create(forwardlink=forwardpage['href'],photolink=image['src'],site=site,laptopname=name,price=pricesort)           
                        elif brandlds=='apple':
                            apple.objects.create(forwardlink=forwardpage['href'],photolink=image['src'],site=site,laptopname=name,price=pricesort)           
                        elif brandlds=='lenovo':
                            lenovo.objects.create(forwardlink=forwardpage['href'],photolink=image['src'],site=site,laptopname=name,price=pricesort)           
                        elif brandlds=='msi':
                            print('scraping lds msi ')
                            msi.objects.create(forwardlink=forwardpage['href'],photolink=image['src'],site=site,laptopname=name,price=pricesort)           
            print('lds data scrape sucessful')  




    #ptech brand-------------------------------------
            print('starting ptech data scrape')
            brandptechs=['apple','dell','hp','lenovo','msi','acer','razerblade','asus']
            count=0
            for brandptech in brandptechs:
                if brandptech=='acer' or brandptech=='hp' or brandptech=='dell' or brandptech=='lenovo' or brandptech=='msi' or brandptech=='asus':
                    baseurlptech='https://ptechktm.com/laptops/'+brandptech+'?product_list_limit=36'
                    count=1
                if count==1:
                    p=requests.get(baseurlptech,headers=headers)
                    ptechsite=BeautifulSoup(p.content,'html.parser')
                    productptech=ptechsite.find('ol', class_='products list items product-items')
                    productptech=productptech.find_all('div',class_='images-container')

                    for infos in productptech:
                        name=infos.find('h2','product-name product-item-name').text
                        price=infos.find('span',class_='price').text
                        image=infos.find('img',class_='product-image-photo')
                        forwardpage=infos.find('a',class_='product-item-photo')
                        pricesort=price.split('Rs ')[1].replace(',','').replace('.00','')
                        pricesort=int(pricesort)
                
                        site='ptech electronics'
                        print('here')
                        alllaptops.objects.create(forwardlink=forwardpage['href'],photolink=image['data-src'],laptopname=name,price=pricesort,site=site)
                        if brandptech=='acer':
                            print('scraping ptech acer ')
                            acer.objects.create(forwardlink=forwardpage['href'],photolink=image['data-src'],site=site,laptopname=name,price=pricesort)
                        elif brandptech=='asus':
                            asus.objects.create(forwardlink=forwardpage['href'],photolink=image['data-src'],site=site,laptopname=name,price=pricesort)   
                        elif brandptech=='hp':
                            hp.objects.create(forwardlink=forwardpage['href'],photolink=image['data-src'],site=site,laptopname=name,price=pricesort)           
                        elif brandptech=='dell':
                            dell.objects.create(forwardlink=forwardpage['href'],photolink=image['data-src'],site=site,laptopname=name,price=pricesort)           
                        
                        
                        elif brandptech=='lenovo':
                            print('scraping lenovo ptech')
                            lenovo.objects.create(forwardlink=forwardpage['href'],photolink=image['src'],site=site,laptopname=name,price=pricesort)           
                        elif brandptech=='msi':
                            print('scraping lds msi ')
                            msi.objects.create(forwardlink=forwardpage['href'],photolink=image['src'],site=site,laptopname=name,price=pricesort)           

               
            print('ptech data sucessfully saved')


            return render(request,'laptopscrape.html',{'password':step1,'wait':step2})
            

            
        else:
            step1="password was incorrect"
            step2="Please type password again"
            return render(request,'laptopscrape.html',{'password':step1,'wait':step2})
    return render(request,'laptopscrape.html')