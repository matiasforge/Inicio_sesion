from app_flask.config.mysqlconnection import connectToMySQL
from app_flask import BASE_DATOS, EMAIL_REGEX
from flask import flash

class Usuario:
    def __init__(self, datos):
        self.id = datos['id']
        self.nombre = datos['nombre']
        self.apellido = datos['apellido']
        self.correo = datos['correo']
        self.password = datos['password']
        self.fecha_creacion = datos['fecha_creacion']
        self.fecha_actualizacion = datos['fecha_actualizacion']

    @classmethod
    def crear_uno(cls, datos):
        query = """
                INSERT INTO usuarios(nombre, apellido, correo, password)
                VALUES(%(nombre)s, %(apellido)s, %(correo)s, %(password)s);
                """
        return connectToMySQL(BASE_DATOS).query_db(query, datos)
    
    @classmethod
    def obtener_uno(cls, datos):
        query = """
                SELECT *
                FROM usuarios
                WHERE correo = %(correo)s;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, datos)
        if len(resultado) == 0:
            return None
        return cls(resultado[0])

    @staticmethod
    def valida_registro(datos):
        es_valido = True
        if len(datos['nombre']) < 2:
            flash('Por favor escribe tu nombre.', 'error_nombre')
            es_valido = False
        if len(datos['apellido']) < 2:
            flash('Por favor escribe tu apellido.', 'error_apellido')
            es_valido = False
        if not EMAIL_REGEX.match(datos['correo']):
            flash('Por favor escribe un correo válido.', 'error_correo')
            es_valido = False
        if len(datos['password']) < 8:
            flash('Tu contraseña debe de tener al menos 8 caracteres.', 'error_password')
            es_valido = False
        if datos['password'] != datos['password_confirmar']:
            flash('Tus contraseñas no son iguales.', 'error_password')
            es_valido = False
        return es_valido