from datetime import date 
  
def calcula_idade(nascimento:date): 
    hoje = date.today() 
    diff = hoje - nascimento 
    idade = int(diff.days/365)
    return idade
 