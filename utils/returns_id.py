def retorna_id(string):
    print(string)
    var_str = ((string.split(','))[0].split(' '))[1]
    return int(var_str)
