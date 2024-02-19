
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


class QRCode:
    dot = "██"
    space = "  "
