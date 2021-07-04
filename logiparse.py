from stack import Stack
import re

class Logiparse():
    def __init__(self, str=""):
        self.equations = []
        self.variables = {}

        self.addEquation(str)

    def addEquation(self, str):
        """
        Sets self.equation
        :param str: <str> logic equation
        :return: <bool> success or failure
        """
        # Do not add equation if empty string
        if(str != ""):
            # Pre-format string
            str = str.lower()
            str = str.replace(" ", "")
            # Validate formatting
            res, err = self.validateFormat(str)
            # If validation failed: display error and return false
            if(not res):
                print(err)
                print("Method setEquation() failed.")
                return False

            # Set self.equation
            self.equations.append(str)
        # return success
        return True

    def getAllEquations(self):
        return self.equations

    def validateFormat(self, equ):
        """
        Validates format of logic equation
        :param equ: <str> logic equation
        :return: <bool>, <str> success/failure, error
        """
        # Add "End of Equation" char - '#' if not already on equation
        if(equ[-1] != '#'):
            equ += '#'
        # To be filled error string
        err = ""
        # To be filled flag indicating whether component is variable
        isvar = False
        # Stack to track equation's open parenthesis
        parenthesis = ""
        # Remove spaces from equation
        equ = equ.replace(" ", "")
        # Placeholder to be used in validation algorithm - (component, isvar)
        lastcomponent = ("", False)
        # List to be filled with equation components
        components = []
        # current selected component index
        ci = 0
        # Loop through equation
        for i in range(len(equ)):
            # Reached end of equation
            if(equ[i] == '#'):
                break
            # Check if variable or operator
            if( equ[i] != '*' and
                equ[i] != '+' and
                equ[i] != '='):
                isvar = True
            else:
                isvar = False

            # Skip if first iteration
            # -----------------------
            if(lastcomponent[0] != ""):
                # Check that last component is opposite component type
                if(isvar and isvar == lastcomponent[1]):
                    # Check if character is parenthesis, final '(not), or alphanumeric
                    if( equ[i] != '(' and
                        equ[i] != ')' and
                        equ[i] != '\'' and
                        not equ[i].isalnum()):
                        # Error and return failure
                        err = "Error: variable must be alphanumeric, may contain parenthesis, or a final quote (') indicating the negation.\nBroke on: \'" + lastcomponent[0] + "\'."
                        return False, err
                    else:
                        # Keep track of parenthesis
                        if(equ[i] == '(' or equ[i] == ')'):
                            parenthesis += equ[i]
                        # If negation, verify it is at the end of variable
                        if(equ[i] == '\'' and i != len(equ)-1):
                            # Get rest of the string if more characters exist beyond the negation
                            remainder = re.search("[^\*\+]*?(?=[\*\+\n]|[#]$)", equ[i+1:])# Get all characters until the first operator or end of equation.
                            # Check that remaining characters are closing parenthesis
                            if(remainder):
                                if(remainder.group() != ''): # seperate if b/c throws error if remainder is None
                                    if(not bool(re.match("^[)'#]+$", remainder.group(0)))): # match if all characters are closing parenthesis, quote, or End of Equation char
                                        # Error and return failure
                                        err = "Error: variable negation must take place at the tail of the component.\nBroke on: \'" + lastcomponent[0] + "\'."
                                        return False, err
                        # Add the currently being parsed variable's character to the last component.
                        lastcomponent = (lastcomponent[0] + equ[i], lastcomponent[1])
                elif(not isvar and isvar == lastcomponent[1]):
                    # Error and return failure
                    err = "Error: unexpected component type. Check for alternating variable and operator order.\nBroke on: \'" + lastcomponent[0] + "\'."
                    return False, err
            # If first iteration, ensure component is variable
            else:
                # Set last component to current character
                lastcomponent = (equ[i], isvar)
                # Check if operator
                if(isvar == False):
                    err = "Error: unexpected component type. Equation must not begin with operator.\nBroke on: \'" + lastcomponent[0] + "\'."
                    return False, err
            # Set lastcomponent for next iteration
            if( (lastcomponent[1] and not isvar) or
                (not lastcomponent[1] and isvar)):
                lastcomponent = (equ[i], isvar)
        # If we made it to the end, return success!
        return True, err


    def precedence(operator):
        """
        Informs the precedence of operators (',*,+)
        :param operator: <str> equation operator
        :return: <int> precedence value (1-3)
        """
        if(operator == '+'):
            return 1
        elif(operator == '*'):
            return 2
        elif(operator == '\''):
            return 3
        return 0

    def infixToPostfix(equation):
        """
        Converts infix equation notation to postfix equation.
        :param equation: <str> infix equation
        :return: <str> postfix equation
        """


        # Initialize to be filled postfix equation string
        postfix = ""
        # Initialize stack to be used in postfix conversion. Chosen over list for O(1).
        stack = Stack()
        stack.push('#') # Add extra character to avoid underflow
        # Infix equation's 'components' are identified by space. Retrieve components.
        components = equation.split(" ")
        # Loop through components
        #for component in components:
