#Economu Victor, grupa 134
# * -> lambda (transition)
import queue

def afisare_1(Str):
    for value in Str:
        print(value)
    print("\n")

def afisare_AFD(first, Final, D):
    print("\nAFISARE AFD:\n")
    for key in D:
        print(key, ": ", sep = "", end = " ")
        print(D[key])
    print("\nSTAREA INITIALA in AFD este:", first, sep = "  ")
    print("\nSTARILE FINALE in AFD sunt:", Final, sep = "  ")
    print()
    

# Main:
###
fisier = "AFN-LAMBDA_in.txt"
# fisier = "AFN-LAMBDA_in_2.txt"
# fisier = "AFN-LAMBDA_in_3.txt"
# fisier = "AFN-LAMBDA_in_4.txt"
###
f = open(fisier, "r")

Q = int(f.readline()) #Citim numarul total de stari(AFN-Lambda).
F = set(int(F_i) for F_i in f.readline().split()) #Citim un set cu toate starile finale(acceptoare) pt. AFN-Lambda.

AFN_Lambda = [{} for i in range(Q)] #Memoram toate tranzitiile AFN-Lambda-ului intr-o lista de dictionare. 
for line in f:
    line = line.split()
    line[0] = int(line[0])
    line[2] = int(line[2])
    if line[1] not in AFN_Lambda[line[0]]:
        AFN_Lambda[line[0]][line[1]] = set()
        AFN_Lambda[line[0]][line[1]].add(line[2])
    else:
        AFN_Lambda[line[0]][line[1]].add(line[2])        
f.close() 

##
# print("Afisare AFN-Lambda:\n")
# afisare_1(AFN_Lambda)
##
######
AFN_Inchideri = [set() for value in AFN_Lambda] #Implementam cate un set(multime) pt. fiecare stare, astfel incat sa retinem Lambda-Inchiderile fiecarei stari in parte.
for i in range(len(AFN_Lambda)):
    visited = [False for i in range(Q)] #Verificam sa nu trecem de mai multe ori prin aceleasi stari.

    AFN_Inchideri[i].add(i)
    qu_1 = queue.Queue() #Implementam o coada care va adauga si va sterge, pe rand, starile prin care ajungem cu Lambda("*"), folosind metoda BFS de parcurgere.
    qu_1.put(i) #Lambda-Inchiderea cu nr. "k" contine cel putin starea "k". 
    while not qu_1.empty():
        top = qu_1.get() #Scoatem starea din coada, la momentul actual.
        visited[top] = True #Marcam mereu starile scoase din coada.
        if "*" in AFN_Lambda[top]:
            for x in AFN_Lambda[top]["*"]:
                if visited[x] == False: #Adaugam in coada si in set, doar stari nevizitate pana in acel moment.
                    AFN_Inchideri[i].add(x) #Adaugam, daca nu exista in multimea "i", toate starile "x" prin care am ajuns cu "*"(tranzitie).
                    qu_1.put(x) #Punem in coada aceste stari, pt. a putea fi prelucrate mai tarziu la rnadul lor.

##
# print("Afisare LAMBDA_Inchideri:\n")    
# afisare_1(AFN_Inchideri)
##
######

AFN = [{} for value in range(Q)] #Implementam o lista de dictionare care va retine functia DELTA pt. un AFN echivalent cu AFN_Lambda-ul nostru dat ca input.

for i in range(Q):
    all_transitions = set() #Vom retine astfel tranzitiile tuturor starilor din Lambda-Inchiderea "i".
    for val in AFN_Inchideri[i]:
        for x in AFN_Lambda[val]:
            if x != "*": #Nu luam in considerare tranzitiile Lambda("*")!
                all_transitions.add(x) #Adaugam tranzitia(cheia) in setul de tranzitii pt. Lambda-Inchiderea "i".
    
    for key in all_transitions:
        temp1 = set() #Retinem setul de stari pt. "lambda* -> Tr ->", unde Tr = tranzitie.
        for vl in AFN_Inchideri[i]:
            if key in AFN_Lambda[vl]:
                temp1 |= AFN_Lambda[vl][key] #Reunim multimile corespunzatoare de stari din "AFN_Lambda" cu cele din "temp1".
        temp2 = set() #Retinem setul de stari pt. "temp1 -> lambda*".
        for x in temp1:
            temp2 |= AFN_Inchideri[x] #Reunim multimile corespunzatoare de stari din "AFN_Inchideri" cu cele din "temp2".
        if key not in AFN[i] and len(temp2) > 0:
            AFN[i][key] = temp2 #Adaugam in dictionarul "i" din AFN, un set "temp2" cu toate starile ce alcatuiesc AFN-ul echivalent, precum si tranzitia(cheia) sa corespunzatoare.

