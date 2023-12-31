import unittest
from flask import Flask, jsonify, request
from main import app
import datetime


class ContactosTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_contactos_success(self):
        # Caso de prueba para una solicitud exitosa con un 'minumero' válido
        response = self.app.get('/billetera/contactos?minumero=21345')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
                            "123": "Luisa",
                            "456": "Andrea"
                            })

    def test_contactos_invalid_numero(self):
        # Caso de prueba para un parámetro 'minumero' inválido
        response = self.app.get('/billetera/contactos?minumero=987654321')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), "No se encontro el numero")

    def test_contactos_no_match(self):
        # Caso de prueba para un 'minumero' que no coincide con ninguna cuenta
        response = self.app.get('/billetera/contactos?minumero=78955')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), "El usuario no tiene contactos")

    def test_contactos_missing_parameter(self):
        # Caso de prueba para un parámetro 'minumero' faltante
        response = self.app.get('/billetera/contactos')
        self.assertEqual(response.status_code, 400)

class PagarTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_pagar_success(self):
        # Caso de prueba para un pago exitoso con parámetros válidos
        response = self.app.get('/billetera/pagar?minumero=21345&numerodestino=123&valor=100')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), "Realizado en " + str(datetime.datetime.now().strftime("%d/%m/%Y")))

    def test_pagar_invalid_numero_destino(self):
        # Cuenta de destino no encontrada
        response = self.app.get('/billetera/pagar?minumero=21345&numerodestino=555555555&valor=100')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), "El numero de destino no ha sido encontrado")
    
    def test_pagar_insufficient_balance(self):
        # Caso de prueba para saldo insuficiente en la cuenta
        response = self.app.get('/billetera/pagar?minumero=21345&numerodestino=123&valor=1000')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), "No tiene saldo suficiente")
    
    def test_pagar_missing_contact(self):
        # Caso de prueba para un parámetro faltante
        response = self.app.get('/billetera/pagar?minumero=21345&numerodestino=457&valor=100')
        self.assertEqual(response.status_code, 400)

class HistorialTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_historial_success(self):
        # Caso de prueba para una solicitud exitosa con un 'minumero' válido
        response = self.app.get('/billetera/historial?minumero=21345')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), "Saldo de Arnaldo: 200 Operaciones de Arnaldo: []")

    def test_historial_invalid_numero(self):
        # Caso de prueba para un parámetro 'minumero' inválido
        response = self.app.get('/billetera/historial?minumero=987654321')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), "No se encontro el numero")

    def test_historial_no_match(self):
        # Caso de prueba para un 'minumero' que no coincide con ninguna cuenta
        response = self.app.get('/billetera/historial?minumero=555555555')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), "No se encontro el numero")

    def test_historial_missing_parameter(self):
        # Caso de prueba para un parámetro 'minumero' faltante
        response = self.app.get('/billetera/historial')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
