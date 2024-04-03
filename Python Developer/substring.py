N = int(input())
nums_list = []

while(N > 0):
    ''' 
    TODO  Verifique, para cada entrada A e B, se os dois valores são compatíveis e imprima se
    "encaixa" ou "não encaixa" para cada uma das relações N vezes.
    '''
    
    nums_list.append(input().split(' '))
    
    N -= 1

for nums in nums_list:
    A = nums[0]
    B = nums[1]
    
    if A.find(B) > -1:
      print("encaixa")
    else:
      print("nao encaixa")