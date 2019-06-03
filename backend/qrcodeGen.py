#Codigo para gerar QRCODE a partir de chave de usuario
#Utilizacao: python qrcodeGen.py USER_KEY
#Output: QRCODE com o mesmo id da chave passada como parametro

#Para rodar este codigo eh necessario fazer:
# pip install pyqrcode e pip install pypng
import sys
import pyqrcode


def generate_qr():
    hashKeyUser = str(sys.argv[1])
    print("CREATING QRCODE FOR USER:" + hashKeyUser)
    qrCode = pyqrcode.create(hashKeyUser)
    fileName = hashKeyUser + ".png"
    qrCode.png(fileName, scale=8)
    print("QR CODE CREATED")


if __name__ == '__main__':
    generate_qr()
