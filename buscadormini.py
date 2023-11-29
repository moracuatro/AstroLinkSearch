import nltk
from nltk import SnowballStemmer
from nltk.tokenize import word_tokenize
import json
from nltk.corpus import stopwords
import time
import requests
from bs4 import BeautifulSoup

datos = json.dumps({})
try: 
    with open('indexraiz.txt', 'r', encoding='utf-8') as file:
        datos = json.load(file)
except (e):
    print(e)

nltk.download('punkt')
nltk.download('stopwords')

def obtener_titulo_con_header(url):
    try:
        # Definir un encabezado (User-Agent) para simular una solicitud desde un navegador
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        # Realizar la solicitud GET a la URL con el encabezado definido
        response = requests.get(url) #, headers=headers

        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Utilizar BeautifulSoup para analizar el contenido HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Encontrar la etiqueta <title> que contiene el título de la página
            title_tag = soup.find('title')

            # Verificar si se encontró la etiqueta <title>
            if title_tag:
                return title_tag.text.strip()
            else:
                return "No se encontró la etiqueta <title>."

        else:
            return f"Error al obtener la página. Código de estado: {response.status_code}"

    except Exception as e:
        return f"Error: {e}"    
    
    
def buscadorweb(text):
    i=0
    try:
        # Obtener la lista de conectores en español
        conectores = set(stopwords.words('spanish'))

        spanish_stemmer = SnowballStemmer('spanish')


        # Tokenizar el texto
        tokens = word_tokenize(text, language='spanish')

        # Eliminar los conectores
        tokens_sin_conectores = [token for token in tokens if token.lower() not in conectores]

        # Unir los tokens para obtener el texto sin conectores
        texto_sin_conectores = ' '.join(tokens_sin_conectores)

        # Tokenizar el texto sin conectores
        tokens = word_tokenize(texto_sin_conectores, language='spanish')

        # Aplicar el stemmer a cada token
        stems = [spanish_stemmer.stem(token) for token in tokens]

        # Buscar las palabras en el atributo "palabra"
        palabras_encontradas = {}

        for entrada in datos:
            palabra_actual = entrada.get("palabra", "").lower()  # Obtener la palabra en minúsculas
            if palabra_actual in stems:
                if palabra_actual not in palabras_encontradas:
                    palabras_encontradas[palabra_actual] = {"frecuencia_url": {}}
                frecuencia_url = entrada.get("frecuencia_url", {})
                palabras_encontradas[palabra_actual]["frecuencia_url"].update(frecuencia_url)

        # Convertir las claves de palabras_encontradas a una lista
        palabras_lista = list(palabras_encontradas.keys())

        # Encontrar URLs que contienen una o más palabras y contar cuántas palabras coinciden
        urls_coincidentes = {}
        for palabra in palabras_lista:
            frecuencia_url = palabras_encontradas[palabra]["frecuencia_url"]
            urls_coincidentes[palabra] = [url for url, frecuencia in frecuencia_url.items() if frecuencia > 0]

        # Crear un diccionario para contar la cantidad de palabras por URL
        cont_palabras_por_url = {}
        interseccion_urls = set(urls_coincidentes[palabras_lista[0]])
        for url in interseccion_urls:
            num_palabras_coincidentes = sum(1 for urls in urls_coincidentes.values() if url in urls)
            cont_palabras_por_url[url] = num_palabras_coincidentes

        # Ordenar las URLs por la cantidad de palabras coincidentes
        #urls_ordenadas = sorted(cont_palabras_por_url.items(), key=lambda x: (x[1], suma_frecuencias[x[0]]), reverse=True)
        urls_ordenadas = sorted(cont_palabras_por_url.items(), key=lambda x: x[1], reverse=True)

        # Imprimir la URL junto con el número de palabras coincidentes
        urllist = []
        titulos = []
        urls = []
        numpalabras = []
        frecuencias = []
        for url, num_palabras in urls_ordenadas:
            
            
            try: 
                titulos.append(obtener_titulo_con_header(url))
            except:
                titulos.append("Error al obtener nombre")
            urls.append(url)
            numpalabras.append(num_palabras)
            ###
            suma_frecuencias = 0

            # Itera sobre cada marca en los datos
            for marca, info in palabras_encontradas.items():
                # Obtén la frecuencia_url para la marca actual
                frecuencia_url = info.get('frecuencia_url', {})

                # Suma la frecuencia para la URL objetivo si está presente
                suma_frecuencias += frecuencia_url.get(url, 0)
            ###
            frecuencias.append(suma_frecuencias)
            i = i+1
            if i == 10:
                break
                
        if all(valor == numpalabras[0] for valor in numpalabras):
            print("Son iguales acomodalas")
            combinadas = list(zip(titulos, urls, numpalabras, frecuencias))

            # Ordenar la lista combinada por los valores
            combinadas_ordenadas = sorted(combinadas, key=lambda x: x[3], reverse = True)

            # Descombinar las listas ordenadas
            titulos, urls, numpalabras, frecuencias = zip(*combinadas_ordenadas)
        return titulos, urls, numpalabras, frecuencias
    except:
        return [], [], [], []