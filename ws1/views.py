from django.shortcuts import render

import ws1.getReque as gR


def v_napster(request):
    rtex = gR.napster()
    return render(request, 'index.html', {'rtex': rtex, 'bro': 'napster'})


def v_shazam(request):
    rtex = gR.shazam()
    return render(request, 'index.html', {'rtex': rtex, 'bro': 'shazam'})


def v_deezer(request):
    rtex = gR.deezer()
    return render(request, 'index.html', {'rtex': rtex, 'bro': 'deezer'})


def v_spotifycharts(request):
    rtex = gR.spotifycharts()
    return render(request, 'index.html', {'rtex': rtex, 'bro': 'spotifycharts'})
    #return HttpResponse(rtex, content_type='text/html')  # .encode('cp1251')

def scra01(request):
    return render(request, 'index.html', {})

