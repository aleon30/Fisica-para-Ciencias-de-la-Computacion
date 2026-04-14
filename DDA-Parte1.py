longitud = float(input("Ingrese la longitud del dique, L(m): "))
while longitud < 1.5 or longitud > 3.5:
    longitud = float(input("La longitud debe estar en el intervalo [1,50; 3,50]: "))
altura = float(input("Ingrese la altura del nivel del fluido, H(m): "))
while altura < 1 or altura > 4.8:
    altura = float(input("La altura debe estar en el intervalo [1,00; 4,80]: "))
