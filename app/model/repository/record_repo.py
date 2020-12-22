from ..data.record import Record
import sqlite3, os

class RecordRepository:
    

    def __init__(self, db: str) -> None:
        """
        Inicializa el objeto.

        Parámetros:
            - db (string): nombre de la base de datos.
        """
        self.db = db

        # Crear la tabla Agenda
        self.__connect()
        self.__create_table()
        self.__close()


    def __connect(self) -> None:
        """
        Conecta a la base de datos y crea la tabla AGENDA si no existe.
        """
        self.conn = sqlite3.connect(self.db)


    def __create_table(self) -> None:
        """
        Crea la tabla Agenda.
        """
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../sql/create_table_agenda.sql')

        with open(filename) as sql_file:
            query = sql_file.read()
            self.conn.cursor().execute(query)


    def __close(self) -> None:
        """
        Cierra la conexión con la base de datos.
        """
        self.conn.commit()
        self.conn.close()


    def __execute(self, query: str) -> list:
        """
        Ejecuta la consulta 'query'

        Parámetros:
            - query (str): consulta a ejecutar
        Retorna:
            - Una lista con los resultados de la consulta. Esta lista puede estar vacía.
            - None si se ha producido un error.
        """
        # Conectar a la base de datos
        self.__connect()

        # Ejecutar consulta
        try:
            results = self.conn.cursor().execute(query).fetchall()
        except sqlite3.IntegrityError as e:
            print(e)
            results = [None]

        # Recuperar último ID
        query = "SELECT last_insert_rowid()"
        self.last_id = self.conn.cursor().execute(query).fetchone()[0]

        # Cerrar la conexión
        self.__close()

        # for row in results:
        #     print(row)

        return results


    #############################################
    #
    # Métodos CRUD (Create, Read, Update, Delete)
    #
    #############################################

    def insert(self, record : Record) -> int:
        """
        Actualiza el nombre de la tupla (nombre, telefono) que cumpla la condición
        telefono=number.
        
        Parámetros:
            - record (Record): registro a insertar

        Retorna:
            - ID del nuevo registro insertado (empieza en 1, 0 no hay datos).
        """
        # Insertar valores
        query = f"INSERT INTO Agenda VALUES ('{record.name}', '{record.number}')"
        self.__execute(query)

        # Devolver ID del registro insertado
        return self.last_id


    def get_all(self) -> list:
        """
        Devuelve todos las tuplas (nombre, telefono) de la tabla 'Agenda'.
        
        Retorna:
            - Una lista con los resultados de la consulta.
        """
        query = "SELECT rowid, nombre, telefono FROM agenda"
        return self.__execute(query)


    def update(self, record : Record) -> bool:
        """
        Actualiza el nombre de la tupla (nombre, telefono) que cumpla la condición
        telefono=number.
        
        Parámetros:
            - name (str): nuevo nombre.
            - number (int): clave de la tupla a actualizar.

        Retorna:
            - True si la consulta se ha ejecutado correctamente, False en otro caso.
        """   
        # Consulta 
        query = f"UPDATE Agenda SET nombre='{record.name}', telefono={record.number} WHERE rowid={record.id}"
        # Lanzar consulta y guardar resultados
        success = self.__execute(query)
        # Devolver True si la lista es vacía (no ha habido errores)
        return len(success) == 0


    def delete(self, record: Record) -> bool:
        """
        Elimina las tuplas (nombre, telefono) que cumpla la condición telefono=number
        
        Parámetros:
            - record (record): registro a eliminar.

        Retorna:
            - True si la consulta se ha ejecutado correctamente, False en otro caso.
        """
        # Eliminar valores
        query = f"DELETE FROM Agenda WHERE rowid='{record.id}'"
        # Lanzar consulta y guardar resultados
        success = self.__execute(query)
        # Devolver True si la lista es vacía (no ha habido errores)
        return len(success) == 0
