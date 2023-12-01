# Pregunta 3

> **Se requiere realizar un cambio en el software para que soporte un valor máximo de 200 soles a transferir por día.**
> 

# Qué cambiaría en el código (Clases / Métodos) - No implementación.

Para implementar un límite diario de transferencia de 200 soles, debo realizar cambios en mi clase `Cuenta:`

1. Añadir un nuevo atributo para rastrear la cantidad total de dinero transferido en el día actual.
2. Añadir un nuevo atributo para rastrear la fecha de la última transferencia.
3. Crear un nuevo método `verificar_limite_diario` para verificar si una transferencia propuesta excedería el límite diario. Este método debería:
    - Comprobar si la fecha de la última transferencia es hoy. Si no es así, restablecer la cantidad total de dinero transferido a 0.
    - Sumar la cantidad de la transferencia propuesta a la cantidad total de dinero transferido y comprobar si el resultado excede 200. Si es así, rechazar la transferencia.
4. Crear un método `transferir` que maneja la lógica de transferencia y verifica el límite diario.

```python
Clase Cuenta:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.operaciones = []

        self.total_transferido_hoy = 0 #Cambios 1
        self.fecha_ultima_transferencia = None #Cambios 2

    def verificar_limite_diario(self, monto_transferencia): #Cambios 3
        Si self.fecha_ultima_transferencia no es igual a la fecha actual:
            Establecer self.total_transferido_hoy a 0

        Si self.total_transferido_hoy + monto_transferencia > 200:
            Lanzar ValorError con mensaje "La transferencia excede el límite diario de 200 soles."
        Sino:
            Retornar Verdadero

    def transferir(self, numero_destino, monto): #Cambios 4
        Si monto <= 0:
            Lanzar ValorError con mensaje "El monto de la transferencia debe ser mayor que cero."

        Si self.saldo < monto:
            Lanzar ValorError con mensaje "Saldo insuficiente para realizar la transferencia."

        Si no self.verificar_limite_diario(monto):
            Lanzar ValorError con mensaje "La transferencia excede el límite diario."

        # Realizar la transferencia
        Restar monto de self.saldo
        Sumar monto a self.total_transferido_hoy
        Establecer self.fecha_ultima_transferencia a la fecha actual

        # Registrar la operación
        operacion = "Transferencia a ", numero_destino, ": ", monto, " soles"
        Agregar operacion a self.operaciones

    def getSaldo(self):
        Retornar self.saldo
```

# Nuevos casos de prueba a adicionar.

Con la nueva funcionalidad de límite diario de transferencia, podría agregar los siguientes casos de prueba:

1. **Prueba de transferencia exitosa por debajo del límite diario**: Esta prueba verificaría que una transferencia se realiza con éxito cuando el monto total transferido en el día aún no ha alcanzado el límite de 200 soles.
2. **Prueba de transferencia fallida por encima del límite diario**: Esta prueba verificaría que una transferencia es rechazada cuando el monto total transferido en el día ya ha alcanzado o excedido el límite de 200 soles.
3. **Prueba de reinicio del límite diario**: Esta prueba verificaría que el monto total transferido se restablece a 0 al comienzo de un nuevo día.
4. **Prueba de varias transferencias en un día**: Esta prueba verificaría que varias transferencias pueden realizarse en un solo día, siempre que el monto total transferido no exceda el límite de 200 soles.

En `test_main.py`, podría crear una nueva clase `TestTransferencia` para tener en cuenta el nuevo límite diario de transferencia. 

```python
class TestTransferencia(TestCase):
    def test_transferencia_exitosa_por_debajo_del_limite_diario(self):
        #Configurar una cuenta con un saldo suficiente
        cuenta = Cuenta('123', 'Amen', 300, {})
        #Realizar una transferencia de menos de 200 soles
        cuenta.transferir('456', 150)
        #Verificar que la transferencia fue exitosa
        self.assertEqual(cuenta.getSaldo(), 150)

    def test_transferencia_fallida_por_encima_del_limite_diario(self):
        #Configurar una cuenta con un saldo suficiente
        cuenta = Cuenta('123', 'Amen', 300, {})
        #Realizar una transferencia de más de 200 soles
        with self.assertRaises(ValueError):
            cuenta.transferir('456', 250)

    def test_reinicio_del_limite_diario(self):
        #Configurar una cuenta con un saldo suficiente
        cuenta = Cuenta('123', 'Amen', 500, {})
        # Realizar una transferencia de 200 soles
        cuenta.transferir('456', 200)
        # Avanzar al día siguiente
        cuenta.setFecha(datetime.date.today() + datetime.timedelta(days=1))
        # Realizar otra transferencia de 200 soles
        cuenta.transferir('456', 200)
        # Verificar que ambas transferencias fueron exitosas
        self.assertEqual(cuenta.getSaldo(), 100)

    def test_varias_transferencias_en_un_dia(self):
        # Configurar una cuenta con un saldo suficiente
        cuenta = Cuenta('123', 'Amen', 300, {})
        # Realizar varias transferencias que sumen menos de 200 soles
        cuenta.transferir('456', 100)
        cuenta.transferir('456', 50)
        # Verificar que todas las transferencias fueron exitosas
        self.assertEqual(cuenta.getSaldo(), 150)
```

# Cuánto riesgo hay de “romper” lo que ya funciona?

La estructura del código en **`main.py`** y **`test_main.py`** se ha organizado cuidadosamente para minimizar posibles problemas al realizar cambios en la clase **`Cuenta`** y agregar nuevos casos de prueba en **`TestTransferencia(TestCase)`**. Este enfoque sigue buenas prácticas de desarrollo de software:

- **Encapsulamiento:** Las operaciones de la cuenta están encapsuladas en la clase **`Cuenta`**, ocultando los detalles internos del resto del código. Esto permite realizar ajustes internos, como agregar un límite de transferencia diario, sin afectar otras partes del código, siempre y cuando la interfaz pública de **`Cuenta`** permanezca sin cambios.
- **Pruebas unitarias:** Se han implementado pruebas unitarias en **`test_main.py`** para verificar el correcto funcionamiento de la clase **`Cuenta`**. La adición de nuevos casos de prueba al introducir nuevas funcionalidades asegura que estas operen adecuadamente. La ejecución exitosa de todas las pruebas proporciona confianza en la ausencia de errores.
- **Desarrollo incremental:** Los cambios se han realizado de manera incremental, con ajustes pequeños seguidos de pruebas. Este enfoque facilita la detección inmediata de posibles problemas, simplificando la resolución al tener una comprensión clara de qué cambio está relacionado con cualquier inconveniente.