def parse_expression(expression):
    items = []
    actions = ['+', '−', '×', '÷', '^']
    str_value = ''
    for char in expression:
        if char in actions:
            if str_value != '':
                items.append(str_value)
                str_value = ''
            items.append(char)
        elif char == '!' or char == '%':
            if str_value != '':
                items.append(str_value)
                str_value = ''
            items.append(char)
        elif char == '(':
            if str_value != '':
                items.append(str_value)
                str_value = ''
            items.append(char)
        elif char == ')':
            if str_value != '':
                items.append(str_value)
                str_value = ''
            items.append(char)
        elif char == '√':
            items += char
        else:
            str_value += char
    if str_value != '':
        items.append(str_value)
    if items[0] == '':
        items.pop(0)
    return items
