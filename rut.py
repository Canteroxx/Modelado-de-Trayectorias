def convertir_rut(rut):
    digitos_par = []
    digitos_inpar = []
    for i in rut:
        if i == "." or i == "-":
            continue
        entero = int(i)
        if len(rut) % 2 == 0:
            digitos_par.append(entero)
        else:
            digitos_inpar.append(entero)
    
    return digitos_par if len(rut) % 2 == 0 else digitos_inpar
