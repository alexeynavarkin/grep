
import argparse
import sys
import re


def output(line):
    print(line)


def output_line(line, line_number=False, non_match=False):
    """
    Adds to line proper leading symbols if needed

    Keyword arguments:
        line(str):        line to output
        line_number(int): should be line numbered
        non_match(bool):  if current line satisfy pattern (":" or "-" will be added)
    Returns:
    """
    if line_number and non_match:
        output(str(line_number) + '-' + line)
    elif line_number:
        output(str(line_number) + ':' + line)
    else:
        output(line)


def count(lines, regexp, invert=False):
    """
    Count lines matches regexp.

    Args:
        lines(list):          lines to process
        regexp(SRE_Pattern):  regexp to check
        invert(bool):         invert regexp match
    Returns:
        Number of lines matching regexp
    """
    counter = 0
    for line in lines:
        if bool(regexp.search(line)) != invert:
            counter += 1
    return counter


def out_match(lines, regexp, invert=False, line_number=False):
    """
    Outputs lines matching regexp

    Args:
        lines(list):         lines to process
        regexp(SRE_Pattern): regexp to check
        invert(bool):        invert regexp match
        line_number(bool):   number lines
    Returns:
    """
    for idx, line in enumerate(lines):
        if bool(regexp.search(line)) != invert:
            output_line(line, idx+1 if line_number else False)


def out_match_context(lines, regexp, before, after,
                      invert=False, line_number=False):
    """
    Outputs lines matching regexp with context __after__ and __before__

    Args:
        lines(list):        lines to process
        regexp(SRE_Pattern):regexp to check
        before(int):        context before
        after(int):         context after
        invert(int):        invert regexp match
        line_number(bool):  number lines
    Returns
    """
    left = False
    right = False
    matches_idx = []
    for idx in range(len(lines)):
        lines[idx] = lines[idx].rstrip()
        if bool(regexp.search(lines[idx])) != invert:
            matches_idx.append(idx)
            cur_left = idx - before
            if cur_left < 0: cur_left = 0
            cur_right = idx + after
            if cur_right > len(lines) - 1: cur_right = len(lines) - 1
            if left is right:
                left = cur_left
                right = cur_right
            elif cur_left <= right:
                right = cur_right
            else:
                for i in range(left, right+1):
                    output_line(lines[i], i+1 if line_number else False, i not in matches_idx)
                    matches_idx.clear()
                    left = cur_left
                    right = cur_right
    if left is not right:
        for i in range(left, right+1):
            output_line(lines[i], i+1 if line_number else False, i not in matches_idx)


def grep(lines, params):
    regexp = params.pattern.replace('?', '.').replace('*', '.*')
    regexp = re.compile(regexp, re.I if params.ignore_case else 0)
    if params.count:
        result = count(lines, regexp, params.invert)
        output(str(result))

    elif params.context or params.after_context or params.before_context:
        before = params.context if params.context >= params.before_context else params.before_context
        after = params.context if params.context >= params.after_context else params.after_context
        out_match_context(lines, regexp, before, after,
                          params.invert, params.line_number)

    else:
        out_match(lines, regexp, params.invert, params.line_number)


def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v',
        action="store_true",
        dest="invert",
        default=False,
        help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i',
        action="store_true",
        dest="ignore_case",
        default=False,
        help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()
