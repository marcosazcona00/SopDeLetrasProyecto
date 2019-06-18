#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
import json
import random
 
def seleccionar_palabras(cantidad,lista,listaTipo,i,dicTipoPalabra,color):
    for k in range(cantidad):
        j=random.randrange(0,len(listaTipo))
        lista.append(listaTipo[j].lower())
        dicTipoPalabra[color].append(listaTipo[j].lower())
        listaTipo.pop(j)

def main_selector(dic):
    '''
        Este metodo nos va a devolver la lista de palabras que se van a distribuir en la grilla
        y un diccionario que contenga como clave eñ color de un tipo y como valores la lista de palabras para ese tipo
        ese diccionario luego va a usarse para verificar las palabras seleccionadas en la grilla
    '''
    with open('tipos.json','r') as file:
        archivo = json.load(file)
    #dic recibe esto {'Sustantivo':['color',cantidad de palabras]}
    listaPalabrasElegidas = []
    aux=[]
    dicPalabrasColor = dict()
    for i in dic:

        #i es el tipo: Sustantivo,adjetivo,verbo
        color = dic[i][0]
        dicPalabrasColor[color] = []
        print('Archivo[i]',archivo[i])
        seleccionar_palabras(int(dic[i][1]),listaPalabrasElegidas,archivo[i],i,dicPalabrasColor,color)
    return (listaPalabrasElegidas,dicPalabrasColor)
