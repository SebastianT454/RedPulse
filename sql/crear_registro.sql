-- Crea la tabla registros
CREATE TABLE REGISTRO (
  ID SERIAL PRIMARY KEY,
  TIPO_REGISTRO VARCHAR(20) NOT NULL CHECK (TIPO_REGISTRO IN ('Donacion', 'Solicitud')),
  TIPO_SANGRE VARCHAR(3) NOT NULL CHECK (TIPO_SANGRE IN ('AB+', 'AB-', 'A+', 'A-', 'B+', 'B-', 'O+', 'O-')),
  CANTIDAD FLOAT NOT NULL,
  RAZON TEXT NOT NULL,
  COMENTARIOS TEXT,
  DOCUMENTO_USUARIO VARCHAR(10) NOT NULL,
  PRIORIDAD INT NOT NULL
);
