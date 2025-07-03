# Documentación de Pruebas - Patient Appointment System Backend

Este documento describe las pruebas realizadas en el sistema, detallando qué se prueba, cómo se prueba, con qué datos, el tipo de prueba, el módulo evaluado y el resultado esperado.

---

## Resumen de Pruebas Realizadas

### 1. Pruebas Unitarias

#### a) Controlador de Citas (`controllers/appointmentController.py`)
- **Archivo:** `tests/test_appointment_controller.py`
- **Tipo de prueba:** Unitaria
- **Qué se prueba:**  
  - Creación de citas virtuales y presenciales.
  - Validación de modalidad de cita.
  - Obtención de todas las citas pendientes.
- **Cómo se prueba:**  
  - Uso de objetos simulados (mocks) para la base de datos y dependencias externas (correo, Jitsi).
  - Creación de datos de ejemplo para pacientes, servicios y slots.
  - Verificación de la creación correcta de la cita según la modalidad y generación de enlaces/correos.
  - Validación de excepción para modalidad inválida.
- **Con qué datos:**  
  - Paciente: `Id=1, Name="John Doe", Email="john@example.com"`
  - Servicio: `Id=1, Name="Consulta General"`
  - Slot: `Id=1, Time="09:00 - 10:00"`
  - Modalidades: `"Virtual"`, `"Presential"`, `"InvalidModality"`
- **Resultado esperado:**  
  - Las citas virtuales generan enlace de reunión y correo.
  - Las citas presenciales no generan enlace.
  - Modalidad inválida lanza error 400.
  - Se obtienen todas las citas pendientes correctamente.
- **Resultado:** Pasó

#### b) Utilidades de Jitsi (`utils/jitsi_utils.py`)
- **Archivo:** `tests/test_jitsi.py`
- **Tipo de prueba:** Unitaria
- **Qué se prueba:**  
  - Generación de IDs de reunión.
  - Generación de tokens JWT para Jitsi.
  - Obtención de enlaces y tokens de reunión.
- **Cómo se prueba:**  
  - Pruebas de funciones puras con diferentes nombres y datos.
  - Simulación de dependencias como la clave privada y el builder de JWT.
- **Con qué datos:**  
  - Nombres: `"John Doe"`, `"María José"`
  - IDs: `123`, `456`
- **Resultado esperado:**  
  - Los IDs y enlaces se generan correctamente según el formato esperado.
  - El token JWT se genera y utiliza la clave privada simulada.
- **Resultado:** Pasó

---

### 2. Pruebas de Integración

#### a) Rutas de Citas (`routes/appointmentRoutes.py`)
- **Archivo:** `tests/test_appointment_routes.py`
- **Tipo de prueba:** Integración
- **Qué se prueba:**  
  - Creación de citas vía endpoint `/appointment`.
  - Validación de datos requeridos.
  - Obtención de citas de un paciente, citas del día, todas las citas.
  - Creación de prescripciones.
  - Obtención del total de citas pendientes.
  - Obtención de token y enlace Jitsi para una cita.
- **Cómo se prueba:**  
  - Uso de `TestClient` de FastAPI para peticiones HTTP a los endpoints.
  - Simulación de dependencias externas (correo, Jitsi) con mocks.
- **Con qué datos:**  
  - Datos de cita: problema, fecha, IDs de paciente, servicio y slot, modalidad.
  - Datos inválidos: omisión de campos requeridos.
  - Prescripción: `"Paracetamol 500mg cada 8 horas"`
- **Resultado esperado:**  
  - Las citas se crean correctamente y devuelven los datos esperados.
  - La validación de datos responde con error 422 si faltan campos.
  - Los endpoints de consulta devuelven listas o enteros según corresponda.
  - El endpoint de prescripción actualiza el estado de la cita.
- **Resultado:** Pasó

#### b) Pruebas de Integración Completa (`tests/test_integration.py`)
- **Tipo de prueba:** Integración
- **Qué se prueba:**  
  - Flujo completo de creación de paciente y cita virtual con integración de Jitsi y notificación por correo.
  - Manejo de errores al crear citas con datos inválidos.
- **Cómo se prueba:**  
  - Creación de pacientes y citas reales en la base de datos de pruebas.
  - Simulación de funciones de correo y Jitsi.
  - Verificación de generación de enlaces y correos.
  - Validación de errores cuando el paciente no existe.
- **Con qué datos:**  
  - Pacientes con datos únicos generados en cada prueba.
  - Citas virtuales con modalidad `"Virtual"`.
  - Citas con IDs de paciente inexistentes para probar errores.
- **Resultado esperado:**  
  - El enlace de Jitsi y el correo se generan correctamente.
  - El sistema responde con error 400 si el paciente no existe.
- **Resultado:** Pasó

---

## Conclusión

Las pruebas cubren tanto la lógica interna de los controladores y utilidades (unitarias) como la integración de los endpoints y el flujo completo de negocio (integración). Se utilizan datos simulados y reales, y se validan tanto los casos exitosos como los de error. Todas las pruebas han pasado correctamente, evidenciando el correcto funcionamiento de los módulos principales del sistema de citas para pacientes.

---

## Resultados de la última ejecución de pruebas

A continuación se muestran los resultados de la última ejecución de pruebas, donde se evidencia que todas las pruebas fueron exitosas: 
- tests/test_appointment_controller.py::test_create_appointment_virtual PASSED
- tests/test_appointment_controller.py::test_create_appointment_presential PASSED
- tests/test_appointment_controller.py::test_create_appointment_invalid_modality PASSED
- tests/test_appointment_controller.py::test_get_all_appointments_pending PASSED
- tests/test_appointment_routes.py::test_create_appointment_endpoint PASSED
- tests/test_appointment_routes.py::test_create_appointment_invalid_data PASSED
- tests/test_appointment_routes.py::test_get_patient_appointments PASSED
- tests/test_appointment_routes.py::test_get_todays_appointments PASSED
- tests/test_appointment_routes.py::test_get_all_appointments PASSED
- tests/test_appointment_routes.py::test_create_prescription PASSED
- tests/test_appointment_routes.py::test_get_total_pending_appointments PASSED
- tests/test_appointment_routes.py::test_get_jitsi_token PASSED
- tests/test_integration.py::test_virtual_appointment_jitsi_integration PASSED
- tests/test_integration.py::test_virtual_appointment_email_notification PASSED
- tests/test_integration.py::test_invalid_virtual_appointment_creation PASSED
- tests/test_jitsi.py::test_generate_meeting_id PASSED
- tests/test_jitsi.py::test_generate_jitsi_jwt PASSED
- tests/test_jitsi.py::test_get_jitsi_meeting_link_and_token PASSED