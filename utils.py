"""Utilities modules to store other functions and classes."""
from ipaddress import ip_address, IPv4Address, IPv6Address


class TextFormatter:
    """Text formatter module used to format text."""

    @staticmethod
    def format(text, color):
        """Format text.
        *text*, a ``str`` text to be formated.
        *color*, a ``str` color value. The available text formats:
            - red, blue, green, yellow, purple, cyan, darkcyan
            - bold, underline
        """
        colors = [
            {'purple': '\033[95m'},
            {'cyan': '\033[96m'},
            {'darkcyan': '\033[36m'},
            {'blue': '\033[94m'},
            {'green': '\033[92m'},
            {'yellow': '\033[93m'},
            {'red': '\033[91m'},
            {'bold': '\033[1m'},
            {'underline': '\033[4m'},
            {'end': '\033[0m'}
            ]
        for color_dict in colors:
            if color_dict.get(color):
                return f"{color_dict[color]}{text}{colors[-1]['end']}"
        return text


class Validator:
    """Validator class used to validate data input"""

    @staticmethod
    def validate(data, datatype, **kwargs):
        """Validate data"""
        try:
            match datatype:
                case 'number':
                    is_number(number=data, num_type=datatype)
                case 'integer':
                    is_number(number=data, num_type=datatype)
                case 'positive_integer':
                    is_number(number=data, num_type=datatype)
                case 'negative_integer':
                    is_number(number=data, num_type=datatype)
                case 'float':
                    is_number(number=data, num_type=datatype)
                # case 'int':
                #     is_positive_int(data)
                case 'ip':
                    is_ip_addr(ip_addr=data)
                case 'ipv4':
                    is_ip_addr(ip_addr=data, addr_type=datatype)
                case 'ipv6':
                    is_ip_addr(ip_addr=data, addr_type=datatype)
                case 'input':
                    is_valid_value(data, kwargs['valid_values'])
                case _:
                    raise ValueError(f"Invalid data type '{datatype}'")
            return data
        except ValueError as err:
            raise ValueError(err) from err


def is_ip_addr(ip_addr: str, addr_type: str='ip') -> bool:
    """Validate IPv4 address

    :param ip_addr: a `str` value represents an IPv4 address
    :param addr_type: IPv4, IPv6, or IP (default)
    :return: a `True` bool value if it is a valid IPv4/IPv6 address
    :rtype: `bool`
    :raise ValueError: if it is not a valid IPv4/IPv6 address
    """
    try:
        match addr_type.lower():
            case 'ipv4':
                addr_type = 'IPv4'
                if isinstance(ip_address(ip_addr), IPv4Address):
                    return True
            case 'ipv6':
                addr_type = 'IPv6'
                if isinstance(ip_address(ip_addr), IPv6Address):
                    return True
            case 'ip':
                addr_type = 'IPv4/IPv6'
                if isinstance(ip_address(ip_addr), (IPv4Address, IPv6Address)):
                    return True
    except ValueError:
        pass  # To raise custom ValueError
    raise ValueError(f"'{ip_addr}' does not appear to be a valid {addr_type} address.")

def is_ipv4(ip_addr: str) -> bool:
    """Validate IPv4 address

    :param ip_addr: a `str` value represents an IPv4 address
    :return: a `True` bool value if it is a valid IPv4 address
    :rtype: `bool`
    :raise ValueError: if it is not a valid IPv4 address
    """
    try:
        if isinstance(ip_address(ip_addr), IPv4Address):
            return True
    except ValueError:
        pass  # To raise custom ValueError
    raise ValueError(f"'{ip_addr}' does not appear to be a valid IPv4 address.")

def is_ipv6(ip_addr: str) -> bool:
    """Validate IPv6 address

    :param ip_addr: a `str` value represents an IPv6 address
    :return: a `True` bool value if it is a valid IPv6 address
    :rtype: `bool`
    :raise ValueError: if it is not a valid IPv6 address
    """
    try:
        if isinstance(ip_address(ip_addr), IPv6Address):
            return True
    except ValueError:
        pass  # To raise custom ValueError
    raise ValueError(f"'{ip_addr}' does not appear to be a valid IPv6 address.")

def is_number(number: str, num_type: str='number'):
    """Validate a valid number
    :param number: a `str` represents an number value
    :param num_type: a `str` represents a number type. Default is `number`
        Possible values:
            number
            integer
            positive_integer
            negative_integer
            float
    :return: a `True` bool value if it is a valid number matched with the provied `num_type`
    :rtype: `bool`
    :raise ValueError: if it is not a valid number
    """
    try:
        match num_type:
            case 'integer':
                if isinstance(int(number), int):
                    return True
            case 'positive_integer':
                if int(number) and int(number) > 0:
                    return True
            case 'negative_integer':
                if int(number) and int(number) < 0:
                    return True
            case 'float':
                if isinstance(float(number), float):
                    return True
            case _:
                if isinstance(float(number), float):
                    return True
    except ValueError:
        pass
    raise ValueError(f"'{number}' is not a valid {num_type}.")

def is_positive_int(x: str) -> bool:
    """Validate positive integer

    :param x: a `str` represents an `integer` value
    :return: a `True` bool value if it is a positive integer
    :rtype: `bool`
    :raise ValueError: if it is not a valid positive integer
    """
    try:
        if int(x) and int(x) > 0:
            return True
    except ValueError:
        pass
    raise ValueError(f"'{x}' is not a valid positive integer.")

def is_valid_value(x: str, valid_values: list) -> bool:
    """Validate a value against a defined valid values

    :param x: a `str` value to be validated against a defined valid values
    :param valid_values: a `list` of valid values
    :raise ValueError: if a value is not valid
    :return: `True` bool value if the x value is valid
    """
    if x.strip() in valid_values:
        return True
    raise ValueError(
            f"The value '{x}' is not valid. "
            f'Valid values are {valid_values}.'
            )
