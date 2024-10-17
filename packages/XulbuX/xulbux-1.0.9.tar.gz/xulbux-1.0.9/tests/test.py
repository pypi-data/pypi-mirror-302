import XulbuX as xx
import regex as rx
import re

VERSION = '1.0.0'
code = '''
some_func(func() + add(a, b * test()) / mod(c, (a * b)))
<x.tag-name "test \\">\\"".test = test = '>' = test>
'''
# print(f'ORIGINAL:  {code}')
# print(f'MATCHES:   {re.findall(r'<' + xx.Regex.all_except('>') + r'>', code)}')
# print(f'REPLACED:  {re.sub(r'<([\w.-]+)' + xx.Regex.all_except('>', is_group=True) + r'>', r'<\1 /> :: \2', code)}')  # EMPTY TAG
# print(f'OUTSIDE:   {re.findall(xx.Regex.outside_strings('test'), code)}')
# print(f'REPLACED:  {re.sub(xx.Regex.outside_strings('test'), 'outside', code)}')
# print(f'BRACKETS:  {rx.sub(xx.Regex.brackets('(',')', is_group=True), r'::\1::', code)}')
# print(f'FUNCTION:  {rx.sub(xx.Regex.func_call(func_name='add'), r'::\1::\2::', code)}')
l = ['fruit and vegetables', 4, [1, 2, 3], [], ['', '  ', None], ['apples', 'bananas \n\'bananas\'', '', '  ', None, '  oranges  '], ['carrots', '  broccoli  ', 'broccoli \t"broccoli"', 'celery'], ['chips', 'popcorn'], ['chips', 'popcorn']]
t = ('fruit and vegetables', 4, (1, 2, 3), (), ('', '  ', None), ('apples', 'bananas \n\'bananas\'', '', '  ', None, '  oranges  '), ('carrots', '  broccoli  ', 'broccoli \t"broccoli"', 'celery'), ('chips', 'popcorn'), ('chips', 'popcorn'))
d = {
  'healthy': {
    'fruit': [[], ['apples', 'bananas \n\'bananas\'', '', '  ', None, '  oranges  ']],
    'vegetables': ((), ('carrots', '  broccoli  ', 'broccoli \t"broccoli"', 'celery')),
    'snacks': ['chips', 'popcorn'],
    'snacks': ['chips', 'popcorn']
  },
  'is_unhealthy': False,
  'empty_l_items': ['', '  ', None],
  'empty_t_items': ('', '  ', None),
  'empty_d_items': {
    'nothing': ['', '  ', None, ['', '  ', None]],
    'nothing': ('', '  ', None, ('', '  ', None))
    },
  'empty_l': [],
  'empty_t': (),
  'empty_d': {},
  'empty_item': '',
  'spaces': '  ',
  'empty_item': None,
  'number_items': [1, 2, 3],
  'number_item': 4,
  5: set([1, 1, 2, 3]),
  6: frozenset([1, 1, 2, 3]),
  7: complex(1, 2),
  8: float('inf'),
  9: float('-inf'),
  10: float('nan'),
}
obj1 = ['>> FULL ITEM IS COMMENT', ['app>> CENTER PART OF ITEM IS COMMENT<<les', 'bananas', 'bananas', '', 'oranges  >> LAST PART OF ITEM IS COMMENT', '>> FULL ITEM IS COMMENT'], ['carrots', '>> FIRST PART OF ITEM IS COMMENT <<  broccoli', 'celery']]
obj2 = ('>> FULL ITEM IS COMMENT', ('app>> CENTER PART OF ITEM IS COMMENT<<les', 'bananas', 'oranges  >> LAST PART OF ITEM IS COMMENT', '>> FULL ITEM IS COMMENT'), ('carrots', '>> FIRST PART OF ITEM IS COMMENT <<  broccoli', 'celery'))
obj3 = {
  'healthy': {
    'fruit': ['app>> CENTER PART OF ITEM IS COMMENT<<les', 'bananas', 'oranges  >> LAST PART OF ITEM IS COMMENT', '>> FULL ITEM IS COMMENT'],
    'vegetables': ('carrots', '>> FIRST PART OF ITEM IS COMMENT <<  broccoli', 'celery'),
  },
  'is_unhealthy': False
}
_obj1 = [['val1', 'val2', 'val3'], ['val1', 'val2', 'val3']]
_obj2 = (('val1', 'val2', 'val3'), ('val1', 'val2', 'val3'))
_obj3 = {
  'dict': {
    'key1': ['val1', 'val2', 'val3'],
    'key2': ('val1', 'val2', 'val3')
  },
  'key': 'val'
}
# obj1, obj2, obj3 = xx.Data.remove_comments((obj1, obj2, obj3))
# print(f'OBJ1: {obj1}')
# print(f'OBJ2: {obj2}')
# print(f'OBJ3: {obj3}')
# print()
# id1 = xx.Data.get_path_id(obj1, '0->apples')
# id2 = xx.Data.get_path_id(obj2, '1->2')
# id3 = xx.Data.get_path_id(obj3, 'healthy->fruit->0')
# print(f'ID1: {id1}')
# print(f'ID2: {id2}')
# print(f'ID3: {id3}')
# print()
# print(xx.Data.set_value_by_path_id(_obj1, f'{id1}::pineapples'))
# print(xx.Data.set_value_by_path_id(_obj2, f'{id2}::pineapples'))
# print(xx.Data.set_value_by_path_id(_obj3, f'{id3}::pineapples'))
# print()
# print(f'GOT1: {xx.Data.get_value_by_path_id(obj1, id1)}')
# try: print(f'GOT1 KEY: {xx.Data.get_value_by_path_id(obj1, id1, get_key=True)}')
# except Exception as e: print(f'ERROR: {e}')
# print(f'GOT2: {xx.Data.get_value_by_path_id(obj2, id2)}')
# try: print(f'GOT2 KEY: {xx.Data.get_value_by_path_id(obj2, id2, get_key=True)}')
# except Exception as e: print(f'ERROR: {e}')
# print(f'GOT3: {xx.Data.get_value_by_path_id(obj3, id3)}')
# print(f'GOT3 KEY: {xx.Data.get_value_by_path_id(obj3, id3, get_key=True)}')
# print()

