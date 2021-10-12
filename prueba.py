prueba = " Hd, A,"
prueba = prueba.split(",")[:-1]
print(prueba)
final = " V"
for letra in prueba:
    if letra not in final:
        final += letra +","

print(final)