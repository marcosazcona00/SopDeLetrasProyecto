#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
class Celda:
    def __init__(self):
        self.__coordenada_inf = ()
        self.__coordenada_sup = ()
        self.__letra = ' '
        self.__color= 'white'
        self.__color_auxiliar = self.__color


    def set_coordenada_sup(self,pos_sup):
        self.__coordenada_sup = pos_sup

    def set_coordenada_inf(self,pos_inf):
        self.__coordenada_inf = pos_inf

    def set_letra(self,l):
        self.__letra =l

    def set_color(self,c):
        ok = False
        if(self.__color==self.__color_auxiliar):
            self.__color=c
            ok=True
        elif(c==self.__color):
            self.__color=self.__color_auxiliar
            ok = True
        return ok

    def get_coordenada(self):
        return (self.__coordenada[0],self.__coordenada[1])

    def get_letra(self):
        return self.__letra

    def get_color(self):
        return self.__color

    def draw_cell(self,graph):
        celda=graph.DrawRectangle(self.__coordenada_sup,self.__coordenada_inf,fill_color=self.__color,line_color='black')
        graph.DrawText(self.__letra,((-11 + self.__coordenada_inf[0]),(-11 + self.__coordenada_inf[1])),font='Arial 15') #Se mueve cada 24 sobre el x
