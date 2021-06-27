class Logiparse():
    def __init__(self, str=""):
        self.equation = ""

        self.setEquation(str)

    def setEquation(self, str):
        """
        Sets self.equation
        :param str: <str> logic equation
        :return: <bool> success or failure
        """
        # Pre-format string
        str = str.lower()
        # Validate formatting
        res, err = self.validateFormat(str)
        # If validation failed: display error and return false
        if(not res):
            print(err)
            print("Method setEquation() failed.")
            return False

        # Set self.equation
        self.equation = str
        # return success
        return True

    def getEquation(self):
        return self.equation

    def validateFormat(self, str):
        """
        Validates format of logic equation
        :param str: <str> logic equation
        :return: <bool>, <str> success/failure, error
        """
        # To be filled error string
        err = ""
        # To be filled flag indicating whether component is variable
        isvar = False
        # Stack to track equation's open parenthesis
        parenthesis = ""
        # Equation's 'components' are identified by space. Retrieve components.
        components = str.split(" ")
        # Placeholder to be used in validation algorithm - (component, isvar)
        lastcomponent = ("", False)
        # Loop through components
        for component in components:
            # Check if variable or operator
            if( component != '*' and
                component != '+' and
                component != '='):
                isvar = True
            else:
                isvar = False

            # Skip if first iteration
            # -----------------------
            if(lastcomponent[0] != ""):

                # Check that last component is opposite component type
                if(isvar == lastcomponent[1]):
                    # Error and return failure
                    err = "Error: unexpected component type. Check for alternating variable and operator order.\nBroke on: \'" + component + "\'."
                    return False, err

                # Validate variable formatting
                if(isvar):
                    # Loop through variable to validate format
                    for i in range(len(component)):
                        # Check if character is parenthesis, final '(not), or alphanumeric
                        if( component[i] != '(' and
                            component[i] != ')' and
                            component[i] != '\'' and
                            not component[i].isalnum()):
                            # Error and return failure
                            err = "Error: variable must be alphanumeric, may contain parenthesis, or a final quote (') indicating the negation.\nBroke on: \'" + component + "\'."
                            return False, err
                        else:
                            # Keep track of parenthesis
                            if(component[i] == '(' or component[i] == ')'):
                                parenthesis += component[i]
                            # If negation, verify it is at the end of variable
                            if(component[i] == '\'' and i != len(component)-1):
                                # Get rest of the string if more characters exist beyond the negation
                                remainder = component[i+1:]
                                # Check that remaining characters are closing parenthesis
                                if(not remainder[0] == ')' or not remainder.count(remainder[0]) == len(remainder)):
                                    # Error and return failure
                                    err = "Error: variable negation must take place at the tail of the component.\nBroke on: \'" + component + "\'."
                                    return False, err

            # Set lastcomponent for future iterations
            lastcomponent = (component, isvar)

        # Check if each parenthesis has a match
        # Remove matching neighbor matching parenthesis if exists
        parenthesis = parenthesis.replace("()", "")
        # While still neighbor matching parenthesis, remove them
        while parenthesis != "":
            lastcheck = parenthesis
            parenthesis = parenthesis.replace("()", "")
            # If removal attempt accomplishes nothing, throw error and break
            if(lastcheck == parenthesis):
                # Error and return failure
                err = "Error: Orphaned parenthesis.  Please review to make sure each open and closing parenthesis has a matching opposite."
                return False, err

        # Return success
        return True, err
