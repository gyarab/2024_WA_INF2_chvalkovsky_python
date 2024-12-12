def Bohemians(): 
    bohemiansJsouDobry = True
    if bohemiansJsouDobry == True:
        print('bohemians 1905 yayy miluju bohemku')
    else: 
        print('bohemians fuuuj jsou shit')
Bohemians()

def fibonacci(n):
    if isinstance(n, int) and n >= 0:
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fibonacci(n-1) + fibonacci(n-2)
    else:
        return "Invalid input"
n = 20

def is_prime(number):
    if isinstance(number, int) and number >= 0:
        if number == 1 or number == 2 or number == 3:
            return True
        elif number > 3:
            for i in range(2, int(number // 2) + 1):
                if number % i == 0:
                    return False
        return True
    else:
        return ValueError
if __name__ == "__main__":
    print(fibonacci(n))
    print(is_prime(27))