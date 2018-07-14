# coding=utf-8
def redondear(numero, full_scale):
    """Función para redondear el valor pasado por argumento"""
    # Si el numero es menor que 0.1%, se devuelve 0
    if abs(numero) <= 0.001 * abs(full_scale):
        return 0
    if numero < 0:
        negativo = True
        numero = numero * (-1)
    else:
        negativo = False
    numero_s = str(numero)
    longitud = len(numero_s)
    # Se encuentra la posición de la coma, si hay. Si no, coma = -1
    coma = numero_s.find('.')
    n = 0
    # Bucle while para hallar dígito y n
    # Digito = Ultimo dígito antes de la coma
    # n = Posicion de la primera cifra significativa
    while True:
        # Se asigna el dígito del numero correspondiente a la iteracion
        digito = numero_s[n]
        if digito != ".":
            if int(digito) > 0:
                # El bucle acaba cuando el dígito es distinto de una coma y de 0
                break
            else:
                # Si el dígito es 0, se suma 1 a n y se sigue iterando
                n += 1
        else:
            # Si el dígito es una coma, se suma 1 a n y se sigue iterando
            n += 1
    # Si la primera cifra significativa es 1, hay que redondear a 4 decimales
    if digito == '1':
        decimales = 4
    # Si no, hay que redondear a 3
    else:
        decimales = 3
    # Si hay una coma antes de la primera cifra significativa, se resta 1 a longitud y a n, ya que no cuenta
    if coma <= n:
        longitud -= 1
        n -= 1
    # Cifras = Numero de cifras a las que hay que redondear
    # Si la longitud es menor que 4, no hace falta redondear
    if longitud < 4:
        if negativo:
            numero = numero * (-1)
        return numero
    # Si no hay coma y el primer dígito es cifra significativa, se cogen (decimales - longitud) cifras
    elif n == 0 and coma == -1:
        cifras = decimales - longitud
    # Si la primera cifra significativa no es 1 y no es el primer dígito, se cogen (decimales + n - 1) cifras
    elif int(digito) > 1 and n > 0:
        cifras = decimales + n - 1
    # Si la primera cifra significativa es 1 y no es el primer dígito, se cogen (decimales + n - 1) cifras
    elif int(digito) == 1 and n > 0:
        cifras = decimales + n - 1
    # Si la primera cifra significativa es 1 y es el primer dígito...
    elif int(digito) == 1 and n == 0:
        # ...y la coma esta mas allá de después del primer dígito, se cogen (decimales - n - 1 - coma) cifras
        if coma > 1:
            cifras = decimales - n - coma
        # ...y la coma no esta mas allá de después del primer dígito, se cogen (decimales - n - 1) cifras
        else:
            cifras = decimales - n - 1
    # Si la primera cifra significativa no es 1 y es el primer dígito, se cogen (decimales - coma) cifras
    elif int(digito) > 1 and n == 0:
        cifras = decimales - coma
    # En cualquier otro caso, no se redondea
    else:
        if negativo:
            numero = numero * (-1)
        return numero
    # Se redondea el numero a las cifras correspondientes
    resultado = round(numero, cifras)
    # Se evita el ".0" para numeros enteros
    if float(resultado).is_integer():
        resultado = int(resultado)
    # Se devuelve el numero redondeado
    if negativo:
        resultado = resultado * (-1)
    return resultado
