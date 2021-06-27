from logiparse import Logiparse

def main():
    logic = Logiparse("A' + B&C")
    print(logic.getEquation())

main()
