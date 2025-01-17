import sqlite3


class Consulta:
    def __init__(self, id, server, fecha, url, solicitudes, concurrency):
        self.id = id
        self.server = server
        self.fecha = fecha
        self.url = url
        self.solicitudes = solicitudes
        self.concurrency = concurrency


class DatosConsulta:
    def __init__(self, id, software, length, concurrency, time_for_tests, complete_request, failed_request, request_per_second, time_per_request, connect_min, connect_max, connect_medium, processing_min, processing_max, processing_medium, waiting_min, waiting_max, waiting_medium, id_consulta):
        self.id = id
        self.software = software
        self.length = length
        self.concurrency = concurrency
        self.time_for_tests = time_for_tests
        self.complete_request = complete_request
        self.failed_request = failed_request
        self.request_per_second = request_per_second
        self.time_per_request = time_per_request
        self.connect_min = connect_min
        self.connect_max = connect_max
        self.connect_medium = connect_medium
        self.processing_min = processing_min
        self.processing_max = processing_max
        self.processing_medium = processing_medium
        self.waiting_min = waiting_min
        self.waiting_max = waiting_max
        self.waiting_medium = waiting_medium
        self.id_consulta = id_consulta


class Comportamiento:
    def __init__(self, id, porcentaje, tiempo_real, id_consulta):
        self.id = id
        self.porcentaje = porcentaje
        self.tiempo_real = tiempo_real
        self.id_consulta = id_consulta


class Singlenton(type):

    __instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls.__instances:
            instance = super().__call__(*args, **kwargs)
            cls.__instances[cls] = instance

        return cls.__instances[cls]


