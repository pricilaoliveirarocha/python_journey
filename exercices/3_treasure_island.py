print ('''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/
*******************************************************************************
''')

print("Bem vindo(a) ao jogo da Ilha do Tesouro!")
print("Sua missão é encontrar o tesouro.")
print("Você está em uma encruzilhada. Para onde você quer ir? Digite 'esquerda' ou 'direita'.")

choice_1 = input("Digite sua escolha: ").lower()

if choice_1 == "esquerda":
    print("Você chegou a um lago. Há uma ilha no meio do lago. Digite 'esperar' para esperar por um barco ou 'nadar' para nadar até a ilha.")
    choice_2 = input("Digite sua escolha: ").lower()
    
    if choice_2 == "esperar":
        print("Você chegou à ilha em segurança. Há uma casa com 3 portas: uma vermelha, uma amarela e uma azul. Qual você escolhe?")
        choice_3 = input("Digite sua escolha: ").lower()
        
        if choice_3 == "amarela":
            print("Parabéns! Você encontrou o tesouro! Você venceu!")
        elif choice_3 == "vermelha":
            print("Você entrou em uma sala cheia de fogo. Game Over.")
        elif choice_3 == "azul":
            print("Você entrou em uma sala cheia de feras. Game Over.")
        else:
            print("Você escolheu uma porta que não existe. Game Over.")
    else:
        print("Você foi atacado por um peixe gigante. Game Over.")