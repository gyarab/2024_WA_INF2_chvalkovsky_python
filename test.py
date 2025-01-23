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

def split_into_threes(text):
    text = text.replace('"', '')
    if not isinstance(text, str):
        raise ValueError
    return [text[i:i+3] for i in range(0, len(text), 3)]

def caesar_encode(text):
    alph = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    shift = 3
    for i in range(0, len(text) 0 , 1):
        text = list(text)
        if text[i].lower() in alph:
            text[i] = alph[(alph.index(text[i].lower()) + shift) % 26]
        text = ''.join(text)
        return text
    
def morse(text):
    morse_code = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
    }
    for c in text.upper():
        if c not in morse_code:
            raise ValueError(f"Character '{c}' cannot be encoded in Morse code.")
        for char in text:
            if char in text:
                if char == ' ':
                    text = text.replace(char, ' / ')
                morse_code.index(char)


        return ' '.join([morse_code[c] for c in text.upper()])
if __name__ == "__main__":
    print(fibonacci(n))
    print(is_prime(6))
    print(primes_in_range(20, 1))
    print(split_into_threes("aj dnjasnd ansdioa j"))
    print(caesar_encode("abc"))
    print(morse("test"))

    