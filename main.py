import re


priority = {
    '*': 1,
    '/': 1,
    '+': 2,
    '-': 2,
}


def create_token(value: str) -> tuple:
        import re
        if re.match(r'^\d+$', value):
            return 'number', int(value)
        elif re.match(r'^\d+\.\d+?$', value):
            return 'number', float(value)
        elif re.match(r'^[\(\)]$', value):
            return 'bracket', value

        return 'operator', value


def parse_expression(expression: str) -> list[tuple]:
    return [create_token(item) for item in re.split(r'(\s+|[(\)\+\-\*/])', expression) if item.strip()]


def get_rpn(tokens: list[tuple]) -> list[tuple]:
    rpn = []
    operators = []
    
    for token in tokens:
        token_type, value = token
        if token_type == 'number':
            rpn.append(token)
        elif token_type == 'bracket':
            if value == '(':
                operators.append(token)
            else:
                while operators and operators[-1][1] != '(':
                    rpn.append(operators.pop())
                operators.pop()
        elif token_type == 'operator':
            if not operators:
                operators.append(token)
            else:
                operator_priority = priority[value]
                while operators and operators[-1][0] == 'operator' and operator_priority > priority[operators[-1][1]]:
                    rpn.append(operators.pop())
                operators.append(token)

    while operators:
        rpn.append(operators.pop())

    return rpn


def evaluate(tokens: list[tuple]) -> int | float:
    stack: list[int | float] = []
    for token_type, value in rpn:
        if token_type == 'number':
            stack.append(value)
        elif token_type == 'operator':
            right = stack.pop()
            left = stack.pop()

            if value == '+':
                stack.append(left + right)
            elif value == '-':
                stack.append(left - right)
            elif value == '*':
                stack.append(left * right)
            elif value == '/':
                stack.append(left / right)

    return stack.pop()


if __name__ == '__main__':
    expression = '(3.14159 * 2)'
    tokens = parse_expression(expression)
    rpn = get_rpn(tokens)
    print(evaluate(rpn))
