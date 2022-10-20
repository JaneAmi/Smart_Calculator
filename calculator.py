from collections import deque
import re


def user_command(u_command):
    if u_command == '/help':
        print('The program calculates the sum of numbers')
    else:
        print('Unknown command')


def variables_check(u_var, var_dict):
    if re.match('\\s*?[a-zA-Z]+\\s*=', u_var.strip()):  # check if it is the variable with the value
        new_var_name = re.findall('[a-zA-Z]+', u_var)[0]
        if re.match('\\s*?[a-zA-Z]+\\s*=\\s*\\d+$', u_var.strip()):  # for the variable with num value
            new_var_vol = re.findall('\\d+', u_var)[0]
            var_dict.update({new_var_name: new_var_vol})
        elif re.match('\\s*?[a-zA-Z]+\\s*=\\s*[a-zA-Z]+\\s*$', u_var.strip()):  # for the variable with another variable as value
            exist_var = re.findall('[a-zA-Z]+', u_var)[1]
            exist_var_vol = var_dict.get(exist_var)
            if exist_var_vol is None:
                print('Unknown variable')
            else:
                var_dict.update({new_var_name: exist_var_vol})
        else:
            print('Invalid assignment')
    elif re.match('\\s*?[a-zA-Z]+\\s*$', u_var):  # check if the variable exists
        exist_var = re.findall('[a-zA-Z]+', u_var)[0]
        exist_var_vol = var_dict.get(exist_var)
        if exist_var_vol is None:
            print('Unknown variable')
        else:
            print(exist_var_vol)
    else:
        print('Invalid identifier')
    return var_dict


def input_to_expr(u_expr, var_dict):
    new_var_d = {}
    for k in sorted(var_dict, key=len, reverse=True):  # sort the dict with variables by length in descending order
        new_var_d[k] = var_dict[k]
    for key in new_var_d:  # change var letters to numbers
        if new_var_d.get(key) is None:
            print('Unknown variable')
        else:
            new_val = new_var_d.get(key)
            u_expr = u_expr.replace(key, new_val)
    return u_expr


def postfix(expression):
    first_op, sec_op = r'\+$|-$', r'\*|\/'
    if len(re.findall(r'[a-zA-Z]', expression)) > 0:
        posts_exp = 'Invalid expression'
        print('Invalid expression')
        return posts_exp
    new_exp = re.findall(r'^-\d+|\d+|\++|-+|\*+|/+|\^+|\(|\)', expression)
    posts_exp, tmp_op, n_br = deque(), deque(), 0
    for i in new_exp:
        if re.match(r'\*\*+|//+|\^\^+', i):
            posts_exp = 'Invalid expression'
            print(posts_exp)
            break
        elif re.match(r'--+', i):
            new_op = '+' if len(i) % 2 == 0 else '-'
            if len(tmp_op) > 0:
                for o in range(len(tmp_op)):
                    last_op = tmp_op.pop()
                    posts_exp.append(last_op)
                    tmp_op.append(new_op)
            else:
                tmp_op.append(new_op)
        elif re.match(first_op, i):
            if len(tmp_op) > 0:
                for o in range(len(tmp_op)):
                    last_op = tmp_op.pop()
                    if last_op == '(':
                        tmp_op.append(last_op)
                        break
                    else:
                        posts_exp.append(last_op)
                tmp_op.append(i)
            else:
                tmp_op.append(i)
        elif re.match(r'-?\d+', i):
            posts_exp.append(i)
        elif re.match(sec_op, i):
            if len(tmp_op) > 0:
                last_op = tmp_op.pop()
                if re.match(first_op, last_op):
                    tmp_op.append(last_op)
                    tmp_op.append(i)
                elif re.match(sec_op, last_op) and re.match(sec_op, i):
                    posts_exp.append(last_op)
                    tmp_op.append(i)
            else:
                tmp_op.append(i)
        elif re.match(r'\)', i):
            n_br -= 1
            if n_br < 0:
                posts_exp = 'Invalid expression'
                print('Invalid expression')
                break
            else:
                last_op = tmp_op.pop()
                while last_op != '(':
                    posts_exp.append(last_op)
                    last_op = tmp_op.pop()
        elif re.match(r'\(', i):
            n_br += 1
            tmp_op.append(i)
        elif re.match(r'\^', i):
            tmp_op.append(i)
        else:
            posts_exp = 'Invalid expression'
            print(posts_exp)
            break
    if n_br != 0:  # check number of brackets
        posts_exp = 'Invalid expression'
        print(posts_exp)
    elif posts_exp != 'Invalid expression':
        for o in range(len(tmp_op)):
            posts_exp.append(tmp_op.pop())
    return posts_exp


def calc_count(pf_expr):  # make calculations
    num_stack = deque()
    while pf_expr:
        i = pf_expr.popleft()
        if re.match(r'-?\d+', i):
            num_stack.append(i)
        else:
            a, b = num_stack.pop(), num_stack.pop()
            if re.match(r'\+', i):
                num_stack.append(int(a)+int(b))
            elif re.match('-', i):
                num_stack.append(int(b)-int(a))
            elif re.match(r'\*', i):
                num_stack.append(int(a)*int(b))
            elif re.match(r'/', i):
                num_stack.append(int(b)/int(a))
            elif re.match(r'\^', i):
                num_stack.append(int(b) ** int(a))
    return num_stack.pop()


u_var_dict = {}
while True:
    user_input = input()
    if user_input == '/exit':
        print('Bye!')
        break
    elif user_input == '':
        continue
    elif re.match('/.*', user_input):
        user_command(user_input)
    elif re.match('\\s*?[a-zA-Z]+\\s*(=.*)?$', user_input.strip()):  # check is the variables are in the user expression
        u_var_dict = variables_check(user_input, u_var_dict)
    else:
        user_expression = input_to_expr(user_input, u_var_dict)  # add numbers instead of variables
        pf_user_exp = postfix(user_expression)  # make postfix
        if pf_user_exp != 'Invalid expression':
            print(calc_count(pf_user_exp))  # make calculations
