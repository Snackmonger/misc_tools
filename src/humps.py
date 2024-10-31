"""
Tool for converting text between different programming-friendly case systems.

Version
-------
This program originally from github.com/nficano/humps

Original docstring: "This module contains all the core logic for humps."

This version revised by github.com/snackmonger in Oct 2024:
- Add type annotations to function signatures
- Remove ``Mapping`` and ``list`` types so the program only deals with ``str``. 
- Rewrite docstrings for NumPy style, just because this is consistent with
my other projects. 
- Move existing tests from separate files into docstrings as examples, so 
this can serve as a standalone file like the other miscellaneous tools.
- The current version of humps on GitHub is not consistent with the current 
version on PyPi, causing some tests to fail. Reverted the SPLIT_RE regex to 
previous and tests now pass.

Examples
--------
>>> camelize("jack_in_the_box")
'jackInTheBox'
>>> decamelize("rubyTuesdays")
'ruby_tuesdays'
>>> depascalize("UnosPizza")
'unos_pizza'
>>> pascalize("red_robin")
'RedRobin'
>>> kebabize("white_castle")
'white-castle'
>>> dekebabize("taco-bell")
'taco_bell'

In the original version of the program, the functions could also take
dictionaries and lists of dictionaries, and change the case of the keys.
I didn't like how this made all function returns appear to be a Union, 
so I changed it to str only. Now, dictionary conversion must be done with
comprehensions, but my linter is happy:

>>> x = {"number_one": 1, "number_two": 2, "number_twenty": 20}
>>> y = [{"number_one": 1, "number_two": 2}, {"number_ten": 10, "number_twenty": 20}]
>>> {camelize(k):v for k, v in x.items()}
{'numberOne': 1, 'numberTwo': 2, 'numberTwenty': 20}
>>> [{camelize(k): v} for e in y for k, v in e.items()]
[{'numberOne': 1}, {'numberTwo': 2}, {'numberTen': 10}, {'numberTwenty': 20}]
>>> [{kebabize(k): v} for e in y for k, v in e.items()]
[{'number-one': 1}, {'number-two': 2}, {'number-ten': 10}, {'number-twenty': 20}]
"""
import re

ACRONYM_RE = re.compile(r"([A-Z\d]+)(?=[A-Z\d]|$)")
PASCAL_RE = re.compile(r"([^\-_]+)")
SPLIT_RE = re.compile(r"([\-_]*[A-Z][^A-Z]*[\-_]*)")
# SPLIT_RE = re.compile(r"([\-_]*(?<=[^0-9])(?=[A-Z]+)[^A-Z]*[\-_]*)")
UNDERSCORE_RE = re.compile(r"(?<=[^\-_])[\-_]+[^\-_]")


def pascalize(string: str) -> str:
    '''
    Convert a string to pascal case.

    Parameters
    ----------
    string : str
        A string to convert.

    Returns
    -------
    str
        A converted string.

    Examples
    --------
    >>> pascalize('fallback_url')
    'FallbackUrl'
    >>> pascalize('scrubber_media_url')
    'ScrubberMediaUrl'
    >>> pascalize('dash_url')
    'DashUrl'
    >>> pascalize('_fallback_url')
    '_FallbackUrl'
    >>> pascalize('__scrubber_media___url_')
    '__ScrubberMediaUrl_'
    >>> pascalize('_url__')
    '_Url__'
    >>> pascalize('API')
    'API'
    >>> pascalize('_API_')
    '_API_'
    >>> pascalize('__API__')
    '__API__'
    >>> pascalize('APIResponse')
    'APIResponse'
    >>> pascalize('_APIResponse_')
    '_APIResponse_'
    >>> pascalize('__APIResponse__')
    '__APIResponse__'
    >>> pascalize('')
    ''
    >>> pascalize(None)
    ''
    '''
    s = _ensure_str(string)
    if s.isupper() or s.isnumeric():
        return string

    def _replace_fn(match: re.Match[str]):
        return match.group(1)[0].upper() + match.group(1)[1:]

    s = camelize(PASCAL_RE.sub(_replace_fn, s))
    return s[0].upper() + s[1:] if len(s) != 0 else s


