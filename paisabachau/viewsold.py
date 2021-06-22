


def home(request):
    ittitotalinfolist=[]
    base_url="https://www.itti.com.np/"
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    r=requests.get('https://www.itti.com.np/',headers=headers)

    soups=BeautifulSoup(r.content,'html.parser')




    laptops=alllaptops.objects.order_by('price')

    for laptop in laptops:
        print(laptop.price)
        print(laptop.laptopname)
    homepagemobile.objects.create(forwardlink='https://www.itti.com.np/',photolink='https://www.itti.com.np/',mobilename='acer nitro 5',price='180000')

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
    count=0
    ittitotalinfo={}
    ittitotalinfolist=[]
    ldstotalinfo={}

    zozohubsite={}
    ptechinfo={}

    brandptech=brandslug
    branditti=brandslug
    brandzozo=brandslug

    brandlds=brandslug
    baseurlitti = 'https://itti.com.np/laptops-by-brands/'
    baseurllds = 'https://lds.com.np/laptop/laptop-'
    baseurlzozohub='https://zozohub.com/category-products/'
    baseurlptech='https://ptechktm.com/laptops/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.95 Safari/537.36',
        'Accept-Language': 'en-GB,en;q=0.5',
    }
    if branditti=='acer' or branditti=='asus' :
        baseurlitti = 'https://itti.com.np/laptops-by-brands/'+branditti+'-laptop-nepal?product_list_limit=36'

    elif branditti=='apple':
        branditti='apple-macbook'
        baseurlitti = 'https://itti.com.np/laptops-by-brands/'+branditti+'-laptops-nepal?product_list_limit=36'
    elif branditti=='dell':
         baseurlitti = 'https://itti.com.np/laptops-by-brands/'+branditti+'?product_list_limit=36'
    else:
        baseurlitti = 'https://itti.com.np/laptops-by-brands/'+branditti+'-laptops-nepal?product_list_limit=36'

    ldscount=0
    if brandlds=='acer' or brandlds=='hp' or brandzozo=='dell' or brandlds=='lenovo' or brandlds=='msi' or brandlds=='asus':
        ldscount=1
        baseurllds = 'https://lds.com.np/laptop/laptop-'+brandlds+'?limit=36'
    elif brandlds=='apple':
        brandlds='Apple'
        ldscount=1
        baseurllds='https://lds.com.np/laptop/Laptops-'+brandlds+'?limit=36'


    if brandptech=='acer' or brandlds=='hp' or brandzozo=='dell' or brandlds=='lenovo' or brandlds=='msi' or brandlds=='asus':
        baseurlptech='https://ptechktm.com/laptops/'+brandptech+'?product_list_limit=36'
        count=1

    elif brandptech=='apple':
        baseurlptech='0'


    i = requests.get(baseurlitti, headers=headers)

    l=requests.get(baseurllds,headers=headers)
    ittisite = BeautifulSoup(i.content, 'html.parser')


    # ittisite scrape portion ---------------------------------------

    productitti = ittisite.find('ol', class_='products list items product-items row')
    productitti = productitti.find_all('li', class_='item product product-item')

    for infos in productitti:
        name = infos.find('h2', class_='product-name').text.strip()
        price = getattr(infos.find('span', class_='price'), 'text', None)
        image=infos.find('img',class_='product-image-photo')

        forwardpage=infos.find('a',class_='product-item-link')


        sort=price.split('NPR')[1].replace(',','').replace('.00','')
        sort=int(sort)

        ittitotalinfo = {
            'name': name,
            'price': price,
            'image':image['data-src'],
            'forwardpage0':forwardpage['href'],
            'arranger':sort,
            'logo':1
        }
        ittitotalinfolist.append(ittitotalinfo)

    #zozohub scrape portion-------------------------------------------------------------------------
    position=0
    brandzozo=brandslug
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
            selector = scrapy.Selector(text=infos['priceHTML'], type="html")

            selector=selector.xpath('//span/text()').extract()

            price=selector[1]
            price=price.split('Rs. ')[1].replace(',','')
            price=int(price)
            slug='https://zozohub.com/'+infos['slug']

            zozohubsite={
                'name':infos['name'],
                'price':price,
                'image':infos['image'],
                'forwardpage0':slug,
                'arranger':price,
                'logo':4
            }
            ittitotalinfolist.append(zozohubsite)


    #-----------------------------------------------------------------------------------------------


    #lds scrape portion ----------------------------------------------------------------------------
    if ldscount== 1:
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
            ldstotalinfo={
                'name':name,
                'price':price,
                'image':image['src'],
                'forwardpage0':forwardpage['href'],
                'arranger':pricesort,
                'logo':2

            }
            ittitotalinfolist.append(ldstotalinfo)

    #ptech scrape portion---------------------------------------------------------
    if count==1:
        print("ptech started")
        p=requests.get(baseurlptech,headers=headers)
        ptechsite=BeautifulSoup(p.content,'html.parser')
        productptech=ptechsite.find('ol', class_='products list items product-items')
        productptech=productptech.find_all('div',class_='images-container')
        print('at ptech')
        for infos in productptech:
            name=infos.find('h2','product-name product-item-name').text
            price=infos.find('span',class_='price').text
            image=infos.find('img',class_='product-image-photo')
            forwardpage=infos.find('a',class_='product-item-photo')
            pricesort=price.split('Rs ')[1].replace(',','').replace('.00','')
            pricesort=int(pricesort)

            ptechinfo={
                'name':name,
                'price':price,
                'image':image['data-src'],
                'forwardpage0':forwardpage['href'],
                'arranger':pricesort,
                'logo':3
            }
            print(name)
            ittitotalinfolist.append(ptechinfo)

    ittitotalinfolist=sorted(ittitotalinfolist,key=itemgetter('arranger'))
    count=len(ittitotalinfolist)

    try:
        filtered_data=[]
        if request.method=='GET':
            upperlimit=int(request.GET.get('upperlimits'))
            lowerlimit=int(request.GET.get('lowerlimits'))

        for infos in ittitotalinfolist:

            if infos['arranger'] >= lowerlimit and infos['arranger'] <= upperlimit:
                filtered_data.append(infos)
        count=len(filtered_data)
        return render(request, 'laptopbrand.html',{'ittinepal':filtered_data,'brand':brandslug.capitalize(),'count':count})
    except:
        return render(request, 'laptopbrand.html',{'ittinepal':ittitotalinfolist,'brand':brandslug.capitalize(),'count':count})

