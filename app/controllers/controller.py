"""
 - Fichero: controller.py
 - Descripción: Controlador de la aplicación
 - Autor: Alejandro Ruiz Becerra
"""
from model.data.record import Record
from model.repository.record_repo import RecordRepository
from model.services.record_creator import RecordCreator
from model.services.record_getter import RecordGetter
from model.services.record_updater import RecordUpdater
from model.services.record_deleter import RecordDeleter
from views.view import MainWindow
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
import csv


class Controller():
    """
    Controlador principal de la aplicación. Se encarga del flujo principal y de gestionar 
    la comunicación entre el modelo (backend) y la interfaz gráfica de usuario (frontend).
    """

    def __init__(self):
        """
        Inicializador
        """
        # Modelo
        self.repo = RecordRepository('v2.db')

        # Inicializar la interfaz gráfica de Tkinter
        self.view = MainWindow()

        # Configurar la interfaz gráfica
        self._config_view()


    def _config_view(self):
        """
        Configura la interfaz gráfica
        """
        # Configurar método de salida
        self.view.protocol("WM_DELETE_WINDOW", self.view.exit)

        # Configurar el menú
        self.view.menu.add_command(label="Import from CSV", command=self.read_csv)
        self.view.menu.add_command(label="Export to CSV", command=self.write_csv)
        self.view.config(menu=self.view.menu)

        # Configurar botones
        self.view.set_add_button_handler(self.insert)
        self.view.set_update_button_handler(self.update)
        self.view.set_remove_button_handler(self.remove)
        self.view.set_remove_all_button_handler(self.remove_all)

        # Enviar los datos a la interfaz gráfica
        for row in self.get_all():
            # Encapsular datos
            record = Record(row[0], row[1], row[2])
            self.view.add_record(record.__dict__)


    def run(self):
        """
        Lanza la aplicación.
        """
        self.view.mainloop()


    def is_valid_record(self, record : Record) -> bool:
        """
        Comprueba si el registro contiene valores válidos

        Retorna False si:
            - el nombre es vacío o None
            - el nombre contiene números
            - el nombre tiene menos de 3 caracteres
            - el número es vacío o None
            - el número contiene letras
            - el número no contiene exactamente 9 dígitos
        """
        # Si el input_name está vacío
        if len(record.name) == 0:
            self.print("Debe introducir un nombre")
            return False

        # Si el input_name contiene números. Eliminamos espacios con split y join.
        if not "".join(record.name.split()).isalpha():
            self.print("El nombre debe estar compuesto por los caracteres [a-z, A-Z] y espacios")
            return False

        # Si el input_name tiene menos de 3 caracteres
        if len(record.name) < 3:
            self.print("El nombre debe contener al menos 3 caracteres")
            return False

        # Si el input_number está vacío
        if len(record.number) == 0:
            self.print("Debe introducir un número de teléfono móvil (6xx xxx xxx)")
            return False

        # Si el input_number no es convertible a número
        if not record.number.isnumeric():
            self.print("El número debe estar compuesto solamente por dígitos")
            return False

        # Si el input_number no tiene 9 dígitos
        if len(record.number) != 9:
            self.print("El número debe contener exactamente 9 dígitos")
            return False

        return True 


    def insert(self, record : Record = None) -> None:
        """
        Lee los datos introducidos por el usuario desde la interfaz gráfica y los inserta
        en la base de datos, retornando el nuevo registro como resultado de la operación.

        Esté método se ejecuta cuando cuando el usuario pincha sobre el botón Insert de la
        interfaz gráfica.
        """
        # Si no se dan los datos como parámetro, los recojo de la vista
        if not record:
            # Recuperar datos del front
            name = self.view.name_input.get()
            number  = self.view.number_input.get()
            
            # Encapsular datos
            record = Record(name=name, number=number)

        # Comprobar datos y salir si no son válidos
        if not self.is_valid_record(record):
            return

        # Crear servicio
        service = RecordCreator(self.repo)

        # Lanzar servicio y recuperar ID
        id = service.insert_record(record)

        # Si se ha insertado correctamente en la base de datos (id > 0), actualizar vista,
        # mandando el registro creado como un diccionario (JSON-RESTful API).
        if id > 0:
            record.id = id
            self.view.add_record(record.__dict__)
            # self.print ("Nuevo regsitro insertado: ", record)
        else:
            self.print ("La inserción falló")

    
    def get_all(self) -> list:
        """
        Recupera y retorna todos los registros de la base de datos
        """
        # Crear el servicio.
        service = RecordGetter(self.repo)

        # Lanzar acción.
        results = service.get_records()

        return results


    def update(self) -> None:
        """
        Actualiza el registro seleccionado en la base de datos y actualiza la interfaz 
        gráfica.
        """
        # Recuperar datos del front
        id = self.view.id_input.get()
        name = self.view.name_input.get()
        number = self.view.number_input.get()

        # Encapsular datos
        record = Record(id, name, number)

        # Comprobar datos y salir si no son válidos
        if not self.is_valid_record(record):
            return

         # Comprobar datos y salir si no son válidos
        if not id:
            self.print("No se ha seleccionado nada")
            return

        # Crear servicio
        service = RecordUpdater(self.repo)

        # Lanzar acción. Actualizar
        success = service.update_record(record)

        # Actualizar front
        self.view.update_record()
        self.print ("Registro actualizado: ", record)


    def remove(self) -> None:
        """
        Elimina el registro seleccionado. Actualiza la interfaz.
        """
        # recuperar datos del front
        id = self.view.id_input.get()
        name = self.view.name_input.get()
        number = self.view.number_input.get()

        if not id.isnumeric():
            self.print("No se ha seleccionado nada")
            return

        # Encapsular datos
        record = Record(id, name, number)
        
        # Crear servicio
        service = RecordDeleter(self.repo)

        # Lanzar acción. Eliminar
        success = service.delete_record(record)

        # Actualizar front
        self.view.remove_one()
        
        self.print("Registro eliminado: ", record)


    def remove_all(self) -> None:
        """
        Elimina todos los registros de la base de datos. Actualiza la interfaz gráfica.
        """
        # Recupear datos desde la base de datos
        rows = self.get_all()

        # Crear servicio
        service = RecordDeleter(self.repo)

        # Lanzar acción para cada fila. Eliminar
        for id, name, number in rows:
            record = Record(id, name, number)
            service.delete_record(record)

        # Actualizar front
        self.view.remove_all()

        self.print("Todos los registros han sido eliminados")


    def read_csv(self) -> None:
        """
        Abre y lee un fichero CSV. Pide al usuario que seleccione un fichero CSV para leer.
        Se pasan los datos a la interfaz gráfica.
        """
        filename = askopenfilename(filetypes=[('CSV', '.csv')])

        if not filename:
            return

        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Recuperar columnas
                try:
                    name = row['NOMBRE']
                    number = row['TELEFONO']
                except KeyError:
                    # Error en las cabeceras
                    msg = "Las cabeceras del fichero CSV deben ser NOMBRE, TELEFONO"
                    showinfo(title="Formato no válido", message=msg)
                    return

                # Encapsular datos
                record = Record(name=name, number=number)

                # Insertar en la base de datos y en la vista
                self.insert(record)


    def write_csv(self) -> None:
        """
        Escribe los registros de la base de datos en un fichero.
        """
        # Archivo de salida
        filename = 'output.csv'
        # 
        fieldnames = ['id', 'name', 'number']

        # Crear / abrir archivo
        try:
            csvfile = open(filename, 'x')
        except FileExistsError:
            csvfile = open(filename, 'w')
        
        # Recuperar datos
        records = self.get_all()

        writer = csv.DictWriter(csvfile, fieldnames)
        # Escribir cabeceras
        writer.writeheader()

        # Guardar datos
        for row in records:
            record = Record(row[0], row[1], row[2])
            writer.writerow(record.__dict__)
        
        # Cerrar archivo
        csvfile.close()

        # Mostrar ventana de confirmación
        showinfo(title="Operación completada", message="Los datos se han exportado correctamente")

    
    def print(self, text : str, args = ""):
        msg = text + str(args)
        showinfo(message=msg)
    

if __name__ == '__main__':
    m = Controller()
    m.run()
