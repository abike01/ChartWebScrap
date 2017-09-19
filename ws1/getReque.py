import json
import time

import requests
from bs4 import BeautifulSoup

from lxml import html
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

def napster():
    url = 'http://de.napster.com/chart/tracks'
    sess = requests.Session()
    request = sess.get(url)
    #    r = requests.get(url)
    return napster_load(request)


def napster_load(request):
    soup = BeautifulSoup(request.text)
    el_list = soup.find('ul', {'class': 'track-list js-track-list feature-module'})
    items_list = []
    items = el_list.find_all('li', {'class': 'js-track-item track-item'})

    for item in items:
        item_m = {'album_id': item.get('album_id')}
        item_m['album_name'] = item.get('album_name')
        item_m['album_shortcut'] = item.get('album_shortcut')
        item_m['Art_230124592'] = item.get('Art.230124592')
        item_m['artist_name'] = item.get('artist_name')
        item_m['artist_shortcut'] = item.get('artist_shortcut')
        item_m['duration'] = item.get('duration')
        item_m['genre_id'] = item.get('genre_id')
        item_m['href'] = item.get('href')
        item_m['preview_url'] = item.get('preview_url')
        item_m['right_flags'] = item.get('right_flags')
        item_m['track_id'] = item.get('track_id')
        item_m['track_name'] = item.get('track_name')
        item_m['track_shortcut'] = item.get('track_shortcut')
        item_m['track_type'] = item.get('track_type')
        items_list.append(item_m)

    jres = json.dumps(items_list, indent=2)
    return jres


def shazam():
    url = 'https://www.shazam.com/charts/top-100/germany'
    return shazam_load(url)  # napster_load(url, s)


def shazam_load(url):
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    driver = webdriver.Firefox(capabilities=firefox_capabilities)

    driver.get(url)
    time.sleep(3)

    items_list = []
    Listok = driver.find_element_by_xpath("//ul[@class='tracks shz-ux-showmoreless']");
    Lis = Listok.find_elements_by_tag_name('article')

    for item in Lis:
        item_m = {'track_id': item.get_attribute('data-track-id')}
        pnumber = item.find_element_by_xpath(".//span[@class='number']")
        item_m['number'] = pnumber.get_attribute('innerHTML')

        item_m['shz_audio_url'] = item.get_attribute('data-shz-audio-url')
        item_m['shz_beacon'] = item.get_attribute('data-shz-beacon')
        item_m['itemscopen'] = item.get_attribute('itemscope')

        item_m['itemtype'] = item.get_attribute('itemtype')

        title = item.find_element_by_xpath(".//meta[@itemprop='name']")
        item_m['title'] = title.get_attribute('content')

        artist = item.find_element_by_class_name('artist')
        item_m['artist'] = artist.get_attribute('data-track-artist')

        ellip = artist.find_element_by_class_name('ellip')
        item_m['artist_text'] = ellip.get_attribute('innerHTML')

        item_m['artist_href'] = ellip.get_attribute('href')

        num = item.find_element_by_class_name('num')
        item_m['num'] = str(num.get_attribute('innerHTML')).replace('&nbsp;','')

        #        driver.execute_script("arguments[0].setAttribute('class','vote-link up voted')", element)
        #print('get_attribute: ', item.get_attribute('id'))  # article.get_attribute('id')
        #print('data-track-id: ', item.get_attribute('data-track-id'))
        #print('data-shz-audio-url: ', item.get_attribute('data-shz-audio-url'))
        #print('data-shz-beacon: ', item.get_attribute('data-shz-beacon'))
        #print('itemscopen: ', item.get_attribute('itemscope'))
        #print('itemtype: ', item.get_attribute('itemtype'))

        #title = item.find_element_by_class_name('title')
        #print('title.text: ', title.get_attribute('content'))
        #artist = item.find_element_by_class_name('artist')
        #print('artist.data-track-artist: ', artist.get_attribute('data-track-artist'))
        #ellip = artist.find_element_by_class_name('ellip')
        #print('artist.text: ', ellip.get_attribute("innerHTML"))
        #print('artist.href: ', ellip.get_attribute("href"))
        #num = item.find_element_by_class_name('num')
        #print('num: ', num.get_attribute("innerHTML"))

        items_list.append(item_m)
    jres = json.dumps(items_list, indent=2, sort_keys=True)
    time.sleep(2)
    driver.close()
    return jres


def spotifycharts():
    url = 'http://spotifycharts.com/regional/de/daily/2017-08-27'
    sess = requests.Session()
    request = sess.get(url)
    return spotifycharts_load(request)


def spotifycharts_load(request):
    soup = BeautifulSoup(request.text)
    el_list = soup.find("table", {"class": "chart-table"})

    items_list = []
    items = el_list.find_all('tr')

    for item in items:
        chart_position = item.find('td', {'class': 'chart-table-position'})
        item_m = {'chart_position': getTagContent(chart_position, '')}

        track = item.find('td', {'class': 'chart-table-track'})
        item_m['track_strong'] = getTagContent(track, 'strong')
        item_m['track_span'] = getTagContent(track, 'span')

        streams = item.find('td', {'class': 'chart-table-streams'})
        item_m['track_streams'] = getTagContent(streams, '')

        if(item_m['chart_position'] != ''):
            items_list.append(item_m)

    jres = json.dumps(items_list, indent=2, sort_keys=True)
    return jres