def pricerange(request,priceslug):
    pricerangeinfolist=[]
    price=priceslug

    price=price.split('to')

    lowerprice=price[0]
    upperprice=price[1]
    headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.95 Safari/537.36',
            'Accept-Language': 'en-GB,en;q=0.5',
        }



    baseurl1='http://192.168.1.155:8000/laptop/msi/?csrfmiddlewaretoken=DVZEQm8tIIoHUIxw3QbZfVDxcQj2TgxyvTU3Ivd3TjLSesEJDjSEB30k7RFRCynj&lowerlimits='+lowerprice+'&'+'upperlimits='+upperprice
    p=requests.get(baseurl1,headers=headers)
    paisabachau=BeautifulSoup(p.content,'html.parser')
    paisabachausite=paisabachau.find_all('div',class_='post-box')
    for infos in paisabachausite:
        name=infos.find('h4').text
        image=infos.find('img')
        forwardpage=infos.find('a',class_='button-type')
        price=infos.find('h5',class_='priceheading').text
        pricesort=price.split('NPR')[1]
        pricesort=int(pricesort)
        pricerange={
            'name':name,
            'image':image['src'],
            'forwardpage0':forwardpage['href'],
            'arranger':pricesort
        }
        pricerangeinfolist.append(pricerange)

    baseurl1='http://192.168.1.155:8000/laptop/acer/?csrfmiddlewaretoken=DVZEQm8tIIoHUIxw3QbZfVDxcQj2TgxyvTU3Ivd3TjLSesEJDjSEB30k7RFRCynj&lowerlimits='+lowerprice+'&'+'upperlimits='+upperprice
    p=requests.get(baseurl1,headers=headers)
    paisabachau=BeautifulSoup(p.content,'html.parser')
    paisabachausite=paisabachau.find_all('div',class_='post-box')
    for infos in paisabachausite:
        name=infos.find('h4').text
        image=infos.find('img')
        forwardpage=infos.find('a',class_='button-type')
        price=infos.find('h5',class_='priceheading').text
        pricesort=price.split('NPR')[1]
        pricesort=int(pricesort)

        pricerange={
            'name':name,
            'image':image['src'],
            'forwardpage0':forwardpage['href'],
            'arranger':pricesort
        }
        pricerangeinfolist.append(pricerange)

    baseurl1='http://192.168.1.155:8000/laptop/asus/?csrfmiddlewaretoken=DVZEQm8tIIoHUIxw3QbZfVDxcQj2TgxyvTU3Ivd3TjLSesEJDjSEB30k7RFRCynj&lowerlimits='+lowerprice+'&'+'upperlimits='+upperprice
    p=requests.get(baseurl1,headers=headers)
    paisabachau=BeautifulSoup(p.content,'html.parser')
    paisabachausite=paisabachau.find_all('div',class_='post-box')
    for infos in paisabachausite:
        name=infos.find('h4').text
        image=infos.find('img')
        forwardpage=infos.find('a',class_='button-type')
        price=infos.find('h5',class_='priceheading').text
        pricesort=price.split('NPR')[1]
        pricesort=int(pricesort)

        pricerange={
            'name':name,
            'image':image['src'],
            'forwardpage0':forwardpage['href'],
            'price':price,
            'arranger':pricesort
        }
        pricerangeinfolist.append(pricerange)

    baseurl1='http://192.168.1.155:8000/laptop/hp/?csrfmiddlewaretoken=DVZEQm8tIIoHUIxw3QbZfVDxcQj2TgxyvTU3Ivd3TjLSesEJDjSEB30k7RFRCynj&lowerlimits='+lowerprice+'&'+'upperlimits='+upperprice
    p=requests.get(baseurl1,headers=headers)
    paisabachau=BeautifulSoup(p.content,'html.parser')
    paisabachausite=paisabachau.find_all('div',class_='post-box')
    for infos in paisabachausite:
        name=infos.find('h4').text
        image=infos.find('img')
        forwardpage=infos.find('a',class_='button-type')
        price=infos.find('h5',class_='priceheading').text
        pricesort=price.split('NPR')[1]
        pricesort=int(pricesort)

        pricerange={
            'name':name,
            'image':image['src'],
            'forwardpage0':forwardpage['href'],
            'price':price,
            'arranger':pricesort
        }
        pricerangeinfolist.append(pricerange)
    pricerangeinfolist=sorted(pricerangeinfolist,key=itemgetter('arranger'))
    count=len(pricerangeinfolist)
    baseurl1='http://192.168.1.155:8000/laptop/razerblade/?csrfmiddlewaretoken=DVZEQm8tIIoHUIxw3QbZfVDxcQj2TgxyvTU3Ivd3TjLSesEJDjSEB30k7RFRCynj&lowerlimits='+lowerprice+'&'+'upperlimits='+upperprice
    p=requests.get(baseurl1,headers=headers)
    paisabachau=BeautifulSoup(p.content,'html.parser')
    paisabachausite=paisabachau.find_all('div',class_='post-box')
    for infos in paisabachausite:
        name=infos.find('h4').text
        image=infos.find('img')
        forwardpage=infos.find('a',class_='button-type')
        price=infos.find('h5',class_='priceheading').text
        pricesort=price.split('NPR')[1]
        pricesort=int(pricesort)

        pricerange={
            'name':name,
            'image':image['src'],
            'forwardpage0':forwardpage['href'],
            'price':price,
            'arranger':pricesort
        }
        pricerangeinfolist.append(pricerange)
    pricerangeinfolist=sorted(pricerangeinfolist,key=itemgetter('arranger'))
    count=len(pricerangeinfolist)
    baseurl1='http://192.168.1.155:8000/laptop/apple/?csrfmiddlewaretoken=DVZEQm8tIIoHUIxw3QbZfVDxcQj2TgxyvTU3Ivd3TjLSesEJDjSEB30k7RFRCynj&lowerlimits='+lowerprice+'&'+'upperlimits='+upperprice
    p=requests.get(baseurl1,headers=headers)
    paisabachau=BeautifulSoup(p.content,'html.parser')
    paisabachausite=paisabachau.find_all('div',class_='post-box')
    for infos in paisabachausite:
        name=infos.find('h4').text
        image=infos.find('img')
        forwardpage=infos.find('a',class_='button-type')
        price=infos.find('h5',class_='priceheading').text
        pricesort=price.split('NPR')[1]
        pricesort=int(pricesort)

        pricerange={
            'name':name,
            'image':image['src'],
            'forwardpage0':forwardpage['href'],
            'price':price,
            'arranger':pricesort
        }
        pricerangeinfolist.append(pricerange)
    pricerangeinfolist=sorted(pricerangeinfolist,key=itemgetter('arranger'))
    count=len(pricerangeinfolist)
    try:
        filtered_data=[]
        if request.method=='GET':
            upperlimit=int(request.GET.get('upperlimits'))
            lowerlimit=int(request.GET.get('lowerlimits'))

        for infos in pricerangeinfolist:

            if infos['arranger'] >= lowerlimit and infos['arranger'] <= upperlimit:
                filtered_data.append(infos)
        count=len(filtered_data)
        return render(request, 'laptopbrand.html',{'ittinepal':filtered_data,'count':count})
    except:
        return render(request, 'laptopbrand.html',{'ittinepal':pricerangeinfolist,'count':count})


def mobile(request):
    return render(request,'mobile.html')
