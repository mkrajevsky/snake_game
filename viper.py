#------------importy ---------------------
import time,random
from turtle import *

#---------poczatkowe zalozenia-------------
"""
GRA jest sterowana strzałkami, konczy sie gdy dzdzownica wejdzie w siebie 
uderzy w kamien lub wyjdzie poza pole gry. Plansza sklada sie z 5 typów obiektow:
-puste pole "p"
-kamien     "k"
-jedzenie   "j"
-glowa      "g"
-dzdzownica "d"

Plansza jest odwrotna z polem mianowicie :
dla takiej planszy 
[["p","g","p"],
 ["k","p","p"]
 ["p","j","p"]]
np obiekt "g" to plansza[0][1]
na ekranie będzie tak wsp_g = 1 , 0 
 p  j  p
 k  p  p 
 p  g  p 
 Żeby wyjść należy nacisnąc q potem klinknąć w ekran
Grę można dodatkowa pauzowac na 10 s 
"""


#------------Stale w grze ---------------------------
s = {"szer_okna": 800, "wys_okna": 950, "szer_planszy": 800, "wys_planszy": 900, "margines_dol":50,
            "l_kol":40 ,"l_wier":40, "l_kamieni": 100, "l_jedzenia": 20,
            "kolor_tla": "papaya whip", "tytul gry": "gra - dzdzowmica"  }
szer_kratki, wys_kratki = s["szer_planszy"]/s["l_kol"],s["wys_planszy"]/s["l_wier"]
pressed_key =""
#-----------do komunikatow ---------
polx,poly = s["szer_okna"] // 3, s["margines_dol"] / 3
srod_x,srod_y = s["szer_okna"]//2,s["wys_okna"]//2
#------------------okno gry----------------

def okn0(szer_okna,wys_okna,tytul,kolor_tla):
    global okno
    okno = Screen()
    okno.title(tytul)
    okno.bgcolor(kolor_tla)
    okno.setup(width=szer_okna, height=wys_okna)
    okno.tracer(0)
    # dopasowywanie współrzędnych lewy dolny róg to 0,0
    setworldcoordinates(0, 0, szer_okna, wys_okna)

