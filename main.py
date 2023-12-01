from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import json
import datetime
from flask import make_response

# Crear la aplicación
app = Flask(__name__)
CORS(app)

# Crear la clase Cuenta
class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.operaciones = []

    def __str__(self):
        return "Numero: " + self.numero + ", Nombre: " + self.nombre + ", Saldo: " + str(self.saldo) + ", Contactos: " + str(self.contactos) + ", Operaciones: " + str(self.operaciones)

    def agregarOperacion(self, operacion):
        self.operaciones.append(operacion)

    def getOperaciones(self):
        return self.operaciones

    def getContactos(self):
        return self.contactos

    def getSaldo(self):
        return self.saldo

    def getNombre(self):
        return self.nombre

    def getNumero(self):
        return self.numero

    def setSaldo(self, saldo):
        self.saldo = saldo

    def setContactos(self, contactos):
        self.contactos = contactos

    def setNombre(self, nombre):
        self.nombre = nombre

    def setNumero(self, numero):
        self.numero = numero

# Crear la clase Operacion
class Operacion:
    def __init__(self, numeroDestino, fecha, valor):
        self.numeroDestino = numeroDestino
        self.fecha = fecha
        self.valor = valor

    def __str__(self):
        return "Numero destino: " + self.numeroDestino + ", Fecha: " + self.fecha + ", Valor: " + str(self.valor)

    def getNumeroDestino(self):
        return self.numeroDestino

    def getFecha(self):
        return self.fecha

    def getValor(self):
        return self.valor

    def setNumeroDestino(self, numeroDestino):
        self.numeroDestino = numeroDestino

    def setFecha(self, fecha):
        self.fecha = fecha

    def setValor(self, valor):
        self.valor = valor
    
# Crear la lista de cuentas
BD = []
BD.append(Cuenta("21345", "Arnaldo", 200, ["123", "456"]))
BD.append(Cuenta("123", "Luisa", 400, ["456"]))
BD.append(Cuenta("456", "Andrea", 300, ["21345"]))
BD.append(Cuenta("789", "Christian", 100, ["123"]))
BD.append(Cuenta("78955", "Pedro", 100, []))


# Crear la lista de operaciones
operaciones = []
operaciones.append(Operacion("123", "11/07/2023", 100))
operaciones.append(Operacion("456", "11/07/2023", 50))
operaciones.append(Operacion("21345", "11/07/2023", 200))
operaciones.append(Operacion("123", "11/07/2023", 300))
operaciones.append(Operacion("456", "11/07/2023", 400))

# Crear el endpoint /billetera/contactos?minumero=XXXX

@app.route('/billetera/contactos', methods=['GET'])
def contactos():
    numero = request.args.get('minumero')
    for cuenta in BD:
        if cuenta.getNumero() == numero:
            contactos_info = {}
            for contacto in cuenta.getContactos():
                for c in BD:
                    if c.getNumero() == contacto:
                        contactos_info[contacto] = c.getNombre()
            if not contactos_info:
                response = make_response(jsonify("El usuario no tiene contactos"), 400)
            else:
                response = make_response(jsonify(contactos_info), 200)
            return response
    # Si no se encuentra el número, devolver una respuesta con código de estado 400
    response = make_response(jsonify("No se encontro el numero"), 400)
    return response


# Definir el endpoint /billetera/pagar?minumero=XXXX&numerodestino=YYYY&valor=ZZZZ
@app.route('/billetera/pagar', methods=['GET'])
def pagar():
    numero = request.args.get('minumero')
    numeroDestino = request.args.get('numerodestino')
    valor = int(request.args.get('valor'))

    for cuenta in BD:
        if cuenta.getNumero() == numero:  #Verificar si el número de cuenta coincide con el parámetro 'numero'
            if cuenta.getSaldo() >= valor:  #Verificar si la cuenta tiene saldo suficiente para realizar el pago
                for contacto in cuenta.getContactos():  #Iterar sobre los contactos de la cuenta
                    if contacto == numeroDestino:  #Verificar si el contacto coincide con el parámetro 'numerodestino'
                        # Actualizar los saldos de las cuentas y agregar registros de operaciones
                        cuenta.setSaldo(cuenta.getSaldo() - valor)
                        cuenta.agregarOperacion(Operacion(numeroDestino, datetime.datetime.now().strftime("%d/%m/%Y"), valor))

                        for cuenta_destino in BD:
                            if cuenta_destino.getNumero() == numeroDestino:  #Verificar si el número de cuenta de destino coincide
                                #Actualizar el saldo de la cuenta de destino y agregar registros de operaciones
                                cuenta_destino.setSaldo(cuenta_destino.getSaldo() + valor)
                                cuenta_destino.agregarOperacion(Operacion(numero, datetime.datetime.now().strftime("%d/%m/%Y"), valor))
                                response = make_response(jsonify("Realizado en " + str(datetime.datetime.now().strftime("%d/%m/%Y"))), 200)
                                return response

                        return make_response(jsonify("No se encontro el contacto"), 400)  #Contacto no encontrado

                return make_response(jsonify("El numero de destino no ha sido encontrado"), 400)  #Cuenta de destino no encontrada

            return make_response(jsonify("No tiene saldo suficiente"), 400)  #saldo insuficiente

    return make_response(jsonify("No se encontro el numero de entrada"), 400)  #Cuenta no encontrada


# Crear el endpoint /billetera/historial?minumero=XXXX
@app.route('/billetera/historial', methods=['GET'])
def historial():
    numero = request.args.get('minumero')
    for cuenta in BD:
        if cuenta.getNumero() == numero:
            return jsonify("Saldo de " + cuenta.getNombre() + ": " + str(cuenta.getSaldo()) + " Operaciones de " + cuenta.getNombre() + ": " + str(cuenta.getOperaciones()))
    return make_response(jsonify("No se encontro el numero"),400)

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=5000)