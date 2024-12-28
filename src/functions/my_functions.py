import os
import subprocess
from datetime import datetime

from functions.db import MyDataBase


def bechmark_action(**kwargs):

    db = MyDataBase()
    destino = 'data'
    valores = dict()

    check_dir(destino)
    file = destino + '/' + kwargs['servidor']

    valores['tiempo'] = datetime.timestamp(datetime.now())

    with open(file+'.txt', 'w', encoding='utf-8') as output_file:
        subprocess.run(
            ['ab', '-n', str(kwargs['n']), '-c',
             str(kwargs['c']), '-e', file+'.csv', kwargs['endpoint']],
            stdout=output_file,
            stderr=subprocess.STDOUT,
            check=True
        )

    with open(file+'.txt', 'r', encoding='utf-8') as f:
        data = f.read().split('\n')

    with open(file+'.csv', 'r', encoding='utf-8') as f:
        traza = f.readlines()[1:]

    for i in data:
        if ':' in i:
            valores[i.split(":")[0].strip()] = i.split(":")[-1].strip()

    valores.update(kwargs)
    valores['traza'] = traza

    return db.add_register(valores)


def check_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    return 1


if __name__ == '__main__':
    print('fichero de funciones')
