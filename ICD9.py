import json
from six import string_types

class ICD9:
    """
    The ICD9 class captures the hierarchy and descriptions for the ICD9 coding standard
    The source data files were developed from CMS mapping files
    """
    def __init__(self, errorHandle="NoDx"):
        '''
        Loads the dependancies for the ICD9 class
        All the mapping data is stored in JSON files which are loaded into dicts
        '''
        import os
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.errorHandle = errorHandle

        self.__descriptions = json.load(open(dir_path + '/DxCodeHandler data/icd9/descriptions4.json'))
        self.__descendants = json.load(open(dir_path + '/DxCodeHandler data/icd9/descendants.json'))
        self.__children = json.load(open(dir_path +   '/DxCodeHandler data/icd9/children.json'))
        self.__parents = json.load(open(dir_path +   '/DxCodeHandler data/icd9/parents2.json'))
        self.__depths = json.load(open(dir_path +   '/DxCodeHandler data/icd9/depths2.json'))


    """
    handles how the program responsed to codes that don't exist
    When loading the program, pass one of the following configs
    "string" - a custom return string
    "NoDx"
    "ThrowError"
    "None" - return None
    "false" - returns a boolean false
    if all else fails, this will raise and Exception
    """
    def handleError(self, code):
        if self.errorHandle == "NoDx":
            return "NoDx"
        elif self.errorHandle == "ThrowError":
            raise Exception('%s is not an ICD9 code' % code)
        elif self.errorHandle == "None":
            return None
        elif self.errorHandle == "false":
            return false
        elif isinstance(self.errorHandle, string_types):
            return self.errorHandle
        else:
            return "NoDx"


    '''
    returns all codes in the icd9 hierarchy
    Input: None
    Returns: <list>
    '''
    def getAllCodes(self):
        return set(self.__depths.keys())


    '''
    Identifies the input string as a valid icd9 code or not.
    Input: <string> any string
    Returns: <boolean>
    '''
    def isCode(self, code):

        # convert input to string and uppercase
        code = str(code).upper()

        # check to see if string in ICD9 ontology
        try:
            self.__depths[code]
            return True
        except KeyError:
            return False


    """
    Input: <string> any icd9 code
    Returns: <string> the parent of the input icd9 code or null if no parent exists
    """
    def parent(self, codes):

        #throws exception if input not a string or a list
        if not isinstance(codes, string_types) and not isinstance(codes, list):
            raise Exception('ICD9.parent() input must be string or list')

        output = []
        #checks if input is list
        if isinstance(codes, list):
            for i in codes:
                #retrieve parent of code
                output.append(self.__parent(i))

            #removes all NoneTypes from list
            output = [m for m in output if m]

            #removes duplicates from list
            output = list(set(output))

            if len(output) > 0:
                return output
            else:
                return None
        else:
            #returns the parent of the input if not list
            return self.__parent(codes)


    def __parent(self, code):

        #throws exception of input code is not a valid code
        if not self.isCode(code):
            return self.handleError(code)

        code = code.upper()

        #attempts to retrieve parent code from parent dictionary
        try:
            return self.__parents[code]
        except KeyError:
            return None


    """
    Input: <string> any icd9 code
    Returns: <list> a list of children of the input icd9 code or null if no children exist
    """
    def children(self, code):

        # throws exception if input not a string or a list
        if not isinstance(code, string_types) and not isinstance(code, list):
            raise Exception('ICD9.children() input must be string or list')

        temp = []

        # checks if input is list
        if type(code) == list:
            for i in code:
                #retrieve child of code
                temp += self.__getChildren(i)
        else:
            temp += self.__getChildren(code)

        return temp

    def __getChildren(self, code):

        # throws exception if code not a valid icd9 code
        if not self.isCode(code):
            return self.handleError(code)

        code = str(code).upper()

        try:
            return self.__children[code]
        except KeyError:
            return [None]


    """
    Input: <string> any icd9 code
    Returns: <list> a list of all the descendants from the input code or null if no descendants exist
    """
    def descendants(self, code):
        # throws exception if input not a string or a list
        if not isinstance(code, string_types) and not isinstance(code, list):
            raise Exception('ICD9.descendants() input must be string or list')

        temp = []

        # checks if input is list
        if type(code) == list:
            for i in code:
                #retrieve child of code
                temp += self.__getDescendants(i)
        else:
            temp += self.__getDescendants(code)

        return temp


    def __getDescendants(self, code):

        # throws exception if code is not a valid icd9 code
        if not self.isCode(code):
            return self.handleError(code)

        code = code.upper()

        try:
            return self.__descendants[code]
        except KeyError:
            return None


    """
    Input: <string> any icd9 code
    Returns: <list> the depth in the icd9 hierarchy the input code is at
    """
    def depth(self, code):

        # throws exception if input not a string
        if not isinstance(code, string_types):
            raise Exception('ICD9.depth() input must be string')

        #throws exception if input code is not valid icd9 code
        if not self.isCode(code):
            return self.handleError(code)

        code = code.upper()

        try:
            return self.__depths[code]
        except KeyError:
            return None


    """
    Input: <string> any icd9 code
    Returns: <string> The official description of the input icd9 code or null if no children exist
    """
    def description(self, code):

        # throws exception if input not a string or a list
        if not isinstance(code, string_types) and not isinstance(code, list):
            raise Exception('ICD9.description() input must be string or list')


        # throws exception if input code is not a valid icd9 code
        if not self.isCode(code):
            return self.handleError(code)

        code = code.upper()

        try:
            return self.__descriptions[code]
        except KeyError:
            return None


    """
    Input: <string> any icd9 code
            <int> the depth of the lowest parent you'd like to return
    Returns: <string> the parent of the input code at the input depth in the icd9 hierarchy
    """

    def abstract(self, code, depth):

        # throws exception if input not a string or a list
        if not isinstance(code, string_types) and not isinstance(code, list):
            raise Exception('ICD9.abstract() code input must be string or list')

        # throws exception if requested depth is not an integer
        try:
            depth = int(depth)
        except ValueError:
            raise Exception('ICD9.abstract() depth input must be integer')

        if not isinstance(depth, int):
            raise Exception('ICD9.abstract() depth input must be integer')


        temp = []

        #checks whether code is list
        if isinstance(code, list):
            for i in code:
                temp.append(self.__abstract(i, depth))
        else:
            temp.append(self.__abstract(code, depth))

        return list(temp)


    def __abstract(self, code, depth):

        #throws exception if code is not a valid icd9 code
        if not self.isCode(code):
            return self.handleError(code)

        code = code.upper()

        # iterates up the icd9 tree until depth matches requested depth
        # or the input code depth is higher than the requested depth
        cur_depth = self.__depths[code]
        while cur_depth > depth:
            code = self.__parents[code]
            cur_depth = self.__depths[code]
        return code


    """
    Input: <string> any icd9 code
    Return: <list> all icd9 codes between the input icd9 code and the highest parent in the hierarchy
    """
    def ancestors(self, code):

        # throws exception if input not a string or a list
        if not isinstance(code, string_types) and not isinstance(code, list):
            raise Exception('ICD9.ancestors() input must be string or list')

        codes = []

        #checks whether code is list
        if isinstance(code, list):
            for i in code:
                #collects ancestor codes
                codes += self.__ancestors(i)
            return codes
        else:
            return self.__ancestors(code)

    def __ancestors(self, code):
        code = str(code).upper()
        # throws exception if code is invalid icd9 code
        if not self.isCode(code):
            return self.handleError(code)

        codes = []
        cur_depth = self.__depths[code]
        codes.append(code)

        # iterates up the icd9 tree to retrieve all codes higher than
        # the input code
        while cur_depth > 1:
            code = self.__parents[code]
            cur_depth = self.__depths[code]
            codes.append(code)
        return list(reversed(codes))



    def isLeafNode(self, code):
        code = str(code).upper()
        if not self.isCode(code):
            #return self.handleError(code)
            return False

        if len(self.children(code)) > 1:
            return False
        elif self.children(code)[0]:
            return False
        else:
            return True