xx.FormatCodes.print(
  rf'''  [_|b|#7075FF]               __  __              
  [b|#7075FF]  _  __ __  __/ / / /_  __  ___  __
  [b|#7075FF] | |/ // / / / / / __ \/ / / | |/ /
  [b|#7075FF] > , </ /_/ / /_/ /_/ / /_/ /> , < 
  [b|#7075FF]/_/|_|\____/\__/\____/\____//_/|_|  [*|BG:#7B7C8F|#000] v[b]{VERSION} [*]

  [i|#FF806A] A LOT OF SMALL, USEFUL FUNCTIONS [*]

  [b|#75A2FF]Usage:[*]
    [#FF9E6A]import [#77EFEF]XulbuX [#FF9E6A]as [#77EFEF]xx[*]

  [b|#75A2FF]Includes:[*]
    -  CUSTOM TYPES:
         [#AA90FF]rgb[#505050]/([i|#60AAFF]int[_|#505050],[b]/(intaaaaaaaaaaaaaaaaaaaaaaaaaaaaa[default]aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa),[i|#60AAFF]int[_|#505050],[i|#60AAFF]float[_|#505050])[*]
         [#AA90FF]hsl[#505050]/([i|#60AAFF]int[_|#505050],[i|#60AAFF]int[_|#505050],[i|#60AAFF]int[_|#505050],[i|#60AAFF]float[_|#505050])[*]
         [#AA90FF]hexa[#505050]/([i|#60AAFF]str[_|#505050])[*]
    -  DIRECTORY OPERATIONS     [#77EFEF]xx[#505050].[#AA90FF]Dir[*]
    -  FILE OPERATIONS          [#77EFEF]xx[#505050].[#AA90FF]File[*]
    -  JSON FILE OPERATIONS     [#77EFEF]xx[#505050].[#AA90FF]Json[*]
    -  SYSTEM ACTIONS           [#77EFEF]xx[#505050].[#AA90FF]System[*]
    -  MANAGE ENVIRONMENT VARS  [#77EFEF]xx[#505050].[#AA90FF]Env_vars[*]
    -  CMD LOG AND ACTIONS      [#77EFEF]xx[#505050].[#AA90FF]Cmd[*]
    -  PRETTY PRINTING          [#77EFEF]xx[#505050].[#AA90FF]FormatCodes[*]
    -  COLOR OPERATIONS         [#77EFEF]xx[#505050].[#AA90FF]Color[*]
    -  DATA OPERATIONS          [#77EFEF]xx[#505050].[#AA90FF]Data[*]
    -  STR OPERATIONS           [#77EFEF]xx[#505050].[#AA90FF]String[*]
    -  CODE STRING OPERATIONS   [#77EFEF]xx[#505050].[#AA90FF]Code[*]
    -  REGEX PATTERN TEMPLATES  [#77EFEF]xx[#505050].[#AA90FF]Regex[*]
  [_]''', '#9AB8F7')


xx.Cmd.pause_exit(pause=True)
