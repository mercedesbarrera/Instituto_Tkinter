# Este archivo contiene las consultas SQL para crear las tablas y realizar operaciones básicas en la base de datos.
CREATE_TABLE_ADMIN = """
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
"""

CREATE_TABLE_ALUMNOS = """
CREATE TABLE IF NOT EXISTS alumnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    dni TEXT UNIQUE NOT NULL,
    fecha_nacimiento TEXT
);
"""

CREATE_TABLE_PROFESORES = """
CREATE TABLE IF NOT EXISTS profesores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    dni TEXT UNIQUE NOT NULL,
    departamento TEXT
);
"""

CREATE_TABLE_AULAS = """
CREATE TABLE IF NOT EXISTS aulas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT,
    capacidad INTEGER
);
"""

CREATE_TABLE_ASIGNATURAS = """
CREATE TABLE IF NOT EXISTS asignaturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    departamento TEXT
);
"""

CREATE_TABLE_MATERIAL = """
CREATE TABLE IF NOT EXISTS materiales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    cantidad INTEGER,
    aula_id INTEGER,
    FOREIGN KEY(aula_id) REFERENCES aulas(id)
);
"""

CREATE_TABLE_DIRECCION= """
CREATE TABLE IF NOT EXISTS direccion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profesor_id INTEGER UNIQUE NOT NULL,
    cargo TEXT NOT NULL,
    FOREIGN KEY (profesor_id) REFERENCES profesores (id)
);
"""

CREATE_TABLE_CLASES="""
CREATE TABLE IF NOT EXISTS clases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profesor_id INTEGER NOT NULL,
    asignatura_id INTEGER NOT NULL,
    aula_id INTEGER NOT NULL,
    anio_academico TEXT NOT NULL,
    
    
    FOREIGN KEY (profesor_id) REFERENCES profesores(id),
    FOREIGN KEY (asignatura_id) REFERENCES asignaturas(id),
    FOREIGN KEY (aula_id) REFERENCES aulas(id)
);
"""
CREATE_TABLE_MATRICULAS="""
CREATE TABLE IF NOT EXISTS matriculas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumno_id INTEGER NOT NULL,
    clase_id INTEGER NOT NULL,
    anio TEXT NOT NULL,
    
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id),
    FOREIGN KEY (clase_id)  REFERENCES clase(id),
    
    UNIQUE(alumno_id,clase_id,anio)
);
"""

CREATE_TABLE_CONVOCATORIAS="""
CREATE TABLE IF NOT EXISTS convocatorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);
"""

CREATE_TABLE_CALIFICACIONES = """
CREATE TABLE IF NOT EXISTS calificaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula_id INTEGER NOT NULL,
    convocatoria_id INTEGER NOT NULL,
    nota REAL NOT NULL CHECK(nota BETWEEN 0 AND 10),

    FOREIGN KEY (matricula_id) REFERENCES matriculas(id),
    FOREIGN KEY (convocatoria_id) REFERENCES convocatorias(id),

    UNIQUE(matricula_id, convocatoria_id)
);
"""



#-----------ADMINISTRADORES----------
INSERT_ADMIN='''
INSERT INTO admin (usuario, password)
VALUES (?,?);
'''
#-----------CONVOCATORIAS------------
INSERT_CONVOCATORIAS = """
INSERT OR IGNORE INTO convocatorias (nombre)
VALUES
('1ª Evaluación'),
('2ª Evaluación'),
('Final'),
('Extraordinaria');
"""
#-----------LOGIN ADMINISTRADOR----------
SELECT_ADMIN_LOGIN='''
SELECT id, usuario
from admin
WHERE usuario = ? AND password=?;
'''

