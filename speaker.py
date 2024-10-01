import ctypes
import os

# Obtenemos el directorio actual donde se encuentra el script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Definimos la ruta a la DLL dentro de la subcarpeta 'lib'
dll_path = os.path.join(current_dir, 'lib', 'nvdaControllerClient64.dll')

# depuración
print("Ruta de la DLL:", dll_path)

# Verifica si la DLL existe
if not os.path.exists(dll_path):
	print("La DLL no se encontró en la ruta especificada.")
else:
	# Carga la DLL
	nvda_dll = ctypes.CDLL(dll_path)

	# Define el tipo de argumento y el tipo de retorno para la función en la DLL
	nvda_dll.nvdaController_speakText.argtypes = [ctypes.c_wchar_p]
	nvda_dll.nvdaController_speakText.restype = None

	def alert(message):
		speak_text(message)

	def speak_text(text):
		# Llama a la función de la DLL para que NVDA lea el texto
		nvda_dll.nvdaController_speakText(text)