#--------------------------rysowanie kratek na tlo --------
def tlo0(szer_plaszy, wys_planszy,liczba_wierszy,liczba_kolumn, kolor_kratek, margines_dol):

    global tlo
    tlo=Turtle()
    tlo.hideturtle()
    tlo.goto(0, margines_dol)
    tlo.pencolor(kolor_kratek)
    for i in range(liczba_kolumn+1):
        tlo.lt(90)
        tlo.fd(wys_planszy)
        tlo.rt(180)
        tlo.fd(wys_planszy)
        tlo.lt(90)
        tlo.fd(szer_plaszy // liczba_kolumn)
    tlo.penup()
    tlo.goto(0,margines_dol)
    tlo.pendown()
    tlo.seth(90)
    for i in range(liczba_wierszy+1):
        tlo.rt(90)
        tlo.fd(szer_plaszy)
        tlo.rt(180)
        tlo.fd(szer_plaszy)
        tlo.seth(90)
        tlo.fd(wys_planszy / liczba_wierszy)
    tlo.fillcolor("PaleTurquoise3")
    tlo.begin_fill()
    tlo.seth(0)
    tlo.goto(0,0)
    tlo.fd(szer_plaszy)
    tlo.lt(90)
    tlo.fd(margines_dol)
    tlo.lt(90)
    tlo.fd(szer_plaszy)
    tlo.lt(90)
    tlo.fd(margines_dol)
    tlo.end_fill()




#--------------pokazuje odpowiednie komunikaty -------
def komunikaty(czy_poczatek,wynik,pol_x,pol_y,sek):
    global komunikator
    if czy_poczatek=="poczatek":
        komunikator = Turtle()
        komunikator.speed(0)
        komunikator.shape("square")
        komunikator.color("white")
        komunikator.penup()
        komunikator.hideturtle()
        komunikator.goto(pol_x, pol_y)
        komunikator.write(f"by zaczac nacisnij stralke", align="center",
                          font=("Consoles", 22, "bold"))
    elif czy_poczatek == "gra":
        komunikator.clear()
        komunikator.write(f"twoj wynik to {wynik}", align="center",
                          font=("Consoles", 22, "bold"))
    elif czy_poczatek == "pauza":
        komunikator.clear()

        komunikator.goto(s["szer_okna"]//2,s["wys_okna"]//2)
        komunikator.write(f"Gra zapauzowana, pozostało {sek} sek", align="center",
                          font=("Consoles", 40, "bold"))
        komunikator.goto(pol_x,pol_y)
    elif czy_poczatek =="koniec":
        komunikator.clear()
        koniec = Turtle()
        koniec.speed(0)
        koniec.shape("square")
        koniec.color("black")
        koniec.penup()
        koniec.hideturtle()
        koniec.goto(srod_x, srod_y)
        koniec.write(f"Koniec gry, wynik: {wynik}",align="center",
                          font=("Consoles", 60, "bold"))
        done()
    elif czy_poczatek =="zakonczenie":
        komunikator.clear()
        komunikator.write(f"Zakończyłeś grę z wynikiem: {wynik}, kliknij by wyjść", align="center",
                          font=("Consoles", 22, "bold"))




# ------------ czy gra powinna się zakonczyć -------
# jeden  warunek jest w funkcji poruszanie
# te zwiazany z wejsciem dzownicy w sama siebie
def czy_nie_koniec(plansza,glowa,wynik):
    if any([ plansza[glowa[1]][glowa[0]]=="k",
            glowa[0]<0,glowa[1]<0, glowa[0]>s["l_wier"],glowa[1]>s["l_kol"]]):
        komunikaty("koniec",wynik,polx,poly)
        return False
    return True
#------------------tworzenie obiektow na planszy + sprawdzanie czy nie ma tam juz czegos-----
def stworz_obiekty(plansza,liczba,symbol):
    for i in range(liczba):
        x = random.randint(0, len(plansza[0]) - 1)
        y = random.randint(0, len(plansza) - 1)
        while plansza[y][x] != "p":
            x = random.randint(0, len(plansza[0]) - 1)
            y = random.randint(0, len(plansza) - 1)
        plansza[y][x] = symbol
    return plansza
#-----------pomocnicza funkcja do kolorowania kratek-----
def rysujacy_prost():
    global prost
    prost = Turtle()
rysujacy_prost()
def kolko(pole, kolor, szer_kratki, wys_kratki, margines_dol):
    prost.goto(pole[0] * szer_kratki+szer_kratki, margines_dol + pole[1] * wys_kratki+wys_kratki//2)
    prost.fillcolor(kolor)
    prost.begin_fill()
    prost.circle(min(szer_kratki,wys_kratki)//2)
    prost.end_fill()

def prostokat(pole, kolor, szer_kratki, wys_kratki, margines_dol):
    prost.penup()
    prost.goto(pole[0] * szer_kratki, margines_dol + pole[1] * wys_kratki)
    prost.setheading(90)
    prost.pendown()
    prost.fillcolor(kolor)
    prost.begin_fill()
    prost.fd(wys_kratki)
    prost.rt(90)
    prost.fd(szer_kratki)
    prost.rt(90)
    prost.fd(wys_kratki)
    prost.rt(90)
    prost.fd(szer_kratki)
    prost.rt(90)
    prost.end_fill()
    prost.penup()
    prost.hideturtle()
#----------------samo rysowanie planszy-----------
def rysuj_plansze(plansza, szer_kartki, wys_kratki, margines_dol):
    prost.clear()
    for i in range(len(plansza)):
        for j in range(len(plansza[0])):
            if plansza[i][j] == "k":
                prostokat((j, i), "tomato2", szer_kartki, wys_kratki, margines_dol)
            elif plansza[i][j] == "d":
                prostokat((j, i), "PaleVioletRed1", szer_kartki, wys_kratki, margines_dol)
            elif plansza[i][j] == "j":
                prostokat((j, i), "PaleGreen2", szer_kartki, wys_kratki, margines_dol)
            elif plansza[i][j] == "g":
                prostokat((j, i), "PaleVioletRed4", szer_kartki, wys_kratki, margines_dol)
                kolko((j,i), "lightblue", szer_kratki, wys_kratki, margines_dol)

        """
            elif plansza[i][j] == "p":
                prostokat((j, i), s["kolor_tla"], szer_kartki, wys_kratki, margines_dol)
        """


# ---------- 4 funkcje odpowiadajace za kierunek -------------
def go_up1():
    global kierunek
    if kierunek != "down":
        kierunek = "up"


def go_down():
    global kierunek
    if kierunek != "up":
        kierunek = "down"


def go_left():
    global kierunek
    if kierunek != "right":
        kierunek = "left"


def go_right():
    global kierunek
    if kierunek != "left":
        kierunek = "right"
# obsluga wyjscia z gry za pomoca q
def wyjscie_z_gry():

    komunikaty("zakonczenie",wynik, polx,poly,0)
    time.sleep(1)
    okno.exitonclick()

# obsluga pauzy
def pauza():
    i=5
    while i >0:
        komunikaty("pauza", wynik, polx, poly,i)
        i-=1
        time.sleep(1)

# ----------- glowna funkcja z=odpowiadajaca za poruszanie --------
def poruszanie(glowa,dzdzownica,plansza,wynik):
    x_glowy, y_glowy = glowa
    ostatni_segment = glowa if dzdzownica==[] else dzdzownica[-1]
    #------ ten blok zmienia polozenie glowy w zaleznosci od kierunku
    if kierunek == "up":
        x,y= glowa
        glowa = (x,y+1)
    elif kierunek == "down":
        x,y= glowa
        glowa = (x,y-1)
    elif kierunek == "right":
        x,y= glowa
        glowa = (x+1,y)
    elif kierunek == "left":
        x,y= glowa
        glowa = (x-1,y)
    #sprawdza czy nowe pole nie jest kamieniem i czy dzdzownica nie jest poza
    if not (0<=glowa[1]<s["l_wier"] and 0<=glowa[0]<s["l_kol"])\
            or plansza[glowa[1]][glowa[0]]=="k":
        #jeśli jest to konczy gre
        komunikaty("koniec",wynik,polx,poly,0)

    if dzdzownica !=[]:
        dzdzownica = [(x_glowy,y_glowy)] + dzdzownica[:-1]
        plansza[y_glowy][x_glowy]="d"
    # gdy dzdzownica zje
    if plansza[glowa[1]][glowa[0]]=="j":
        stworz_obiekty(plansza , 1 , "j")
        wynik += 1
        dzdzownica.append(ostatni_segment)
    else:
        plansza [ostatni_segment[1]][ostatni_segment[0]]="p"


    if plansza[glowa[1]][glowa[0]]=="d":
        komunikaty("koniec",wynik,polx,poly,0)
    #na sam koniec ustawia nowe pole na g żeby wszystkie warunki zadzialaly przed
    plansza[glowa[1]][glowa[0]] = "g"
    return glowa,dzdzownica,plansza,wynik
#----------Obsluga klawiatury ----------------
kierunek = ""

def komendy():
    okno.listen()
    okno.onkeypress(go_up1, "Up")
    okno.onkeypress(go_down, "Down")
    okno.onkeypress(go_left, "Left")
    okno.onkeypress(go_right, "Right")
    okno.onkeypress(wyjscie_z_gry,"q")
    okno.onkeypress(pauza, "p")

def main():

    #pusta plansza
    plansza = [["p" for i in range(s["l_kol"])] for j in range(s["l_wier"])  ]
    #glowa w losowym miejscu
    glowa = random.randint(0,s["l_wier"]-1),random.randint(0,s["l_kol"]-1)
    plansza[glowa[1]][glowa[0]] = "g"

    dzdzownica = []
    global wynik
    wynik = 0
    delay = 0.07
    #--------- tworzenie kamieni na planszy
    plansza = stworz_obiekty(plansza,s["l_kamieni"],"k")
    # --------- tworzenie jedzenia na planszy
    plansza = stworz_obiekty(plansza, s["l_jedzenia"], "j")

    okn0(s["szer_okna"], s["wys_okna"],s["tytul gry"], s["kolor_tla"])
    tlo0(s["szer_planszy"], s["wys_planszy"], s["l_wier"], s["l_kol"], "black",
         s["margines_dol"])

    komunikaty("poczatek", wynik, polx, poly,0)
    #rozpoznaje nacusniety klawisz
    komendy()
    czy = True

    while czy:
        okno.update()
        czy = czy_nie_koniec(plansza, glowa, wynik)
        rysuj_plansze(plansza,szer_kratki,wys_kratki,s["margines_dol"])
        komunikaty("gra", wynik, polx, poly,0)
        glowa, dzdzownica, plansza, wynik = poruszanie(glowa,dzdzownica,plansza,wynik)
        delay = 0.07 - wynik/10000
        time.sleep(delay)



if __name__ == '__main__':
    main()