def camelize(string: str) -> str:
    """
    Convert a string to camel case.

    Parameters
    ----------
    string : str
        A string to convert.

    Returns
    -------
    str
        A converted string.
    
    Examples
    --------
    >>> camelize('fallback_url')
    'fallbackUrl'
    >>> camelize('scrubber_media_url')
    'scrubberMediaUrl'
    >>> camelize('dash_url')
    'dashUrl'
    >>> camelize('_fallback_url')
    '_fallbackUrl'
    >>> camelize('__scrubber_media___url_')
    '__scrubberMediaUrl_'
    >>> camelize('_url__')
    '_url__'
    >>> camelize('API')
    'API'
    >>> camelize('_API_')
    '_API_'
    >>> camelize('__API__')
    '__API__'
    >>> camelize('APIResponse')
    'APIResponse'
    >>> camelize('_APIResponse_')
    '_APIResponse_'
    >>> camelize('__APIResponse__')
    '__APIResponse__'
    >>> camelize('whatever_10')
    'whatever10'
    >>> camelize('test-1-2-3-4-5-6')
    'test123456'
    >>> camelize('test_n_test')
    'testNTest'
    >>> camelize('field_value_2_type')
    'fieldValue2Type'
    >>> camelize('')
    ''
    >>> camelize(None)
    ''
    """
    s = _ensure_str(string)
    if s.isupper() or s.isnumeric():
        return string

    if len(s) != 0 and not s[:2].isupper():
        s = s[0].lower() + s[1:]

    # For string "hello_world", match will contain
    #             the regex capture group for "_w".
    return UNDERSCORE_RE.sub(lambda m: m.group(0)[-1].upper(), s)


def kebabize(string: str) -> str:
    """
    Convert a string to kebab case.

    Parameters
    ----------
    string : str
        A string to convert.

    Returns
    -------
    str
        A converted string.

    Examples
    --------
    >>> kebabize('fallback_url')
    'fallback-url'
    >>> kebabize('scrubber_media_url')
    'scrubber-media-url'
    >>> kebabize('dash_url')
    'dash-url'
    >>> kebabize('_fallback_url')
    '_fallback-url'
    >>> kebabize('__scrubber_media___url_')
    '__scrubber-media-url_'
    >>> kebabize('_url__')
    '_url__'
    >>> kebabize('API')
    'API'
    >>> kebabize('_API_')
    '_API_'
    >>> kebabize('__API__')
    '__API__'
    >>> kebabize('API_Response')
    'API-Response'
    >>> kebabize('_API_Response_')
    '_API-Response_'
    >>> kebabize('__API_Response__')
    '__API-Response__'
    """
    s = _ensure_str(string)
    if s.isnumeric():
        return string

    if not (s.isupper()) and (is_camelcase(s) or is_pascalcase(s)):
        return (
            _separate_words(
                string=_fix_abbreviations(s),
                separator="-"
            ).lower()
        )

    return UNDERSCORE_RE.sub(lambda m: "-" + m.group(0)[-1], s)


def decamelize(string: str) -> str:
    """
    Convert a string to snake case.

    Parameters
    ----------
    string : str
        A string to convert.

    Returns
    -------
    str
        A converted string.

    Examples
    --------
    >>> decamelize('symbol')
    'symbol'
    >>> decamelize('lastPrice')
    'last_price'
    >>> decamelize('changePct')
    'change_pct'
    >>> decamelize('impliedVolatility')
    'implied_volatility'
    >>> decamelize('_symbol')
    '_symbol'
    >>> decamelize('changePct_')
    'change_pct_'
    >>> decamelize('_lastPrice__')
    '_last_price__'
    >>> decamelize('__impliedVolatility_')
    '__implied_volatility_'
    >>> decamelize('API')
    'API'
    >>> decamelize('_API_')
    '_API_'
    >>> decamelize('__API__')
    '__API__'
    >>> decamelize('APIResponse')
    'api_response'
    >>> decamelize('_APIResponse_')
    '_api_response_'
    >>> decamelize('__APIResponse__')
    '__api_response__'
    >>> decamelize('_itemID')
    '_item_id'
    >>> decamelize('memMB')
    'mem_mb'
    >>> decamelize('sizeX')
    'size_x'
    >>> decamelize('aB')
    'a_b'
    >>> decamelize('testNTest')
    'test_n_test'
    """
    s = _ensure_str(string)
    if s.isupper() or s.isnumeric():
        return string

    return _separate_words(_fix_abbreviations(s)).lower()


def depascalize(string: str) -> str:
    """
    Convert a string to snake case.

    Parameters
    ----------
    string : str
        A string to convert.

    Returns
    -------
    str
        A converted string.
    """
    return decamelize(string)


def dekebabize(string: str) -> str:
    """
    Convert a string to snake case.

    Parameters
    ----------
    string : str
        A string to convert.

    Returns
    -------
    str
        A converted string.

    Examples
    --------
    >>> dekebabize('symbol')
    'symbol'
    >>> dekebabize('last-price')
    'last_price'
    >>> dekebabize('Change-Pct')
    'Change_Pct'
    >>> dekebabize('implied-Volatility')
    'implied_Volatility'
    >>> dekebabize('_symbol')
    '_symbol'
    >>> dekebabize('change-pct_')
    'change_pct_'
    >>> dekebabize('_last-price__')
    '_last_price__'
    >>> dekebabize('__implied-volatility_')
    '__implied_volatility_'
    >>> dekebabize('API')
    'API'
    >>> dekebabize('_API_')
    '_API_'
    >>> dekebabize('__API__')
    '__API__'
    >>> dekebabize('API-Response')
    'API_Response'
    >>> dekebabize('_API-Response_')
    '_API_Response_'
    >>> dekebabize('__API-Response__')
    '__API_Response__'
    >>> dekebabize('12345')
    '12345'
    """
    s = _ensure_str(string)
    if s.isnumeric():
        return string

    return s.replace("-", "_")


