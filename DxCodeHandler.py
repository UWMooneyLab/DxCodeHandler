import json
from six import string_types

class ICD9:
    """
    The ICD9 class captures the hierarchy and descriptions for the ICD9 coding standard
    The source data files were developed from CMS mapping files
    """
    def __init__(self):
        '''
        Loads the dependancies for the ICD9 class
        All the mapping data is stored in JSON files which are loaded into dicts
        '''
        import os
        dir_path = os.path.dirname(os.path.realpath(__file__))

        self.__parents = json.load(open(dir_path + '/DxCodeHandler data/icd9/parents2.json'))
        self.__depths = json.load(open(dir_path + '/DxCodeHandler data/icd9/depths2.json'))
        self.__descriptions = json.load(open(dir_path + '/DxCodeHandler data/icd9/descriptions3.json'))
        self.__descendants = json.load(open(dir_path + '/DxCodeHandler data/icd9/descendants.json'))
        self.__children = json.load(open(dir_path + '/DxCodeHandler data/icd9/children.json'))


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
            raise Exception('%s is not an ICD9 code' % code)

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
        #if not self.isCode(code):
        #    raise Exception('%s is not an ICD9 code' % code)

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

        # throws exception if input not a string
        if type(code) != str:
            raise Exception('ICD9.descendants() input must be string')

        # throws exception if code is not a valid icd9 code
        if not self.isCode(code):
            raise Exception('%s is not an ICD9 code' % code)

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

        # throws exception if input not a string
        if not isinstance(code, string_types):
            raise Exception('ICD9.depth() input must be string')

        #throws exception if input code is not valid icd9 code
        if not self.isCode(code):
            raise Exception('%s is not an ICD9 code' % code)

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
            raise Exception('%s is not an ICD9 code' % code)

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
            raise Exception('%s is not an ICD9 code' % code)

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
            raise Exception('%s is not an ICD9 code' % code)

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
            #raise Exception('%s is not an ICD9 code' % code)
            return False

        if len(self.children(code)) > 1:
            return False
        elif self.children(code)[0]:
            return False
        else:
            return True




class ICD10:

    def __init__(self):
        import os
        dir_path = os.path.dirname(os.path.realpath(__file__))

        self.__parents = json.load(open(dir_path + '/DxCodeHandler data/icd10/parents.json'))
        self.__depths = json.load(open(dir_path + '/DxCodeHandler data/icd10/depths.json'))
        #self.__descriptions = json.load(open(dir_path + '/DxCodeHandler data/icd10/descriptions.json'))
        self.__descendants = json.load(open(dir_path + '/DxCodeHandler data/icd10/descendants.json'))
        self.__children = json.load(open(dir_path + '/DxCodeHandler data/icd10/children.json'))



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
            raise Exception('%s is not an ICD10 code' % code)

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
            raise Exception('%s is not an ICD10 code' % code)

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
            raise Exception('%s is not an ICD10 code' % code)

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
            raise Exception('%s is not an ICD10 code' % code)


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
            raise Exception('%s is not an ICD10 code' % code)

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
            raise Exception('%s is not an ICD10 code' % code)

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
            raise Exception('%s is not an ICD10 code' % code)

        if len(self.children(code)) > 1:
            return False
        elif self.children(code)[0]:
            return False
        else:
            return True




class Converter:
    def __init__(self):
        import os
        dir_path = os.path.dirname(os.path.realpath(__file__))

        """
        Load all our known ICD10 codes into a set for cross reference
        """
        self.__all_icd10 = json.load(open(dir_path + '/DxCodeHandler data/icd10/depths.json'))
        self.__all_icd10 = set(self.__all_icd10.keys())

        """
        Load all our known ICD9 codes into a set for cross reference
        """
        self.__all_icd9  = json.load(open(dir_path + '/DxCodeHandler data/icd9/depths2.json'))
        self.__all_icd9  = set(self.__all_icd9.keys())

        """
        Load all mappings from ICD10 to ICD9 including GEM files and CUI mapped codes
        """
        self.__icd10_2_icd9 = json.load(open(dir_path + '/DxCodeHandler data/conversions/icd10_2_icd9_conversion_2017.json'))
        self.__icd10_cui_icd9 = json.load(open(dir_path + '/DxCodeHandler data/conversions/icd10_cui_icd9.json'))

        """
        Load all mappings from ICD9 to ICD10 including GEM files and CUI mapped code
        """
        self.__icd9_2_icd10 = json.load(open(dir_path + '/DxCodeHandler data/conversions/icd9_2_icd10_conversion.json'))
        self.__icd9_cui_icd10 = json.load(open(dir_path + '/DxCodeHandler data/conversions/icd9_cui_icd10.json'))

        """
        Load all mappings from 2016 ICD10 to 2017 ICD10
        This will have to be updated on an annual basis.
        """
        self.__icd10_conversion_table = json.load(open(dir_path + '/DxCodeHandler data/conversions/2017_conversion_table.json'))


    def __isICD10Code(self, code):
        code = str(code).upper()

        if code in self.__all_icd10:
            return True
        else:
            return False

    def __isICD9Code(self, code):
        code = str(code).upper()

        if code in self.__all_icd9:
            return True
        else:
            return False

    """
    Input: <string> icd10 code
    Return: <list> general equivalent icd9 code or multiple icd9 codes that are generally equivalent to the input icd10 code
    Source of general equivalency mappings URL: https://www.cms.gov/Medicare/Coding/ICD10/2017-ICD-10-CM-and-GEMs.html
    """

    def convert_10_9(self, code):
        code = str(code).upper()
        old_code = code
        change = False
        if self.__icd10_mapped(code):
            code = self.__icd10_mapped(code)

        try:
            self.__isICD10Code(code)
        except KeyError:
            raise Exception('%s is not an ICD10 code' % code)

        try:
            code = self.__icd10_2_icd9[code]
            change = True
        except KeyError:
            pass

        if code[0] == "NoD.x":
            raise Exception('%s has No Dx equivalent in ICD9' % old_code)
        elif change:
            return code
        else:
            pass

        try:
            code = self.__icd10_cui_icd9[code]
            return code
        except KeyError:
            pass

        raise Exception('%s cannot be converted to ICD9' % code)


    """
    Input: <string> icd9 code
    Return: <list> general equivalent icd10 code or multiple icd10 codes that are generally equivalent to input icd9 code
    Source of general equivalency mappings URL: https://www.cms.gov/Medicare/Coding/ICD10/2015-ICD-10-CM-and-GEMs.html
    """
    def convert_9_10(self, code):
        code = str(code).upper()
        old_code = code
        change = False

        try:
            self.__isICD9Code(code)
        except KeyError:
            raise Exception('%s is not an ICD9 code' % code)

        try:
            code = self.__icd9_2_icd10[code]
            change = True
        except KeyError:
            pass

        if code[0] == "NoD.x":
            raise Exception('%s has No Dx equivalent in ICD10' % old_code)
        elif change:
            return code
        else:
            pass

        try:
            code = self.__icd9_cui_icd10[code]
            return code
        except KeyError:
            pass

        raise Exception('%s cannot be converted to ICD10' % code)

    """
    Checks for code changes from 2016 to 2017 in ICD10.
    """
    def __icd10_mapped(self, code):
        code = str(code)
        code = code.upper()
        try:
            return self.__icd10_conversion_table[code]
        except KeyError:
            return None