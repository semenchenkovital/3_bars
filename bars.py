# -*- coding: utf-8 -*-
import json
import codecs
import math

    #{"bars":
    #[
    # {
    #  "Id":"ae3e9479-070f-4d66-9429-de3acd8427ac",
    #  "Number":1,
    #  "Cells":
    #          {
    #           "global_id":20660594,
    #           "Name":"Юнион Джек",
    #           "IsNetObject":"нет"
    #           "OperatingCompany":null,
    #           "AdmArea":"Центральный административный округ",
    #           "District":"Мещанский район",
    #           "Address":"Нижний Кисельный переулок, дом 3, строение 1",
    #           "PublicPhone":[{"PublicPhone":"(495) 621-19-63"}],
    #           "SeatsCount":30,"SocialPrivileges":"нет",
    #           "geoData":
    #                     {
    #                      "type":"Point",
    #                      "coordinates":[37.621587946152012,55.765366956608361]
    #                      }
    #           }
    #  }
    #]
    #}

def load_data(filepath):
    infile=codecs.open(filepath,'r', 'utf-8-sig').read()
    jsondata = json.loads(infile)
    jsondata2 = json.load(infile)
    print (jsondata['bars'][0])
    return jsondata
        

def get_biggest_bar(data):
    
    SeatsCountmax = 0
    for bars in data['bars']:
        if bars['Cells']['SeatsCount'] > SeatsCountmax :
           SeatsCountmax = bars['Cells']['SeatsCount']
    for bars in data['bars']:
        if bars['Cells']['SeatsCount'] == SeatsCountmax :
           print ("Больше всего мест в баре:",bars['Cells']['Name']," Мест:",bars['Cells']['SeatsCount'])
    return SeatsCountmax       


def get_smallest_bar(data,SeatsCountmax):
    for bars in data['bars']:
        if bars['Cells']['SeatsCount'] < SeatsCountmax and bars['Cells']['SeatsCount'] != 0:
           SeatsCountmax = bars['Cells']['SeatsCount'] 
    for bars in data['bars']:
        if bars['Cells']['SeatsCount'] == SeatsCountmax :
           print ("Меньше всего мест в баре:",bars['Cells']['Name']," Мест:",bars['Cells']['SeatsCount'])
    for bars in data['bars']:
        if bars['Cells']['SeatsCount'] == 0:
           print ("Мест нет в баре:",bars['Cells']['Name']," Мест:",bars['Cells']['SeatsCount'])
           


def get_closest_bar(data, longitude, latitude, dist,name):
    #pi - число pi, rad - радиус сферы (Земли)
    rad = 6372795
    #координаты точки отсчета 
    llat1 = float(latitude)
    llong1 = float(longitude)
    #в радианах
    lat1 = llat1*math.pi/180.
    long1 = llong1*math.pi/180.
    
    #косинусы и синусы широты и разницы долготы
    cl1 = math.cos(lat1)
    sl1 = math.sin(lat1)
    min_closest = dist
    for bars in data['bars']:
        #координаты второй точки
        llong2 = float(bars['Cells']['geoData']['coordinates'][0])
        llat2 = float(bars['Cells']['geoData']['coordinates'][1])
        

        #в радианах
        long2 = llong2*math.pi/180.
        lat2 = llat2*math.pi/180.

        #косинусы и синусы широт и разницы долгот
        cl2 = math.cos(lat2)
        sl2 = math.sin(lat2)
        delta = long2 - long1
        cdelta = math.cos(delta)
        sdelta = math.sin(delta)

        #вычисления длины большого круга
        y = math.sqrt(math.pow(cl2*sdelta,2)+math.pow(cl1*sl2-sl1*cl2*cdelta,2))
        x = sl1*sl2+cl1*cl2*cdelta
        ad = math.atan2(y,x)
        dist = ad*rad
        if dist < min_closest:
           min_closest = dist
           name = bars['Cells']['Name'] 
                      
    print ("Ближайший бар:",name, " находиться на расстоянии:",round(min_closest)," метров")

def get_closest_bar0(data, longitude, latitude):
    #pi - число pi, rad - радиус сферы (Земли)
    rad = 6372795
    #координаты точки отсчета 
    llat1 = float(latitude)
    llong1 = float(longitude)
    #в радианах
    lat1 = llat1*math.pi/180.
    long1 = llong1*math.pi/180.
    
    #косинусы и синусы широты и разницы долготы
    cl1 = math.cos(lat1)
    sl1 = math.sin(lat1)

    
    bars = data['bars'][0]
    #координаты второй точки
    llong2 = float(bars['Cells']['geoData']['coordinates'][0])
    llat2 = float(bars['Cells']['geoData']['coordinates'][1])
    name = bars['Cells']['Name']  

    #в радианах
    long2 = llong2*math.pi/180.
    lat2 = llat2*math.pi/180.

    #косинусы и синусы широт и разницы долгот
    cl2 = math.cos(lat2)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    #вычисления длины большого круга
    y = math.sqrt(math.pow(cl2*sdelta,2)+math.pow(cl1*sl2-sl1*cl2*cdelta,2))
    x = sl1*sl2+cl1*cl2*cdelta
    ad = math.atan2(y,x)
    dist = ad*rad
    return dist,name

    


if __name__ == '__main__':
    jsondata = load_data ('бары.json')
    SeatsCountmax = get_biggest_bar(jsondata)
    get_smallest_bar(jsondata,SeatsCountmax)
    longitude = float(input("Введите долготу точки:"))
    latitude = float(input("Введите широту точки:"))
    dist,name = get_closest_bar0(jsondata, longitude, latitude)
    get_closest_bar(jsondata, longitude, latitude,dist,name)
    