##
# print("Afisare AFN:\n")
# afisare_1(AFN)
##
###############################################################        

AFD = {} #Vom implementa pe parcurs un dictionar de dictionare de seturi(multimi) cu mai multe stari.

#   Transformam Lambda-Inchiderea(set de stari) lui "q0" intr-un sir de caractere sortate crescator, 
#apoi adaugam cheia respectiva in AFD-ul nostru ce va avea ca valoare primul dictionar din AFN-ul
#calculat anterior.
SL_temp = sorted(AFN_Inchideri[0]) 
SL_temp = "_".join([str(x) for x in SL_temp])
AFD[SL_temp] = AFN[0] 

qu_2 = queue.Queue() #Implementam o coada care va adauga si va scoate pe parcurs starile pe care AFD-ul nostru rezultat va trebui sa le contina, conform algoritmului.

for tranzitie in AFD[SL_temp]:
    s_temp = sorted(AFD[SL_temp][tranzitie])
    s_temp = "_".join([str(x) for x in s_temp]) #Multimea de stari va deveni un simplu string, pt. a putea fi cheie in dictionar(hashable type).
    if s_temp not in AFD:
        AFD[s_temp] = {} #Vom memora doar multimi si stringuri de stari distincte. 
        qu_2.put(s_temp) #Daca stringul ce formeaza o noua stare, nu se afla in AFD deja, il punem si in coada pt. a fi prelucrat la randul lui in program. 

while not qu_2.empty():
    str_list = qu_2.get() #Extragem sirul de caractere(format din stari) din coada.
    copy_str_list = str_list #Facem o copie a sirului de caractere extras anterior.

    str_list = str_list.split("_") #Construim o lista de stari(despartite de delimitatorul "_").
    
    all_transitions_2 = set() #Implementam un set(multime) care va retine tranzitiile tuturor starilor 
    for item in str_list:
        for x in AFN[int(item)]:
            all_transitions_2.add(x) #Adaugam toate tranzitiile starilor din "str_list" corespondente in AFN, in setul "all_transitions_2".
    
    for key in all_transitions_2:
        temp_3 = set() #Implementam un set(multime) care va reprezenta, de fapt, noua stare din AFD-ul nostru, cu tranzitia(cheia) "key".
        for val in str_list:
            if key in AFN[int(val)]:
                temp_3 |= AFN[int(val)][key] #"temp_3" va fi, de fapt, reuniunea multimilor de seturi pt. starile si tranzitiile corespondente in AFN-ul nostru.

        if key not in AFD[copy_str_list]:
            AFD[copy_str_list][key] = temp_3 #Adaugam multimea de stari pe pozitia corespunzatoare, in functie de tranzitie("key").

        S_temp_3 = sorted(temp_3)
        S_temp_3 = "_".join([str(x) for x in S_temp_3]) #Multimea de stari va deveni un simplu string, pt. a putea fi cheie in dictionar(hashable type).

        if S_temp_3 not in AFD: 
            AFD[S_temp_3] = {} #Punem o noua cheie in dictionar(stringul de stari rezultat anterior).
            qu_2.put(S_temp_3) #Adaugam stringul de stari(reprezentand noua stare in AFD) in coada pt. a fi prelucrata ulterior in program.

######

F_AFD = set() #Implementam un set de stari finale in AFD-ul calculat anterior.

first_key = None #Retinem starea INIT din AFD-ul nostru.

for key in AFD:
    if first_key == None:
        first_key = key #Starea INIT este chiar prima cheie a dictionarului AFD.

    tp = key.split("_") #Ne cream o lista temporara din starile cheii actuale.

    for stare in tp:
        if int(stare) in F:
            F_AFD.add(key) #Punem in setul de stari finale ale AFD-ului nostru, doar starea(stringuri compuse din vechile stari din AFN si AFN_Lambda) care apare in "F"(starile finale ale Lambda_AFN-ului).
            break #Daca cel putin o stare din stringul nostru apare in "F", atunci adaugam starea in "F_AFD" si apoi dam un "break".

    for transition in AFD[key]: 
        temp_set = sorted(AFD[key][transition])
        temp_set = "_".join([str(x) for x in temp_set]) 
        AFD[key][transition] = temp_set #Toate multimile formate din stari din AFD vor deveni un string ce va reprezenta noua stare rezultata pt. AFD-ul nostru.


##################
# AFD-ul rezultat in urma aplicarii algoritmului asupra unui AFN-Lambda dat ca input:
afisare_AFD(first_key, F_AFD, AFD)