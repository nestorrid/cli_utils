
import typing as t


class TabChar:
    INDENT = '─'
    BRANCH_LEFT = '├'
    BRANCH_RIGHT = '┤'
    BRANCH_TOP = '┬'
    BRANCH_BOTTOM = '┴'
    CROSS = '┼'
    PIPE = '│'
    CORNER_TOP_LEFT = '┌'
    CORNER_TOP_LEFT_ROUND = '╭'
    CORNER_BOTTOM_LEFT = '└'
    CORNER_BOTTOM_LEFT_ROUND = '╰'
    CORNER_BOTTOM_RIGHT = '┘'
    CORNER_BOTTOM_RIGHT_ROUND = '╯'
    CORNER_TOP_RIGHT = '┐'
    CORNER_TOP_RIGHT_ROUND = '╮'
    SPACE = ' '


class DoubleLineTabChar(TabChar):
    INDENT = '═'
    BRANCH_LEFT = '╠'
    BRANCH_RIGHT = '╣'
    BRANCH_TOP = '╦'
    BRANCH_BOTTOM = '╩'
    CROSS = '╬'
    PIPE = '║'
    CORNER_TOP_LEFT = '╔'
    CORNER_BOTTOM_LEFT = '╚'
    CORNER_BOTTOM_RIGHT = '╝'
    CORNER_TOP_RIGHT = '╗'


def print_length(text: str) -> int:
    """
    Count print length of a string.

    Cause Chinese characters is wide then ascii letters, but function `len()` will return 1 for both kind of characters.

    So `中文` will have the same width with `word` but less length.

    This func will count each Chinese character for `2` and others for `1`.

    :param str text: Any string.
    :return int: Real length of the string in Terminal environment with mono space font.
    """

    count = 0
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            count += 2
        else:
            count += 1

    return count


def str_to_lines(text: str, line_width: int) -> t.Iterable[str]:
    """
    将长字符串根据最大单行长度切割为字符串数组.

    目标字符串中的中文字符将被视为两个字符. 比如:

        .. code-block:: python
            str_width_limit('目标文字text', 4)
            # ('目标', '文字', 'text')

    :param str text: 目标字符串
    :param int line_width: 每行文字的最大长度, 应为偶数 
    :return t.Iterable[str]: 分割后的字符串数组
    """

    length = print_length(text)
    if length < line_width:
        return [text]

    result = []

    while print_length(text) > 0:
        temp = text[:line_width]
        while print_length(temp) > line_width:
            temp = temp[:-1]
        text = text[len(temp):]

        if is_last_word_break(temp, text):
            sep = temp.rsplit(' ', 1)
            temp = sep[0]
            text = sep[1] + text

        result.append(temp)

    return result


def is_last_word_break(line: str, new_line: str) -> bool:
    """
    判断行尾的单词是否被分割入两行, 例如:

        'some wo', 'rd is break'

    `word` 应为一个完整的单词, 但是被分割入了两行. 

    :param str line: 第一行文本
    :param str new_line: 第二行文本

    :return bool: 如果第一行文本末尾包含被分割入两行的单词, 返回 True
    """

    if len(new_line) == 0:
        return False

    if line[-1].isalpha() and new_line[0].isalpha() and ' ' in line:
        return True
