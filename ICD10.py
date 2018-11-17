import json
from six import string_types

class ICD10:

    def __init__(self, errorHandle="NoDx"):
        import os
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.errorHandle = errorHandle

        self.__parents = json.load(open(dir_path + '/DxCodeHandler data/icd10/parents.json'))
        self.__depths = json.load(open(dir_path + '/DxCodeHandler data/icd10/depths.json'))
        self.__descriptions = json.load(open(dir_path + '/DxCodeHandler data/icd10/descriptions.json'))
        self.__descendants = json.load(open(dir_path + '/DxCodeHandler data/icd10/descendants.json'))
        self.__children = json.load(open(dir_path + '/DxCodeHandler data/icd10/children.json'))


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
            raise Exception('%s is not an ICD10 code' % code)
        elif self.errorHandle == "None":
            return None
        elif self.errorHandle == "false":
            return false
        elif isinstance(self.errorHandle, string_types):
            return self.errorHandle
        else:
            return "NoDx"


    def getAllCodes(self):
        output = set(self.__depths.keys())
        return output


    def isCode(self, codes):
        output = []
        if type(codes) is list:
            for i in codes:
                i = str(i).upper()
                try:
                    self.__depths[i]
                    output.append(True)
                except KeyError:
                    return False
        else:
            try:
                codes = str(codes).upper()
                self.__depths[codes]
                return True
            except KeyError:
                return False

        if len(output)==len(codes):
            return True
        else:
            return False


    """
    Input: <string> any icd9 code
    Returns: <string> the parent of the input icd9 code or null if no parent exists
    """
    def parent(self, codes):

        # throws exception if input not a string or a list
        if not isinstance(codes, string_types) and not isinstance(codes, list):
            raise Exception('ICD10.parent() input must be string or list')

        output = []

        if type(codes) is list:
            for i in codes:
                output.append(self.__parent[i])
            output = [m for m in output if m]
            output = list(set(output))
            if len(output) > 0:
                return output
            else:
                return None
        else:
            return self.__parent(codes)

    def __parent(self, code):

        # throws exception if code is not a valid icd10 code
        if not self.isCode(code):
            return self.handleError(code)

        code = code.upper()
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
            raise Exception('ICD10.children() input must be string or list')

        temp = []
        if type(code) == list:
            for i in code:
                temp += self.__getChildren(i)
        else:
            temp += self.__getChildren(code)

        return temp


    def __getChildren(self, code):

        # throws exception if code is not a valid icd10 code
        if not self.isCode(code):
            return self.handleError(code)

        code = code.upper()
        try:
            return self.__children[code]
        except KeyError:
            return [None]


    """
    Input: <string> any icd9 code
    Returns: <list> a list of all the descendants from the input code or null if no descendants exist
    """
    def descendants(self, code):

        # throws exception if input not a string
        if not isinstance(code, string_types):
            raise Exception('ICD10.descendants() input must be string')

        # throws exception if code is not a valid icd10 code
        if not self.isCode(code):
            return self.handleError(code)

        code = code.upper()
        temp = [code]
        try:
            temp += self.__descendants[code]
            return temp
        except KeyError:
            return None


    """
    Input: <string> any icd9 code
    Returns: <list> the depth in the icd9 hierarchy the input code is at
    """
    def depth(self, code):

        # throws exception if input not a string or a list
        if not isinstance(code, string_types):
            raise Exception('ICD10.depth() input must be string')

        # throws exception if code is not a valid icd10 code
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
    
    def description(self, code):
    
        # throws exception if code is not a valid icd10 code
        if not self.isCode(code):
            raise Exception('%s is not an ICD10 code' % code)
    
        code = code.upper()
        try:
            return self.__descriptions[code]
        except KeyError:
            return None
    """

    """
    Input: <string> any icd9 code
            <int> the depth of the lowest parent you'd like to return
    Returns: <string> the parent of the input code at the input depth in the icd9 hierarchy
    """

    def abstract(self, code, depth):

        # throws exception if input not a string or a list
        if not isinstance(code, string_types) and not isinstance(code, list):
            raise Exception('ICD10.abstract() input must be string or list')


        # throws exception if requested depth is not an integer
        try:
            depth = int(depth)
        except ValueError:
            raise Exception('ICD10.abstract() depth input must be integer')

        if not isinstance(depth, int):
            raise Exception('ICD10.abstract() depth input must be integer')


        temp = []
        if type(code)==list:
            for i in code:
                temp.append(self.__abstract(i, depth))
        else:
            temp.append(self.__abstract(code, depth))

        return list(temp)


    def __abstract(self, code, depth):

        # throws exception if code is not a valid icd10 code
        if not self.isCode(code):
            return self.handleError(code)

        code = code.upper()
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
            raise Exception('ICD10.ancestors() input must be string or list')

        codes = []
        if type(code) == list:
            for i in code:
                codes += self.__ancestors(i)
            return codes
        else:
            return self.__ancestors(code)

    def __ancestors(self, code):
        code = str(code).upper()
        # throws exception if code is not a valid icd10 code
        if not self.isCode(code):
            return self.handleError(code)

        codes = []
        cur_depth = self.__depths[code]
        codes.append(code)
        while cur_depth > 1:
            code = self.__parents[code]
            cur_depth = self.__depths[code]
            codes.append(code)
        return list(reversed(codes))


    def isLeafNode(self, code):
        code = str(code).upper()
        if not self.isCode(code):
            return self.handleError(code)

        if len(self.children(code)) > 1:
            return False
        elif self.children(code)[0]:
            return False
        else:
            return True
