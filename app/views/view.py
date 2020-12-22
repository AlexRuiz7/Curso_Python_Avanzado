"""
- Recursos:
    - https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course/blob/master/tree.py
    - https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview
    - https://tk-tutorial.readthedocs.io/en/latest/tree/tree.html
    - https://stackoverflow.com/questions/7300072/inheriting-from-frame-or-not-in-a-tkinter-application
    - https://stackoverflow.com/questions/14847243/how-can-i-insert-a-string-in-a-entry-widget-that-is-in-the-readonly-state
"""

from tkinter import *
from tkinter import ttk


class MainWindow(Tk):
    """
    Ventana principal de la interfaz gráfica de usuario de la aplicación.
    """

    def exit(self):
        """
        Sale del bucle principal (mainloop) y elimina todos los componentes (widgets) que
        cuelgan de la instancia (root).
        """
        self.quit()
        super().destroy()


    def __init__(self):
        """
        Inicializador
        """
        super().__init__()
        self._init_root()
        self._init_menu()
        self._init_style()
        self._init_table_frame()
        self._init_tree_scroll()
        self._init_treeview()
        self._init_input_frame()
        self._init_buttons_frame()
        self._init_click_binder()
        

    def _init_root(self) -> None:
        """
        Crea y configura la ventana principal del programa
        """
        self.title('Proyecto Final - TreeView')
        self.geometry("625x475")
        self.resizable(False, False)


    def _init_menu(self) -> None:
        """
        Crea el menu. Se configura en el controlador
        """
        self.menu = Menu(self)


    def _init_style(self) -> None:
        """
        Define el estilo (tema) del programa.

        https://tkdocs.com/tutorial/styles.html
        """
        # Definir un estilo
        style = ttk.Style()
        # Elegir un tema
        style.theme_use("default")
        # Configurar los colores del TreeView
        style.configure(
            "Treeview", 
            background="#D3D3D3",
            foreground="black", 
            rowheight=25, 
            fieldbackground="#D3D3D3"
        )
        # Cambiar el color del elemento seleccionado
        style.map('Treeview', background=[('selected', 'blue')])


    def _init_table_frame(self) -> None:
        """
        Crea el frame que contiene la tabla de datos
        """
        self.tree_frame = Frame(self)
        self.tree_frame.pack(pady=20)


    def _init_tree_scroll(self) -> None:
        """
        Crea el scroll del treeview
        """
        # Crear el Scrollbar
        self.tree_scroll = Scrollbar(self.tree_frame)
        # Empaquetar en el padre (frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)


    def _init_treeview(self) -> None:
        """
        Configura la tabla de datos
        """
        # Crear el tree view
        self.tree_view = ttk.Treeview(
            self.tree_frame, 
            yscrollcommand=self.tree_scroll.set, 
            selectmode="browse"
        )
        # Empaquetar en el padre (frame)
        self.tree_view.pack()
        # Configurar la acción del scrollbar
        self.tree_scroll.config(command=self.tree_view.yview)
        
        # Definir las columnas
        self.tree_view['columns'] = ('ID', 'Name', 'Number')

        # Dar formato a las columnas
        self.tree_view.column('#0', width=0, stretch=NO)
        self.tree_view.column('ID', width=140, anchor=CENTER)
        self.tree_view.column('Name', width=140, anchor=W)
        self.tree_view.column('Number', width=140, anchor=W)

        # Crear los encabezados de las columnas
        self.tree_view.heading('#0', text="", anchor=W)
        self.tree_view.heading('ID', text="ID", anchor=CENTER)
        self.tree_view.heading('Name', text="Name", anchor=W)
        self.tree_view.heading('Number', text="Number", anchor=W)

        # Crear etiquetas para las columnas alternas
        self.tree_view.tag_configure('oddrow', background="white")
        self.tree_view.tag_configure('evenrow', background="lightblue")


    def _init_input_frame(self) -> None:
        """
        Crea el frame para los Inputs
        """
        self.input_frame = Frame(self)
        self.input_frame.pack(pady=20)

        # Inicializar los componentes del Frame
        self._init_input_labels()
        self._init_inputs()


    def _init_input_labels(self) -> None:
        """
        Crea las etiquetas para los inputs
        """
        labels = ['ID', 'Name', 'Number']

        for i, item in enumerate(labels):
            label = Label(self.input_frame, text=item)
            label.grid(row=0, column=i)
    

    def _init_inputs(self) -> None:
        """
        Crea los inputs
        """
        self.id_input = Entry(self.input_frame)
        self.id_input.grid(row=1, column=0)
        # El ID no se puede modificar (es clave primaria)
        self.id_input.configure(state='readonly')

        self.name_input = Entry(self.input_frame)
        self.name_input.grid(row=1, column=1)

        self.number_input = Entry(self.input_frame)
        self.number_input.grid(row=1, column=2)

    
    def _toggle_id_input(self) -> None:
        """
        Alterna el estado de la caja de texto que representa el ID entre los estados
        'readonly' y 'normal', de modo que se pueda modificar el texto solo cuando el
        programa lo requiera, y volver a modo readonly una vez se haya acabado para evitar
        que el usuario pueda modificar el valor del campo ID.
        """
        # Recuperar el estado actual del input
        state = self.id_input['state']

        # Calcular el nuevo estado
        state = 'readonly' if (state == 'normal') else 'normal'

        # Activar el nuevo estado
        self.id_input.configure(state=state)


    def _init_buttons_frame(self) -> None:
        """
        Crea el frame de los botones.
        """
        self.buttons_frame = Frame(self)
        self.buttons_frame.pack(pady=20)

        # Inicializar los componentes del frame (botones).
        self._init_buttons()


    def _init_buttons(self) -> None:
        """
        Crea los botones.
        """
        # Textos para los butones
        buttons = ['Add', 'Update', 'Remove', 'Remove all', 'Clear']

        # Nombres de los métodos, igual que los textos pero en minúscula y sin espacios
        iterable_buttons = [tag.replace(" ", "_").lower() for tag in buttons]

        # Creación dinámica de los botones
        for i, tag in enumerate(iterable_buttons):
            exec(f"self.{tag}_button = Button(self.buttons_frame, text=buttons[i], width=10)")
            exec(f"self.{tag}_button.grid(row=0, column=i, padx=5)")

        # Configurar el botón Clear
        self.clear_button.configure(command=self.clear)


    def set_add_button_handler(self, handler: callable = None) -> None:
        """
        Configura el funcionamiento del botón 'añadir'.
        """
        self.add_button.configure(command=handler)


    def set_update_button_handler(self, handler : callable = None) -> None:
        """
        Configura el funcionamiento del botón 'actualizar'.
        """
        self.update_button.configure(command=handler)


    def set_remove_button_handler(self, handler : callable = None) -> None:
        """
        Configura el funcionamiento del botón 'eliminar'.
        """
        self.remove_button.configure(command=handler)


    def set_remove_all_button_handler(self, handler : callable = None) -> None:
        """
        Configura el funcionamiento del botón 'eliminar todos'.
        """
        self.remove_all_button.configure(command=handler)
    

    def _select_record(self, e = None) -> None:
        """
        Recupera el elemento seleccionado en la tabla (TreeView) y lleva sus valores a las
        cajas de texto. Este método funciona como un OnClick callback.
        """
        # Limpiar las cajas de texto
        self.clear()
        
        # Recuperar fila seleccionada
        selected = self.tree_view.focus()
        # Recuperar los valores de la fila
        values = self.tree_view.item(selected, 'values')

        if values:
            # Llevar los datos a las cajas de texto
            self._toggle_id_input()                # Habilitar input
            self.id_input.insert(0, values[0])
            self._toggle_id_input()                # Deshabilitar input
            self.name_input.insert(0, values[1])
            self.number_input.insert(0, values[2])


    def _init_click_binder(self) -> None:
        """
        Enlaza el evento Click con el método select_record.
        """
        self.tree_view.bind("<ButtonRelease-1>", self._select_record)


    def add_record(self, record : dict) -> None:
        """
        Añade un nuevo registro. Actualiza la tabla de datos (TreeView).

        Parámetros:
          - id (int) : Id del nuevo registro
        """
        # Recuperar número de elementos en la tabla
        i = len(self.tree_view.get_children())

        # Recuperar los datos del nuevo registro.
        data = [record['id'], record['name'], record['number']]

        # Si es una fila par o no
        tag = 'evenrow' if (i % 2 == 0) else 'oddrow'

        # Inserción de datos de la fila en el treeview
        self.tree_view.insert(
            parent='',
            index='end',
            iid=data[0], # id
            values=data,
            tags=(tag)
        )

        # Limpiar inputs
        self.clear()


    def update_record(self) -> None:
        """
        Actualiza el registro seleccionado. Se delega en el controlador para la 
        actualización en la base de datos. Actualiza la tabla de datos (TreeView) para 
        reflejar los cambios.
        """
        # Recuperar elemento seleccionado
        selected = self.tree_view.focus()
        # Recuperar los datos en los campos de texto
        data = [self.id_input.get(), self.name_input.get(), self.number_input.get()]
        # Actualizar los datos
        self.tree_view.item(selected, values=data)

        # Quitar foco del elemento
        self.tree_view.selection_remove(selected)
        # Limpiar inputs
        self.clear()


    def remove_one(self) -> None:
        """
        Elimina el registro seleccionado de la base de datos (delega en el controlador). 
        Actualiza la tabla de datos (TreeView) para reflejar los cambios.
        """
        row = self.tree_view.focus()
        self.tree_view.delete(row)
        
        # Limpiar inputs
        self.clear()


    def remove_all(self) -> None:
        """
        Elimina todos los datos de la tabla actual de la base de datos (delega en el 
        controlador). Actualiza la tabla de datos (TreeView) para reflejar los cambios.
        """
        for row in self.tree_view.get_children():
            self.tree_view.delete(row)

        # Limpiar inputs
        self.clear()


    def clear(self) -> None:
        """
        Limpia las cajas de texto (inputs)
        """
        self._toggle_id_input()                # Habilitar input id
        self.id_input.delete(0, END)
        self._toggle_id_input()                # Deshabilitar input id
        self.name_input.delete(0, END)
        self.number_input.delete(0, END)


if __name__ == '__main__':
    """
    Programa principal, solo para pruebas.
    """
    root = MainWindow()
    root.mainloop()
