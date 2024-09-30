import wx
import random
import pygame
import time
import threading
import os
import sys
from speaker import alert

class RuletaApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(RuletaApp, self).__init__(*args, **kw)

        # Inicializar la interfaz gráfica
        self.init_ui()

        # Inicializar el mixer de pygame
        pygame.mixer.init()

    def init_ui(self):
        panel = wx.Panel(self)

        # Etiqueta para el cuadro de texto
        lbl_element = wx.StaticText(panel, label="Ingrese un elemento:", pos=(10, 10))
        # Cuadro de texto para añadir elementos
        self.txt_element = wx.TextCtrl(panel, pos=(10, 30), size=(200, -1))
        
        # Botón para añadir el elemento a la lista
        btn_add = wx.Button(panel, label="&Añadir", pos=(220, 30))
        btn_add.Bind(wx.EVT_BUTTON, self.on_add_element)
        
        # etiqueta y Lista de elementos añadidos
        lbl_elements = wx.StaticText(panel, label="&Elementos añadidos:", pos=(10, 10))
        self.list_elements = wx.ListBox(panel, pos=(10, 70), size=(300, 200))

        # Botón para girar la ruleta
        self.btn_spin = wx.Button(panel, label="&Girar Ruleta", pos=(10, 280))
        self.btn_spin.Bind(wx.EVT_BUTTON, self.on_spin_thread)

        # Botón para eliminar todos los elementos de la lista
        btn_clear = wx.Button(panel, label="Eliminar Todos", pos=(120, 280))
        btn_clear.Bind(wx.EVT_BUTTON, self.on_clear_elements)

        # Configuración de la ventana
        self.SetTitle("Ruleta Simple")
        self.SetSize((350, 400))
        self.Centre()

    def resource_path(self, relative_path):
        """ Obtiene la ruta del recurso, ya sea en desarrollo o en el ejecutable. """
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def on_add_element(self, event):
        element = self.txt_element.GetValue()
        if element:
            self.list_elements.Append(element)
            alert(f"Elemento añadido: {element}")
            self.current_items = self.list_elements.GetItems()
            alert(f"Cantidad actual de elementos en la lista: {len(self.current_items)}")
            self.txt_element.SetValue("")  # Limpiar el cuadro de texto
            self.txt_element.SetFocus()  # Enfocar el cuadro de texto nuevamente

    def on_clear_elements(self, event):
        """Elimina todos los elementos de la lista."""
        self.list_elements.Clear()
        alert("Todos los elementos han sido eliminados.")

    def on_spin_thread(self, event):
        """Inicia el hilo para ejecutar la función on_spin."""
        hilo = threading.Thread(target=self.on_spin, daemon=True)
        hilo.start()

    def on_spin(self):
        elements = self.list_elements.GetItems()
        if not elements:
            wx.CallAfter(wx.MessageBox, "No hay elementos en la lista para girar la ruleta.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Deshabilitar el botón y cambiar el texto
        wx.CallAfter(self.update_button_state, False, "Ruleta en progreso...")

        # Obtener la ruta del archivo de sonido
        sound_path = self.resource_path("ruleta.ogg")

        # Reproducir el sonido de la ruleta
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()

        # Esperar a que termine el sonido
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        # Elegir un elemento aleatorio
        chosen_element = random.choice(elements)
        wx.CallAfter(wx.MessageBox, f"El resultado de la ruleta es: {chosen_element}", "Resultado", wx.OK | wx.ICON_INFORMATION)

        # Habilitar el botón y restaurar el texto
        wx.CallAfter(self.update_button_state, True, "Girar Ruleta")

    def update_button_state(self, enabled, label):
        """Actualiza el estado del botón y su etiqueta."""
        self.btn_spin.SetLabel(label)
        self.btn_spin.Enable(enabled)

if __name__ == "__main__":
    app = wx.App(False)
    frame = RuletaApp(None)
    frame.Show()
    app.MainLoop()
