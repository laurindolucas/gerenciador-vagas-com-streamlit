casa = 12
nome = input("digite seu nome: ")

if nome == "caio":
    falalal
else: 
    hdjdjd
    
    
lista = [13, 123, "caio", 4.35, True] #mutavel
tupla = (14, 16) #imutavel

chave : valor 

dados = {
    'nome' : "caio",
    'idade' : 14,
    'matricula' : 15252
}

populacoes = {"Brasil": 215_000_000, "China": 1_400_000_000, "EUA": 333_000_000, "Índia": 1_220_000_000}
pais_maior_pop = ""
maior_pop = 0

for pais, populacao in populacoes.items():
    if populacao > maior_pop:
        maior_pop = populacao
        pais_maior_pop = pais
print(f"O país com a maior população é: {pais_maior_pop} com {maior_pop} habitantes.")

