##################################### From last project ########################

def temperature(a):
    temperature = a[a.find('temp_f'): a.find('temp_c')]
    temperature = "Temperature now = " + temperature[8:12]
    return temperature

def winds(a):
    wind = a[a.find('wind_string'): (a.find ('"wind_dir') - 5)]
    wind = "Winds today = " + wind[14:]
    return wind

def rainfall (a):
    rain = a[a.find('precip_today_string'): (a.find('precip_today_in') - 6)]
    rain = "Rainfall today = " + rain[22:]
    return rain

def today (a):
    list = a.split ('period')
    today = list[1][list[1].find('title') + 8:list[1].find('fcttext') - 6]
    return '(' + today + ')'

def tomorrow (a):
    list = a.split ('period')
    tomorrow = list[3][list[3].find('title') + 8:list[3].find('fcttext') - 6]
    return '(' + tomorrow + ')'

def datomorrow (a):
    list = a.split ('period')
    datomorrow = list[5][list[5].find('title') + 8:list[5].find('fcttext') - 6]
    return '(' + datomorrow + ')'

def edtomorrow (a):
    list = a.split ('period')
    edtomorrow = list[7][list[7].find('title') + 8:list[7].find('fcttext') - 6]
    return '(' + edtomorrow + ')'

def stat (a,b):
    list = a.split ('period')
    stat = list[b][list[b].find('fcttext') + 10: list[b].find('fcttext_metric') - 6]
    return stat

def img (a,b):
    list = a.split ('period')
    img = list[b][list[b].find('icon_url') + 11: list[b].find('title') - 6]
    return img

