-- Inserciones para la tabla 'patients'
INSERT INTO patients (Name, Mobile, Email, Address, Gender, BloodGroup) VALUES
('María González', '5551234567', 'maria.gonzalez@gmail.com', 'Calle 10 #123, Ciudad de México', 'Femenino', 'A+'),
('Juan Pérez', '5552345678', 'juanperez@hotmail.com', 'Av. Reforma 456, CDMX', 'Masculino', 'O+'),
('Laura Martínez', '5553456789', 'lauramartinez@yahoo.com', 'Calle Lago Azul 89, Monterrey', 'Femenino', 'B+'),
('Carlos Ramírez', '5554567890', 'carlos.ramirez@gmail.com', 'Calle Real 12, Guadalajara', 'Masculino', 'AB-'),
('Ana Torres', '5555678901', 'ana.torres@gmail.com', 'Col. Jardines, Puebla', 'Femenino', 'O-'),
('Luis Hernández', '5556789012', 'luis.hdz@outlook.com', 'Calle Sol 21, Mérida', 'Masculino', 'A-'),
('Sofía Rojas', '5557890123', 'sofiarojas@gmail.com', 'Blvd. Central 77, Cancún', 'Femenino', 'AB+'),
('Diego Vargas', '5558901234', 'diego.vg@live.com', 'Centro, León', 'Masculino', 'B-'),
('Isabel López', '5559012345', 'isalopez@gmail.com', 'Calle Luna 33, Querétaro', 'Femenino', 'A+'),
('Miguel Ortega', '5550123456', 'miguel.ortega@correo.com', 'Col. Roma, CDMX', 'Masculino', 'O+');

-- Inserciones para la tabla 'services'
INSERT INTO services (Name, Description, Price) VALUES
('Consulta General', 'Evaluación médica general para diagnóstico y tratamiento básico.', 25),
('Lectura de radiografías', 'Informe médico detallado sobre imágenes de rayos X.', 22.00),
('Electroencefalograma (EEG)', 'Estudio de la actividad eléctrica cerebral mediante electrodos.', 50.00),
('Electrocardiograma (ECG)', 'Evaluación gráfica de la actividad eléctrica del corazón.', 30.00),
('Toma de muestra de sangre', 'Extracción de sangre para análisis clínicos de laboratorio.', 12.00),
('Curación de heridas', 'Atención médica para desinfección, limpieza y vendaje de heridas.', 20.00),
('Inyecciones y aplicación de medicamentos', 'Administración intramuscular o intravenosa de fármacos.', 8.00),
('Nebulización', 'Tratamiento respiratorio con medicamentos vaporizados.', 15.00),
('Control de signos vitales', 'Medición de presión arterial, pulso, temperatura y saturación.', 5.00),
('Prueba rápida de glucosa', 'Medición instantánea del nivel de azúcar en sangre.', 7.00);

-- Inserciones para la tabla 'slots'
INSERT INTO slots (Time, Status) VALUES
('08:00 - 09:00', 'Disponible'),
('09:00 - 10:00', 'Ocupado'),
('10:00 - 11:00', 'Disponible'),
('11:00 - 12:00', 'Disponible'),
('12:00 - 13:00', 'Ocupado');
