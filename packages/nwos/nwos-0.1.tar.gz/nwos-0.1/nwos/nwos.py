# nwos.py

class IsPrime:
    def __init__(self, num):
        if not isinstance(num, int):
            raise ValueError(f"Invalid input: {num}. Only integers are allowed.")
        self.num = num

    def check_prime(self):
        if self.num <= 1:
            return False
        for i in range(2, int(self.num ** 0.5) + 1):
            if self.num % i == 0:
                return False
        return True


def isPrime(num):
    try:
        prime_checker = IsPrime(num)
        return prime_checker.check_prime()
    except ValueError as e:
        print(f"Error: {e}")
        return None


def isComposite(num):
    try:
        prime_checker = IsPrime(num)
        return not prime_checker.check_prime()
    except ValueError as e:
        print(f"Error: {e}")
        return None


def check_list_prime(lst):
    if not isinstance(lst, list):
        raise ValueError(f"Expected a list, but got {type(lst).__name__}")

    primes = []
    composites = []

    for num in lst:
        if not isinstance(num, int):
            raise ValueError(f"Invalid element in list: {num}. Only integers are allowed.")

        if isPrime(num):
            primes.append(num)
        elif isComposite(num):
            composites.append(num)

    return primes, composites