def getTagContent(tdgStr, nen):
    if nen == '':
        rets = str(tdgStr).partition('>')[2].partition('</')[0]
    else:
        rets = str(tdgStr).partition('<' + nen + '>')[2].partition('</' + nen + '>')[0]
    return rets


def deezer():
    url = 'http://www.deezer.com/es/playlist/1111143121'
    #    sess = requests.Session()
    #    request = sess.get(url)
    #    print(sess.headers)
    # var PLAYER_INIT =
    # window.__DZR_APP_STATE__
    # find_elements(by='id', value=None)

    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    driver = webdriver.Firefox(capabilities=firefox_capabilities)

    driver.get(url)
    '''
    bodyc = driver.find_element_by_tag_name('body')
    bodyc.send_keys(Keys.COMMAND + '-')
    bodyc.click()
    '''
    time.sleep(3)
    items_list = []

    #    driver.execute_script("document.body.style.zoom = 'scale(0.5)'") #window.parent.document.body.style.zoom
    Lis = driver.find_elements_by_xpath("//div[@class='datagrid-row song active paused']")
    deezer_load(Lis, items_list)

    Lis = driver.find_elements_by_xpath("//div[@class='datagrid-row song']")
    deezer_load(Lis, items_list)

    driver.execute_script("window.scrollBy(0, document.body.scrollHeight*2);")
    time.sleep(2)
    Lis = driver.find_elements_by_xpath("//div[@class='datagrid-row song']")
    deezer_load(Lis, items_list)

    driver.execute_script("window.scrollBy(0, document.body.scrollHeight*2);")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight*2);")
    time.sleep(2)

    Lis = driver.find_elements_by_xpath("//div[@class='datagrid-row song']")
    deezer_load(Lis, items_list)

    driver.execute_script("window.scrollBy(0, -document.body.scrollHeight);")
    time.sleep(2)

    driver.execute_script("window.scrollBy(0, document.body.scrollHeight*0.44);")
    time.sleep(2)

    Lis = driver.find_elements_by_xpath("//div[@class='datagrid-row song']")
    deezer_load(Lis, items_list)

    '''
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % paiz)
    divL = driver.find_element_by_id('dzr-app');
#    driver.execute_script("document.body.style.webkitTransform  = 'scale(0.25)'")
#    intofile(driver.execute_script("return PLAYER_INIT;"),'PLAYER_INIT')
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % 0.30)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % 0.1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
#    bef= driver.execute_script(
#        "return window.getComputedStyle(document.querySelector('.SomeTitle .bar'),':before').getPropertyValue('content')")
#    print(bef)
#    print(driver.get_cookies())
#    print('session_id: ',driver.session_id)
    #div.datagrid - row: nth - child(2)
    '''
    time.sleep(3)
    driver.close()
    jres = json.dumps(items_list, indent=2)
    return jres


def deezer_load(Lis, items_list):
    for item in Lis:
        item_m = {'data_key': item.get_attribute('data-key')}
        number = item.find_element_by_xpath(".//span[@class='datagrid-track-number']")
        item_m['number'] = number.text
        Cancion = item.find_element_by_xpath(".//a[@class='datagrid-label datagrid-label-main title']")
        item_m['cancion'] = Cancion.text
        artista = item.find_element_by_xpath(".//a[@class='datagrid-label datagrid-label-main']")
        item_m['artista'] = artista.text
        album = item.find_element_by_xpath(".//div[@class='datagrid-cell cell-album']")
        album = album.find_element_by_xpath(".//a[@class='datagrid-label datagrid-label-main']")
        item_m['album'] = album.text
        duration = item.find_element_by_xpath(".//span[@class='datagrid-label datagrid-label-idle ellipsis']")
        item_m['duration'] = duration.text
        if item_m not in items_list:
            items_list.append(item_m)
    return items_list.sort(key=lambda x: int(x['number']))


def intofile(item, fname):
    with open(fname, 'w') as output_file:
        output_file.write(str(item))  # .encode('cp1251')


def XPathf():
    test = '''
        <html>
            <body>
                <div class="first_level">
                    <h2 align='center'>one</h2>
                    <h2 align='left'>two</h2>
                </div>
                <h2>another tag</h2>
            </body>
        </html>
    '''
    tree = html.fromstring(test)

    tree.xpath('//h2')  # все h2 теги
    tree.xpath('//h2[@align]')  # h2 теги с атрибутом align
    tree.xpath('//h2[@align="center"]')  # h2 теги с атрибутом align равным "center"
    print(tree.xpath('//h2[@align="center"]'))

    div_node = tree.xpath('//div')[0]  # div тег
    print(tree.xpath('//div'))
    div_node.xpath('.//h2')  # все h2 теги, которые являются дочерними div ноде
