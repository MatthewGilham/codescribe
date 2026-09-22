from unittest import result
import  art
def add(n1, n2):
    return n1 + n2
def subtract(n1, n2):
    return n1 - n2
def divide(n1, n2):
    return n1 / n2
def multiply(n1, n2):
    return n1 * n2
dictionary = {'+': add,
              '*': multiply,
              '/': divide,
              '-': subtract,
              }
def calculator():
    print(art.logo)
    number1 = float(input("Enter first number"))
    while True:
        for n in dictionary:
            print(n)
        choice = input("Make a choice")
        number2 = float(input("Enter your second number"))

        result = int((dictionary[choice](number1, number2)))
        print(f"{number1}{choice}{number2} = {result}")
        choice2 = input(f"Type 'y' to continue calculating with {result}, or type 'n' to start a new calculation: ")
        if choice2 == "y":
            number1 = result
        else:
            print("\n" * 100)
            calculator()

calculator()


















