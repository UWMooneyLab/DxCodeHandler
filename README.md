# DxCodeHandler

This package has a collection of modules for working with clinical data from the University of Washington Medical Center, specifically billing codes.

[DxCodeHandler](#DxCodeHandler)

<a name="DxCodeHandler"></a>
## DxCodeHandler
There are three toolkits in the DxCodeHandler module:

[ICD9](#ICD)

[ICD10](#ICD)

[Converter](#Converter)

<a name="ICD"></a>
### ICD9 and ICD10
An instance of either of these classes has a collection of functions that will allow easy manipulation of ICD billing codes as well as easy traversal of the ICD hierarchy. For a deeper understanding of both the ICD9 and ICD10 hierarchy structures, explore [ICD9](http://www.icd9data.com/2015/Volume1/default.htm) and [ICD10](http://www.icd10data.com/ICD10CM/Codes).

#### Importing and creating an instance
Both the ICD9 and ICD10 classes have the same functions; however, ICD9 will be used as a demostration
```
from library.DxCodeHandler import ICD9
icd9 = ICD9()

from library.DxCodeHandler import ICD10
icd10 = ICD10()
```
#### description()

Returns the description of the input code
```
code = 'E810'
icd9.description(code) 
Motor vehicle traffic accident involving collision with train
```
#### children()
Returns all the children of the input code in the icd9 hierarchy
```
code = 'E810'
icd9.children(code)
['E810.0', 'E810.1', 'E810.2', 'E810.3', 'E810.4', 'E810.5', 'E810.6', 'E810.7', 'E810.8', 'E810.9']
```
A list of codes can also be used as input, returning a list of all the children of all the input codes.
```
codes = ['E810', '240']
icd9.children(codes)
['E810.5', 'E810.8', 'E810.7', 'E810.0', 'E810.9', 'E810.1', 'E810.3', 'E810.6', 'E810.2', 'E810.4', '240.9', '240.0']
```
#### parent()
Returns the parent of the code in the icd9 hierarchy
```
code = 'E810'
icd9.parent(code)
E810-E819
```
A list of codes can also be used as input, returning a list of all the parents of all the input codes.
```
codes = ['E810', '240']
icd9.parent(codes)
['240-246', 'E810-E819']
```

#### depth()
Returns the node depth of the input code in the icd9 hierarchy tree
```
code = 'E810'
icd9.depth(code)
3
```
#### isCode()
Returns whether the input code exists in the icd9 hierarchy
```
code = 'E810'
icd9.isCode(code)
True
```

#### descendants()
Returns a list of all codes, including input code, further down the icd9 hierarchy from the input code
```
code = 'E810'
icd9.descendants(code)
['E810', 'E810.5', 'E810.8', 'E810.7', 'E810.0', 'E810.9', 'E810.1', 'E810.3', 'E810.6', 'E810.2', 'E810.4']
```

#### abstract()
Returns the code that is at the input code icd9 tree depth above the input code

If the input depth is below the input code, the function will return the input code
```
code = 'E810'
icd9.abstract(code, 1)
E000-E999
```
A list of codes can also be used as input, returning all the codes abstracted to the requested tree depth.
```
codes = ['E810', '240']
icd9.abstract(codes, 2)
['E810-E819', '240-246']
```
#### ancestors()
Returns all the codes above the input code in the icd9 hierarchy, including the input code
```
code = 'E810'
icd9.ancestors(code)
['E000-E999', 'E810-E819', 'E810']
```
A list of codes can also be used as input, returning a list of all the ancestors of all the input codes.

Repeating codes are not removed.
```
codes = ['E810', '240']
icd9.ancestors(codes)
['E000-E999', 'E810-E819', 'E810', '240-279', '240-246', '240']
```

#### getAllCodes()
Returns all possible codes in the requested ICD ontology
```
icd9.getAllCodes()
['very', 'long', 'list', 'of', 'ICD9', 'codes']
```
<a name="Converter"></a>
### Converter
An instance of the Converter class has a collection of functions that will allow easy conversion of ICD billing codes between the two standards. For a deeper understanding of both the ICD9 and ICD10 hierarchy structures, explore [ICD9](http://www.icd9data.com/2015/Volume1/default.htm) and [ICD10](http://www.icd10data.com/ICD10CM/Codes).

The conversions are based on the [2015 ICD10](https://www.cms.gov/Medicare/Coding/ICD10/2015-ICD-10-CM-and-GEMs.html) and [2017 ICD10](https://www.cms.gov/Medicare/Coding/ICD10/2017-ICD-10-CM-and-GEMs.html) CMS General Equivalency Mappings

#### Importing and creating an instance
Create a Converter instance.
```
from library.DxCodeHandler import Converter
con = Converter()
```
#### convert_9_10()
This function will check that the input code is an ICD9 code, then, if possible, convert it to the ICD10 closest equivalent code or collection of codes.
```
code = 'S15.121S'
con.convert_9_10(code)
['908.3']
```
Some codes convert in a one to many fashion, thus, the equivalent ICD9 of an ICD10 code could be a collection of codes.
```
code = 'T41.3X1A'
con.convert_9_10(code)
['968.5', '968.9', 'E855.2']
```
If the code cannot be converted, the function will raise an exception
```
code = 'E935.2'
con.convert_9_10(code)
Exception: E935.2 cannot be converted to ICD10  #An E935.2 ICD10 equivalent does not exist
```
#### convert_10_9()
This function will check that the input code is an ICD10 code then, if possible, convert it to the ICD9 closest equivalent code or collection of codes.
```
code = '765.18'
con.convert_10_9(code)
['P07.18']
```
Some codes convert in a one to many fashion, thus, the equivalent ICD9 of an ICD10 code could be a collection of codes.
```
code = '806.24'
con.convert_10_9(code)
['S22.049A', 'S24.152A', 'S22.019A', 'S24.151A', 'S22.029A', 'S22.059A', 'S22.039A']
```
If the code cannot be converted, the function will raise an exception
```
code = 'T42.3X6D'
con.convert_10_9(code)
Exception: T42.3X6D has No Dx equivalent in ICD9
```
