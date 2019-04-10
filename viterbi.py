#Distancia de hamming de dos numero de dos bits
def hamming2(x,y): 
    assert len(x)==len(y)
    return sum(c1!=c2 for c1, c2 in zip(x,y))
states = ('00', '01','10','11') #estados de FMS

#Valores trasmitidos por el codificador
trasmitido = ['11', '10', '00', '10', '00', '10', '00', '10'] 
# Valores obtenidos del receptor con efecto de ruido
observations = ['11', '10', '00', '10', '00', '10', '00', '10']   
start_metric = {'00': hamming2(observations[0],'00'), '01':100, '10': hamming2(observations[0],'11'), '11':100}# metrica inicial
transition_code = {
                '00' : {'00': '00','10': '11'},#Estados de transición de la FSM
                '01' : {'00': '11','10': '00'},
                '10' : {'11': '01','01': '10'},
                '11' : {'01': '01','11': '10'}
                }
def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    print(s)
def viterbi(obs, states, start_m):
    V = [{}]# estructura
    path = {}# direcciones
    for y in states:
        V[0][y] = start_m[y] 
        path[y] = [y]
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
        for y in states:
        #Medida de la distancia de Hamming  con el valor observado
        #y el posible valor codificado en la maquina de estado del trasmisor
            transition_metric = {
                '00' : {'00': hamming2(obs[t],'00'),'01': 100,'10': hamming2(obs[t],'11'),'11': 100},  
                '01' : {'00': hamming2(obs[t],'11'),'01': 100,'10': hamming2(obs[t],'00'),'11': 100}, 
                '10' : {'00': 100,'01': hamming2(obs[t],'10'),'10': 100,'11': hamming2(obs[t],'01')},
                '11' : {'00': 100,'01': hamming2(obs[t],'01'),'10': 100,'11': hamming2(obs[t],'10')}
                }
                #Calculando la ruta con menor distancia 
            (prob, state) = min((V[t-1][y0]+transition_metric[y0][y], y0) for y0 in states) 
            V[t][y] = prob
            newpath[y] = path[state] + [y]
        path = newpath
    #print_dptable(V)
    (prob, state) = min((V[t][y], y) for y in states)
    return (prob, path[state])
b=viterbi(observations,
                   states,
                   start_metric)[1]
b.insert(0,'00')

def stade_code(transition):
    code_tras=[]
    for i in range(0,len(transition)-1):
        code_tras.append(transition_code[transition[i]][transition[i+1]] )
    return code_tras
print("Trasmitido:")
print(trasmitido)
print("Recibido:")
print(observations)
print("Correjido")
print(stade_code(b))
