def Bohemians(): 
    bohemiansJsouDobry = True
    if bohemiansJsouDobry == True:
        print('bohemians 1905 yayy miluju bohemku')
    else: 
        print('bohemians fuuuj jsou shit')
Bohemians()

n = 100
def fibonacci(n):
    if not isinstance(n, int) or n<0:
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fibonacci(n-1) + fibonacci(n-2)
        
print(fibonacci(n))
if __name__ == "__main__":
    print()