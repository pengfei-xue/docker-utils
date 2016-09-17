import os


def clear():
    if os.name == 'posix':
        os.system('clear')

    elif os.name in ('ce', 'nt', 'dos'):
        os.system('cls')


def unit(i):
    # convert byte to K, M, G
    G = 1024 ** 3
    M = 1024 ** 2
    K = 1024

    if i // G > 0:
        return '%.2f G' % (i / G)

    elif i // M > 0:
        return '%.2f M' % (i / M)

    elif i // K > 0:
        return '%.2f K' % (i / K)

    else:
        return '%s B' % i
