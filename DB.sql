DROP DATABASE IF EXISTS ProyectoIS;
CREATE DATABASE ProyectoIS;
USE ProyectoIS;


-----Borrar por si existen
DROP TABLE IF EXISTS tarea;
DROP TABLE IF EXISTS asig_emp_clie;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS empleados;
DROP TABLE IF EXISTS tramite;
DROP TABLE IF EXISTS tipo_emp;
DROP TABLE IF EXISTS tipo_clie;

-----Crear tablas
USE ProyectoIS;

create table tipo_emp (
    tipo_emp_id INT(8), CONSTRAINT tipo_emp_id_pk PRIMARY KEY(tipo_emp_id),
    tipo_e VARCHAR (25),
    permisos VARCHAR (25)
);

create table tipo_clie (
    tipo_clie_id INT(8), CONSTRAINT tipo_clie_id_pk PRIMARY KEY(tipo_clie_id),
    tipo_c VARCHAR (25)
);

create table tramite (
    tramite_id INT(8), CONSTRAINT tramite_id_pk PRIMARY KEY(tramite_id),
    tipo VARCHAR (25),
    descrip VARCHAR (100),
    requisitos VARCHAR (25)
);

CREATE table personas (
    persona_id INT(8), CONSTRAINT persona_id_pk PRIMARY KEY (persona_id),
    nombre VARCHAR (50),
    ap_paterno VARCHAR (25),
    ap_materno VARCHAR (25),
    telefono VARCHAR(10),
    dir_num VARCHAR (4),
    calle VARCHAR (25),
    colonia VARCHAR (25),
    delegacion VARCHAR (25),
    cod_postal VARCHAR (5),
    municipio VARCHAR (25),
    estado VARCHAR (25),
    pais VARCHAR (25),
    correo VARCHAR (40),
    estado_civil VARCHAR (1) CHECK (estado_civil IN ('S','C','D','V')),
    fecha_nac date,
    rfc VARCHAR (13),
    curp VARCHAR (28),
    fecha_reg DATE DEFAULT SYSDATE()
);

create table clientes (
    cliente_id INT(8), CONSTRAINT cliente_id_pk PRIMARY KEY(cliente_id),
    CONSTRAINT cliente_id_fk FOREIGN KEY (cliente_id) REFERENCES personas(persona_id),
    tipo_clie_id INT(8), CONSTRAINT tipo_clie_id_fk FOREIGN KEY(tipo_clie_id) REFERENCES tipo_clie(tipo_clie_id)    
);

create table empleados (
    empleado_id INT(8), CONSTRAINT empleado_id_pk PRIMARY KEY(empleado_id),
    CONSTRAINT empleado_id_fk FOREIGN KEY (empleado_id) REFERENCES personas(persona_id),
    tipo_emp_id INT(8), CONSTRAINT tipo_emp_id_fk FOREIGN KEY(tipo_emp_id) REFERENCES tipo_emp(tipo_emp_id),
    permisos_add VARCHAR(20)
);

create table asig_emp_clie (
    cliente_id INT(8), CONSTRAINT asig_clie_fk FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id),
    empleado_id INT(8), CONSTRAINT asig_emp_fk FOREIGN KEY (empleado_id) REFERENCES empleados(empleado_id),
    CONSTRAINT asig_emp_clie_pk PRIMARY KEY (cliente_id,empleado_id)
);

create table tarea (
    tarea_id INT(8), CONSTRAINT tarea_id_pk PRIMARY KEY(tarea_id),
    id_creador INT(8), CONSTRAINT id_creador_fk FOREIGN KEY (id_creador) REFERENCES empleados(empleado_id),
    cliente_id INT(8),
    id_emp_asig INT(8),
    CONSTRAINT asig_fk FOREIGN KEY (cliente_id,id_emp_asig) REFERENCES asig_emp_clie(cliente_id,empleado_id),
    tramite_id INT(8), CONSTRAINT tramite_id_fk FOREIGN KEY (tramite_id) REFERENCES tramite(tramite_id),
    info_add VARCHAR (50),
    dir_archivo VARCHAR (100),
    estado VARCHAR (10) CHECK (estado IN ('pendiente', 'cancelado', 'completado')),
    costo INT (4),
    fecha_ini DATE DEFAULT SYSDATE(),
    fecha_lim DATE,
    fecha_fin DATE
);
