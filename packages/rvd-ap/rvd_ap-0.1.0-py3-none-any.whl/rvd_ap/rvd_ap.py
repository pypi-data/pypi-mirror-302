'''
                                                                 ~~~ PRELIMNARY ~~~~
Library name: rvd_ap
Creator Name: Aravind Sree U
Place of recidence: Earth 616, South Asia Tectonic Plate, India, Tamilnadu, Chagalpattu, Guduvanchery 603202

This library is creates by Aravind Sree U studying in grade 11. This library will provide you with some randmly created functions which I did for fun.
For some people it will be useful and for some it may not be useful. So kindly go through the all the functions use it and leave Pythnon IDLE.

                                                            ~~~ THANK YOU FOR NOTHING ~~~
'''

def avg(numbers):
    """
    Calculate the average of a list of numbers.

    Args:
        numbers (list): A list of numbers.

    Returns:
        float: The average of the numbers.
    """
    return sum(numbers) / len(numbers)


def sign(number):
    """
    Determine the sign of a number.

    Args:
        number (int or float): The number to check.

    Returns:
        str: The sign of the number (+ or -).
    """
    if number > 0:
        return "+"
    elif number < 0:
        return "-"
    else:
        return "0"


def perfect_num(number):
    """
    Check if a number is a perfect number.

    Args:
        number (int): The number to check.

    Returns:
        bool: True if the number is perfect, False otherwise.
    """
    sum_divisors = 0
    for i in range(1, number):
        if number % i == 0:
            sum_divisors += i
    return sum_divisors == number


def armstrong_num(number):
    """
    Check if a number is an Armstrong number.

    Args:
        number (int): The number to check.

    Returns:
        bool: True if the number is an Armstrong number, False otherwise.
    """
    num_str = str(number)
    num_len = len(num_str)
    sum_digits = 0
    for digit in num_str:
        sum_digits += int(digit) ** num_len
    return sum_digits == number


def palindrome_num(number):
    """
    Check if a number is a palindrome.

    Args:
        number (int): The number to check.

    Returns:
        bool: True if the number is a palindrome, False otherwise.
    """
    return str(number) == str(number)[::-1]


def primality(number):
    """
    Check if a number is prime.

    Args:
        number (int): The number to check.

    Returns:
        bool: True if the number is prime, False otherwise.
    """
    if number <= 1:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True


def fib(end_range):
    """
    Generate a Fibonacci sequence up to a given end range.

    Args:
        end_range (int): The end range of the sequence.

    Returns:
        str: The Fibonacci sequence as a comma-separated string.
    """
    fib_sequence = [0, 1]
    for _ in range(end_range):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return ", ".join(map(str, fib_sequence)) 


def vowel_count(string):
    """
    Count the number of vowels in a given string.

    Args:
        string (str): The string to check.

    Returns:
        int: The number of vowels in the string.
    """
    vowels = "aeiouAEIOU"
    return sum(1 for char in string if char in vowels)


def consonant_count(string):
    """
    Count the number of consonants in a given string.

    Args:
         string (str): The string to check.

    Returns:
        int: The number of consonants in the string.
    """
    consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
    return sum(1 for char in string if char in consonants)


def space_count(string):
    """
    Count the number of spaces in a given string.

    Args:
        string (str): The string to check.

    Returns:
        int: The number of spaces in the string.
    """
    return string.count(" ")


def palindrome_str(string):
    """
    Check if a given string is a palindrome.

    Args:
        string (str): The string to check.

    Returns:
        bool: True if the string is a palindrome, False otherwise.
    """
    return string == string[::-1]


def word_count(string):
    """
    Count the number of words in a given string.

    Args:
        string (str): The string to check.

    Returns:
        int: The number of words in the string.
    """
    return len(string.split())


def alpha_count(string):
    """
    Count the number of alphabets in a given string.

    Args:
        string (str): The string to check.

    Returns:
        int: The number of alphabets in the string.
    """
    return sum(1 for char in string if char.isalpha())


def int_count(string):
    """
    Count the number of integers/floats in a given string.

    Args:
        string (str): The string to check.

    Returns:
        int: The number of integers/floats in the string.
    """
    import re
    return len(re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", string))


def div_it(divident, divisor):
    """
    Check if a dividend is divisible by a divisor.

    Args:
        divident (int or float): The dividend.
        divisor (int or float): The divisor.

    Returns:
        bool: True if the dividend is divisible by the divisor, False otherwise.
    """
    return divident % divisor == 0
