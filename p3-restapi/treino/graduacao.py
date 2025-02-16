import math

# dicionario
order_belt = {'Branca': 0, 'Azul': 1, 'Roxa': 2, 'Marrom': 3, 'Preta': 4 } # Ordem das faixas 

def calculate_lessons_to_upgrade(n): # n é o número de aulas concluídas
    d = 1.47 # Dificuldade do curso
    k = 30 / math.log(d) 

    aulas = k * math.log(n + d) #
    
    return round(aulas) # Arredonda para o número inteiro mais próximo