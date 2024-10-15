def call_my_name(name):
    return f'Myname is {name}'

def repeat_my_name(name, times):
    lst = []
    for i in range(times):
        lst.append(f'my name is {name}')
    return lst