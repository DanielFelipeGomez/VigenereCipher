from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QLineEdit, QLabel, QPlainTextEdit
from PySide6.QtCore import Qt


class VigenereCipher:
    """Representa cifrador de Vigenere

    Attributes:
        alphabet (list): [Alfabeto disponible para cifrar]
        plain_text (str): [Texto de entrada que se desea cifrar]
        key (str): [Clave del cifrado]
        cipher_text (str): [Salida de texto cifrado]
        blocks (list): [Bloques del mensaje según la clave]
    """
    def __init__(self, plain_text, key):
        """Inicializa un objeto de tipo VigenereCipher

        Args:
            plain_text (str) : [Texto de entrada que se desea cifrar]
            key (str) : [Clave del cifrado]
        """
        self._alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                          'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                          'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self._plain_text = plain_text
        self._key = key
        self._cipher_text = ''
        self.blocks = []
        self.define_blocks()

    def find_index(self, character):
        """Retorna el indice donde se encuentra un caracter en el alfabeto

        Args:
            character (str)

        Returns:
            int
        """
        index = 0
        for c in self._alphabet:
            if c == character:
                return index
            index += 1
        return -1

    def define_blocks(self):
        """Separa el mensaje inicial en bloques egún la clave dada"""
        index = 0
        aux = ''
        for i in self._plain_text.replace(' ', ''):
            aux += i
            index += 1
            if index == len(self._key):
                self.blocks.append(aux)
                aux = ''
                index = 0
        else:
            self.blocks.append(aux)

    def encrypt(self):
        """Encripta en mensaje usando el cifrado de Vigenere

        Returns:
            list
        """
        bloques_cifrados = []
        aux = ''
        for block in self.blocks:
            index = 0
            for character in block:
                car = (self.find_index(character) + self.find_index(self._key[index]))
                if car >= 26:
                    car = car % 26
                aux += self._alphabet[car]
                index += 1
            bloques_cifrados.append(aux)
            aux = ''
        self._cipher_text = "".join(bloques_cifrados)
        return [self.blocks, bloques_cifrados]

    def decrypt(self):
        """Descencripta en mensaje usando el cifrado de Vigenere

        Returns:
            list
        """
        bloques_cifrados = []
        aux = ''
        for bloque in self.blocks:
            index = 0
            for character in bloque:
                car = (self.find_index(character) - self.find_index(self._key[index]))
                if car >= 26 or car < 0:
                    car = car % 26
                aux += self._alphabet[car]
                index += 1
            bloques_cifrados.append(aux)
            aux = ''
        self._cipher_text = "".join(bloques_cifrados)
        return [self.blocks, bloques_cifrados]


class MainWindow(QMainWindow):
    """Clase encargada de generar GUI y recibir los datos del usuario
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dialogos en PySide')
        # creamos linea de la clave
        key_label = QLabel("Intriduce la clave", self)
        key_label.move(110,10)
        self.key = QPlainTextEdit(self)
        self.key.move(20, 40)
        self.key.resize(260, 40)
        # creamos linea para el mensaje
        plain_text_label = QLabel("Intriduce la clave", self)
        plain_text_label.move(110, 80)
        self.plain_text = QPlainTextEdit(self)
        self.plain_text.move(20, 110)
        self.plain_text.resize(260, 40)
        # Definimos un boton
        encrypt_button = QPushButton('Cifrar en Vigenere', self)
        encrypt_button.move(20, 160)
        encrypt_button.resize(120,30)
        encrypt_button.clicked.connect(self.vigenere_cipher)
        decrypt_button = QPushButton('Descifrar en Vigenere', self)
        decrypt_button.move(160, 160)
        decrypt_button.resize(120, 30)
        decrypt_button.clicked.connect(self.vigenere_decryption)
        # creamos etiqueta de mensaje de salida
        self.output_label = QLabel(self)
        self.output_label.move(30, 200)
        self.output_label.resize(260, 40)
        self.output_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setWindowIcon(QIcon('candado.ico'))
        self.setGeometry(300, 300, 300, 350)
        self.setWindowTitle('Cifrador Vigenere')

    def vigenere_cipher(self):
        """Encargado de recopilar la infromación necesaria para ejecutar el encriptado con ayuda de CypherVigenere"""
        blocks, encrypted_blocks = VigenereCipher(self.plain_text.toPlainText(), self.key.toPlainText()).encrypt()
        self.output_label.setText("  ".join(blocks) + '\n' + "  ".join(encrypted_blocks))

    def vigenere_decryption(self):
        """Encargado de recopilar la infromación necesaria para ejecutar el descencriptado con ayuda de CypherVigenere"""
        blocks, encrypted_blocks = VigenereCipher(self.plain_text.toPlainText(), self.key.toPlainText()).decrypt()
        self.output_label.setText("  ".join(blocks) + '\n' + "  ".join(encrypted_blocks))


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()