from logiparse import Logiparse

def main():
    logic = Logiparse("A' + (B * C' + (Dooby * Dilly')')")
    print(logic.getAllEquations())

main()