def is_camelcase(string: str) -> bool:
    '''
    Determine if a string is in camel case.

    Parameters
    ----------
    string : str
        A string to test.

    Returns
    -------
    bool
        True, if the string is in camel case.
    '''
    return string == camelize(string)


def is_pascalcase(string: str) -> bool:
    '''
    Determine if a string is in pascal case.

    Parameters
    ----------
    string : str
        A string to test.

    Returns
    -------
    bool
        True, if the string is in pascal case.
    '''
    return string == pascalize(string)


def is_kebabcase(string: str) -> bool:
    """
    Determine if a string is kebab case.

    Parameters
    ----------
    string : str
        A string to test.

    Returns
    -------
    bool
        True, if the string is in kebab case.
    """
    return string == kebabize(string)


def is_snakecase(string: str) -> bool:
    """
    Determine if a string is snake case.

    Parameters
    ----------
    string : str
        A string to test.

    Returns
    -------
    bool
        True, if the string is in snake case.
    """
    if is_kebabcase(string) and not is_camelcase(string):
        return False

    return string == decamelize(string)


def _ensure_str(_in: str | None) -> str:
    '''
    Return an empty string if the input is None, otherwise return the input
    stripped of whitespace.

    Parameters
    ----------
    _in : str | None
        An object that might be a string or None.

    Returns
    -------
    str
        An empty string, or the original string stripped of whitespace.
    '''
    return "" if _in is None else re.sub(r"\s+", "", str(_in))

def _fix_abbreviations(string: str) -> str:
    '''
    Rewrite incorrectly cased acronyms, initialisms, and abbreviations,
    allowing them to be decamelized correctly. For example, given the string
    "APIResponse", this function is responsible for ensuring the output is
    "api_response" instead of "a_p_i_response".

    Parameters
    ----------
    string : str
        A string to be corrected.

    Returns
    -------
    str
        A corrected string.

    Examples
    --------
    >>> decamelize('PERatio')
    'pe_ratio'
    >>> decamelize('HTTPResponse')
    'http_response'
    >>> decamelize('_HTTPResponse')
    '_http_response'
    >>> decamelize('_HTTPResponse__')
    '_http_response__'
    >>> decamelize('BIP73')
    'BIP73'
    >>> decamelize('BIP72b')
    'bip72b'
    >>> decamelize('memMB')
    'mem_mb'
    >>> decamelize('B52Thing')
    'b52_thing'
    '''
    return ACRONYM_RE.sub(lambda m: m.group(0).title(), string)


def _separate_words(string: str, separator: str="_") -> str:
    '''
    Split words that are separated by case differentiation.

    Parameters
    ----------
    string : str
        The string to be separated.
    separator : str, optional
        The character that will be used as the separator, by default "_"

    Returns
    -------
    str
        A string with the separator character at case boundaries.  

    Examples
    --------
    >>> _separate_words('HelloWorld')
    'Hello_World'
    >>> _separate_words('_HelloWorld')
    '_Hello_World'
    >>> _separate_words('__HelloWorld')
    '__Hello_World'
    >>> _separate_words('HelloWorld_')
    'Hello_World_'
    >>> _separate_words('HelloWorld__')
    'Hello_World__'
    >>> _separate_words('helloWorld')
    'hello_World'
    >>> _separate_words('_helloWorld')
    '_hello_World'
    >>> _separate_words('__helloWorld')
    '__hello_World'
    >>> _separate_words('helloWorld_')
    'hello_World_'
    >>> _separate_words('helloWorld__')
    'hello_World__'
    >>> _separate_words('hello_world')
    'hello_world'
    >>> _separate_words('_hello_world')
    '_hello_world'
    >>> _separate_words('__hello_world')
    '__hello_world'
    >>> _separate_words('hello_world_')
    'hello_world_'
    >>> _separate_words('hello_world__')
    'hello_world__'
    >>> _separate_words('whatever_hi')
    'whatever_hi'
    >>> _separate_words('whatever_10')
    'whatever_10'
    >>> _separate_words('sizeX')
    'size_X'
    >>> _separate_words('aB')
    'a_B'
    >>> _separate_words('testNTest')
    'test_N_Test'
    '''
    return separator.join(s for s in SPLIT_RE.split(string) if s)
