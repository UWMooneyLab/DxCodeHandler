import json
from six import string_types


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