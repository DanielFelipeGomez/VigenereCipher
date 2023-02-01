from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QLineEdit, QLabel, QPlainTextEdit
from PySide6.QtCore import Qt


class VigenereCipher:
    def __init__(self, plain_text, key):
        self._plain_text = plain_text
        self._key = key
        self._cipher_text = ''
        self.blocks = []
        self.define_blocks()

    def define_blocks(self):
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
        bloques_cifrados = []
        aux = ''
        for bloque in self.blocks:
            index = 0
            for caracter in bloque:
                car = (ord(caracter) - 65) + (ord(self._key[index]) - 65)
                if car >= 26:
                    car = car % 26
                aux += chr(car + 65)
                index += 1
            bloques_cifrados.append(aux)
            aux = ''
        self._cipher_text = "".join(bloques_cifrados)
        return [self.blocks, bloques_cifrados]

    def decrypt(self):
        bloques_cifrados = []
        aux = ''
        for bloque in self.blocks:
            index = 0
            for caracter in bloque:
                car = (ord(caracter) - 65) - (ord(self._key[index]) - 65)
                if car >= 26 or car < 0:
                    car = car % 26
                aux += chr(car + 65)
                index += 1
            bloques_cifrados.append(aux)
            aux = ''
        self._cipher_text = "".join(bloques_cifrados)
        return [self.blocks, bloques_cifrados]


class MainWindow(QMainWindow):
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
        blocks, encrypted_blocks = VigenereCipher(self.plain_text.toPlainText(), self.key.toPlainText()).encrypt()
        self.output_label.setText("  ".join(blocks) + '\n' + "  ".join(encrypted_blocks))

    def vigenere_decryption(self):
        blocks, encrypted_blocks = VigenereCipher(self.plain_text.toPlainText(), self.key.toPlainText()).decrypt()
        self.output_label.setText("  ".join(blocks) + '\n' + "  ".join(encrypted_blocks))


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()