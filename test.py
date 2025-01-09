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
    if not isinstance(number, int) or number < 0:
        raise ValueError("Input must be a non-negative integer.")
    if number == 0:
     return ValueError
    if number < 2:
        return False
    if number == 2:
        return True
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    
    return True

def primes_in_range(a, b):
    primes = []
    if not isinstance(a, int) or not isinstance(b, int) or a < 0 or b < 0:
        raise ValueError("Inputs must be non-negative integers.")
    if a > b:
        a, b = b, a
    for num in range(a, b + 1):
        if is_prime(num):
            primes.append(num)
    return primes

if __name__ == "__main__":
    print(fibonacci(n))
    print(is_prime(6))
    print(primes_in_range(20, 1))