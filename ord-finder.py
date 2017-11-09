def file_2_list(ordfil):
    # INN: navn på ei fil som antas å inneholde ei ordliste,
    #      ett ord per linje i fila
    # UT: returnerer samme ordliste som ei liste
    # Dropper unntaksbehandling for at programmet ikke skal bli for langt
    fil = open(ordfil, 'r', encoding='utf-8-sig')
    ordliste =[ ]
    for linje in fil:
        ordliste.append(linje.strip())
    fil.close()
    return ordliste
        
primes = {'e':2, 't':3, 'r':5, 's':7, 'n':11, 'a':13, 'i':17,
          'l':19, 'o':23, 'g':29, 'k':31, 'd':37, 'm':41, 'å':43,
          'v':47, 'f':53, 'b':59, 'u':61, 'p':67, 'h': 71, 'j':73,
          'ø':79, 'y':83, 'æ':89, 'c':97, 'q':101, 'w': 103,
          'x':107, 'z':109, 'ü': 113} # et par ord med ü i nsf-fila

def string_2_key(streng):
    # INN: en streng av små bokstaver (et ord på norsk)
    # UT: returnerer et heltall som er et produkt av primtall for,
    #     bokstavene som inngår i ordet, som gitt i dictionary primes
    produkt = 1
    for tegn in streng: # går i løkke tegn for tegn i ordet
        if tegn in primes.keys():
            produkt *= primes[tegn] # og ganger inn primtall for hvert tegn
    return produkt

def list_2_dic(liste):
    # INN: Ei liste med ord
    # UT: dictionary hvor ordene er samlet på hver sin anagramnøkkel
    #     f.eks. {6:['et','te'], 10:['er','re'], 14: ['es', 'se'], ...}
    #     fordi e, t, r og s har verdier hhv. 2, 3, 5 og 7 som ganges sammen
    dic = { } # oppretter en tom dictionary
    for w in liste: # ser på ett og ett ord (w) i lista
        key = string_2_key(w) # finner tallnøkkel for ordet
        if key in dic: # har allerede andre ord m samme nøkkel
            dic[key].append(w)
        else: # ordet er det første vi finner med denne nøkkelen
            dic[key] = [w]
    return dic

def finn_anagram(dic, streng):
    # INPUT (param.) en dictionary (dic) og en tallverdi (verdi)
    # PROS.: ser om det fins et oppslag med nøkkel=verdi i dictionary
    # OUTPUT: returerer lista av ord for nøkkelen, tom liste hvis ingen match
    verdi = string_2_key(streng.lower()) # må ha små bokst for å regne verdi
    if verdi in dic.keys():
        return dic[verdi]
    else:
        return []

#lager en liste med alle mulige kombinasjoner av elementene i listen
#ved at hvert element blir lagt til i hvert av de forrige "setene" før
#det legges til til slutt. 
def lag_power_set(liste):
    power_set = [liste.pop(0)]
    for i in range(len(liste)):
        number = liste.pop(0)
        for j in range(len(power_set)):
            try:
                new_element=list(power_set[j]) 
                #Å bruke list-funksjonen på en enkel int gir en type-error
            except TypeError:
                new_element=[power_set[j]]
            new_element.append(number)
            power_set.append(new_element)
        power_set.append([number])
    return power_set

#returnerer en liste av lister, hvor hver av listene inneholder
#strenger av lengde (i+1) som kan lages ved hjelp av bokstavene i streng
def finn_ord(dic, streng):
    power_set = lag_power_set(list(streng))
    liste_med_ord = [ [] for x in range(len(streng))]
    for liste in power_set:
        word_list = finn_anagram(dic, "".join(liste))
        if len(word_list) > 0:
            for word in word_list:
                liste_med_ord[len(word)-1].append(word)

    #fjerner duplikater og sorterer
    for i in range(len(liste_med_ord)):
        liste_med_ord[i] = list(set(liste_med_ord[i]))
        liste_med_ord[i].sort()
        
    return liste_med_ord

def main():
    print('Dette er et program som kan finne ord til scrabble. Skriv inn en rekke med bokstaver,')
    print('og programmet vil finne alle norske ord som kan lages med disse bokstavene')
    ordliste = file_2_list('nsf2016.txt')
    dic = list_2_dic(ordliste)

    while True:
        print('Skriv inn ordet / strengen du ønsker ord fra,')
        navn = input('eller ENTER (tom streng) for å slutte: ')
        if navn == '':
            break

        word_list = finn_ord(dic, navn)
        for i in range (len(word_list)):
            print (i+1, "bokstaver:")
            try:
                line=word_list[i].pop(0)
                for word in word_list[i]:
                    line = ", ".join([line, word])
                print (line)
            except IndexError: #pop lager en error når listen er tom
                print ("Ingen ord funnet")
            print ()

    print('Takk for nå')

main()

# EKSTRA FORKLARING:
# Dictionary primes gir en unik primtallsverdi for hver bokstav.
# De er ordnet etter frekvens, dvs. mest vanlige bokstav i norsk (E) først,
# dette for at produktene skal bli minst mulig. Ved å multiplisere sammen tall
# for alle bokstavene i et ord vil ord ende med samme verdi hvis og bare hvis de
# består av akkurat de samme bokstavene: TRE = 3*5*2 og ERT = 2*5*3 blir 30, og
# det er er umulig for et ord som inneholder noe annet enn akkurat disse tegnene
# å få samme verdi. Dette fordi vi kun har brukt primtall. Hadde vi brukt andre
# tall enn primtall, f.eks. I=15 i stedet for 17, kunne man ha fått 30 også for
# ordet "EI" som inneholder andre bokstaver enn TRE, ERT, ...
