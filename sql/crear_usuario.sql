-- Crea la tabla de usuarios
CREATE TABLE USUARIOS (
  NOMBRE VARCHAR(100) NOT NULL,
  CONTRASENA VARCHAR(255) NOT NULL,
  CORREO VARCHAR(255) NOT NULL,
  NUMERO_DOCUMENTO VARCHAR(10) NOT NULL,
  DONANTE BOOLEAN NOT NULL,
  ADMIN BOOLEAN NOT NULL,
  ENFERMERO BOOLEAN NOT NULL,
  TIPO_DE_SANGRE VARCHAR(3) NOT NULL CHECK (TIPO_DE_SANGRE IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
  TIPO_DOCUMENTO VARCHAR(50) NOT NULL CHECK (TIPO_DOCUMENTO IN ('Cedula de Ciudadania', 'Cedula de Extranjeria')),
  PERFIL_IMAGEN_LINK TEXT NOT NULL,
  PERFIL_IMAGEN_DELETEHASH TEXT,
  PRIMARY KEY (NUMERO_DOCUMENTO, TIPO_DOCUMENTO)
);