class MyDataBase(metaclass=Singlenton):

    def __init__(self):

        try:
            with sqlite3.connect('registros.db') as conn:
                cursor = conn.cursor()

                tablas = [
                    '''create table if not exists consultas(
                 id integer primary key,
                 server string not null,
                 fecha datetime not null,
                 url string not null   ,
                 solicitudes integer not null,
                 concurrency integer not null
                );
                ''',
                    '''create table if not exists datos_consulta(
                  id integer primary key,
                  software string not null,
                  length integer not null,
                  concurrency integer not null,
                  time_for_tests real not null,
                  complete_request integer not null,
                  failed_request integer not null,
                  request_per_second real not null,
                  time_per_request real not null,
                  connect_min integer not null,
                  connect_max integer not null,
                  connect_medium integer not null,
                  processing_min integer not null,
                  processing_max integer not null,
                  processing_medium integer not null,
                  waiting_min integer not null,
                  waiting_max integer not null,
                  waiting_medium integer not null,
                  id_consulta integer not null,
                  FOREIGN KEY(id_consulta) REFERENCES consultas(id)
                );
                ''',
                    '''
                create table if not exists comportamiento(
                    id integer primary key,
                    porcentaje integer not null,
                    tiempo_real not null,
                    id_consulta integer not null,
                    FOREIGN KEY(id_consulta) REFERENCES consultas(id)
                    );
                '''
                ]

                for i in tablas:
                    cursor.execute(i)
                conn.commit()
                pass
        except Exception as e:
            print(e)

    def add_register(self, kwargs):

        try:
            with sqlite3.connect('registros.db') as conn:
                cursor = conn.cursor()

                cursor.execute(
                    'insert into consultas (server, fecha, url, solicitudes, concurrency) values(?,?,?,?,?)',
                    (kwargs['servidor'],
                     kwargs['tiempo'],
                     kwargs['endpoint'],
                     kwargs['n'],
                     kwargs['c']
                     )
                )

                id = cursor.lastrowid

                cursor.execute(
                    'insert into datos_consulta (software,length,concurrency,time_for_tests,complete_request,failed_request,request_per_second,time_per_request,connect_min,connect_max,connect_medium,processing_min, processing_max, processing_medium, waiting_min, waiting_max, waiting_medium, id_consulta) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    (kwargs.get('servidor'),
                     kwargs.get('Document Length').split(' ')[0],
                     kwargs.get('Concurrency Level'),
                     kwargs.get('Time taken for tests').split(' ')[0],
                     kwargs.get('Complete requests'),
                     kwargs.get('Failed requests'),
                     kwargs.get('Requests per second').split(' ')[0],
                     kwargs.get('Time per request').split(' ')[0],
                     [i for i in kwargs.get('Connect').split(
                         ' ') if i != ''][0],
                     [i for i in kwargs.get('Connect').split(
                         ' ') if i != ''][4],
                     [i for i in kwargs.get('Connect').split(
                         ' ') if i != ''][1],
                     [i for i in kwargs.get('Processing').split(
                         ' ') if i != ''][0],
                     [i for i in kwargs.get('Processing').split(
                         ' ') if i != ''][4],
                     [i for i in kwargs.get('Processing').split(
                         ' ') if i != ''][1],
                     [i for i in kwargs.get('Waiting').split(
                         ' ') if i != ''][0],
                     [i for i in kwargs.get('Waiting').split(
                         ' ') if i != ''][4],
                     [i for i in kwargs.get('Waiting').split(
                         ' ') if i != ''][1],
                     id
                     )
                )

                traza = [(i.split('\n')[0].split(',')[0], i.split('\n')[
                          0].split(',')[1], id) for i in kwargs.get('traza')]

                cursor.executemany(
                    'insert into comportamiento (porcentaje, tiempo_real, id_consulta) values(?,?,?)', traza)

                conn.commit()
                cursor.close()

            code = "success"
            msg = "Datos guardados satisfactoriamente"
            data = {
                "consulta": self.get_consulta(id),
                "detalles": self.get_data_consulta(id),
                'comportamiento': self.get_comportamiento_consulta(id)
            }

            return {"code": code, "msg": msg, "data": data}

        except Exception as e:
            print('Error insertando datos del bechmark: ', e)
            code = "error"
            msg = "No se guardaron los registros"
            return {"code": code, "msg": msg}

    def get_consultas(self):
        with sqlite3.connect('registros.db') as conn:
            cursor = conn.cursor()
            cursor.execute('select * from consultas')
            rows = cursor.fetchall()
            cursor.close()

            consultas = [Consulta(*row) for row in rows]

            return [
                {
                    'id': consulta.id,
                    'server': consulta.server,
                }
                for consulta in consultas
            ]

    def get_consulta(self, id):

        with sqlite3.connect('registros.db') as conn:
            cursor = conn.cursor()
            cursor.execute('select * from consultas where id = ? ', (id,))
            rows = cursor.fetchall()
            cursor.close()

            consultas = [Consulta(*row) for row in rows]

            return [
                {
                    'id': consulta.id,
                    'server': consulta.server,
                    'fecha': consulta.fecha,
                    'url': consulta.url,
                    'solicitudes': consulta.solicitudes,
                    'concurrency': consulta.concurrency
                }
                for consulta in consultas
            ]

    def get_data_consulta(self, id):

        with sqlite3.connect('registros.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'select * from datos_consulta where id_consulta = ? ', [id])
            rows = cursor.fetchall()
            cursor.close()

            detalles = [DatosConsulta(*row) for row in rows]

            return [
                {
                    'id': detalle.id,
                    'software': detalle.software,
                    'length': detalle.length,
                    'concurrency': detalle.concurrency,
                    'time_for_tests': detalle.time_for_tests,
                    'complete_request': detalle.complete_request,
                    'failed_request': detalle.failed_request,
                    'request_per_second': detalle.request_per_second,
                    'time_per_request': detalle.time_per_request,
                    'connect_min': detalle.connect_min,
                    'connect_max': detalle.connect_max,
                    'connect_medium': detalle.connect_medium,
                    'processing_min': detalle.processing_min,
                    'processing_max': detalle.processing_max,
                    'processing_medium': detalle.processing_medium,
                    'waiting_min': detalle.waiting_min,
                    'waiting_max': detalle.waiting_max,
                    'waiting_medium': detalle.waiting_medium,
                    'id_consulta': detalle.id_consulta
                } for detalle in detalles
            ]

    def get_comportamiento_consulta(self, id):

        with sqlite3.connect('registros.db') as conn:

            cursor = conn.cursor()
            cursor.execute(
                'select * from comportamiento where id_consulta = ? ', [id])
            rows = cursor.fetchall()
            cursor.close()

            comportamientos = [Comportamiento(*row) for row in rows]

            return [
                {
                    'id': comportamiento.id,
                    'porcentaje': comportamiento.porcentaje,
                    'tiempo_real': comportamiento.tiempo_real,
                    'id_consulta': comportamiento.id_consulta,
                } for comportamiento in comportamientos]

    def get_general(self):
        with sqlite3.connect('registros.db') as conn:
            cursor = conn.cursor()
            cursor.execute('select * from datos_consulta')
            rows = cursor.fetchall()

            consultas = [DatosConsulta(*row) for row in rows]

            return [{
                "id": consulta.id,
                "software": consulta.software,
                "length": consulta.length,
                "concurrency": consulta.concurrency,
                "time_for_tests": consulta.time_for_tests,
                "complete_request": consulta.complete_request,
                "failed_request": consulta.failed_request,
                "request_per_second": consulta.request_per_second,
                "time_per_request": consulta.time_per_request,
                "connect_min": consulta.connect_min,
                "connect_max": consulta.connect_max,
                "connect_medium": consulta.connect_medium,
                "processing_min": consulta.processing_min,
                "processing_max": consulta.processing_max,
                "processing_medium": consulta.processing_medium,
                "waiting_min": consulta.waiting_min,
                "waiting_max": consulta.waiting_max,
                "waiting_medium": consulta.waiting_medium,
                "id_consulta": consulta.id_consulta
            } for consulta in consultas]
