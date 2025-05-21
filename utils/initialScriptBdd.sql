-- Inserciones para la tabla 'patients'
INSERT INTO patients (Name, Mobile, Email, Address, Gender, BloodGroup) VALUES
('Maria Gonzalez', '5551234567', 'maria.gonzalez@gmail.com', 'Calle 10 #123, Ciudad de Mexico', 'Femenino', 'A+'),
('Juan Perez', '5552345678', 'juanperez@hotmail.com', 'Av. Reforma 456, CDMX', 'Masculino', 'O+'),
('Laura Martinez', '5553456789', 'lauramartinez@yahoo.com', 'Calle Lago Azul 89, Monterrey', 'Femenino', 'B+'),
('Carlos Ramirez', '5554567890', 'carlos.ramirez@gmail.com', 'Calle Real 12, Guadalajara', 'Masculino', 'AB-'),
('Ana Torres', '5555678901', 'ana.torres@gmail.com', 'Col. Jardines, Puebla', 'Femenino', 'O-'),
('Luis Hernandez', '5556789012', 'luis.hdz@outlook.com', 'Calle Sol 21, Merida', 'Masculino', 'A-'),
('Sofia Rojas', '5557890123', 'sofiarojas@gmail.com', 'Blvd. Central 77, Cancun', 'Femenino', 'AB+'),
('Diego Vargas', '5558901234', 'diego.vg@live.com', 'Centro, Leon', 'Masculino', 'B-'),
('Isabel Lopez', '5559012345', 'isalopez@gmail.com', 'Calle Luna 33, Queretaro', 'Femenino', 'A+'),
('Miguel Ortega', '5550123456', 'miguel.ortega@correo.com', 'Col. Roma, CDMX', 'Masculino', 'O+');

-- Inserciones para la tabla 'services'
INSERT INTO services (Name, Description, Price) VALUES
('Consulta General', 'Evaluacion medica general para diagnostico y tratamiento basico.', 25),
('Lectura de radiografias', 'Informe medico detallado sobre imagenes de rayos X.', 22.00),
('Electroencefalograma (EEG)', 'Estudio de la actividad electrica cerebral mediante electrodos.', 50.00),
('Electrocardiograma (ECG)', 'Evaluacion grafica de la actividad electrica del corazon.', 30.00),
('Toma de muestra de sangre', 'Extraccion de sangre para analisis clinicos de laboratorio.', 12.00),
('Curacion de heridas', 'Atencion medica para desinfeccion, limpieza y vendaje de heridas.', 20.00),
('Inyecciones y aplicacion de medicamentos', 'Administracion intramuscular o intravenosa de farmacos.', 8.00),
('Nebulizacion', 'Tratamiento respiratorio con medicamentos vaporizados.', 15.00),
('Control de signos vitales', 'Medicion de presion arterial, pulso, temperatura y saturacion.', 5.00),
('Prueba rapida de glucosa', 'Medicion instantanea del nivel de azucar en sangre.', 7.00);

-- Inserciones para la tabla 'slots'
INSERT INTO slots (Time, Status) VALUES
('08:00 - 09:00', 'Disponible'),
('09:00 - 10:00', 'Ocupado'),
('10:00 - 11:00', 'Disponible'),
('11:00 - 12:00', 'Disponible'),
('12:00 - 13:00', 'Ocupado');
