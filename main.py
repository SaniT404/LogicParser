from logiparse import Logiparse

def main():
    #logic = Logiparse("A' + (B * * C' + (Dooby * Dilly')')")
    #print(logic.getAllEquations())
    logic = Logiparse()
    res, err = logic.validateFormat("A' + (B * C' + (Dooby * Dilly')(dilly)')#")
    if(not res):
        print(err)

main()
