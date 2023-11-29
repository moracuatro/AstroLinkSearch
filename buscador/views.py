from django.shortcuts import render
from django.template import Template, loader
from django.template import Context
import time
from buscadormini import buscadorweb

from django.http import HttpResponse
# Create your views here.
def procesar_busqueda(busqueda):
    # Dividir la cadena en palabras
    """listaTitulos = 
    listaUrls = 
    listaNPalabras = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    listaFrec = [6, 2, 4, 3, 6, 5, 6, 5, 17, 11]"""
    inicio = time.time()
    listaTitulos, listaUrls, listaNPalabras, listaFrec = buscadorweb(busqueda)
    #return listaTitulos, listaUrls, listaNPalabras, listaFrec
    fin = time.time() - inicio

    nresultados = len(listaTitulos)
    combinados = zip(listaTitulos, listaUrls, listaNPalabras, listaFrec)
    return combinados, fin, nresultados

def buscador(request): #cualquier normbre para la funcion

    if request.method == 'POST':
        busqueda = request.POST.get('busqueda', '')
        
        combinados, tiempo, nresultados = procesar_busqueda(busqueda)
        return render(request, 'buscador/index.html', {'combinados': combinados, 'tiempo': tiempo, 'nresultados': nresultados})

    return render(request, 'buscador/index.html')

def resultado (request, consulta):
    response = "Palabra buscada: %s."
    return HttpResponse(response % consulta)

def about(request):
    return HttpResponse('Acerca de mi: Manuel ALejandro MOra Meneses')

"""def buscar_resultados(request):
    
    template = loader.get_template('buscador/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


    if request.method == 'POST':
        busqueda = request.POST.get('busqueda', '')
        resultados = procesar_busqueda(busqueda)
        return render(request, 'buscador/index.html', {'resultados': resultados})

    return render(request, 'buscador/index.html')"""