use project_ing;
SET SQL_SAFE_UPDATES = 0;
select * from auth_permission;

-- permisos cuenta de usuario
UPDATE auth_permission SET name="Crear cuenta de usuario" WHERE codename= "add_user";
UPDATE auth_permission SET codename= "dev_crear_usuario" WHERE codename= "add_user";
UPDATE auth_permission SET name="Ver cuentas de usuario" WHERE codename= "view_user";
UPDATE auth_permission SET codename= "dev_ver_usuario" WHERE codename= "view_user";
UPDATE auth_permission SET name="Editar cuenta de usuario" WHERE codename= "change_user";
UPDATE auth_permission SET codename= "dev_editar_usuario" WHERE codename= "change_user";
UPDATE auth_permission SET name="Eliminar cuenta de usuario" WHERE codename= "delete_user";
UPDATE auth_permission SET codename= "dev_eliminar_usuario" WHERE codename= "delete_user";

-- eliminar permisos de modelo persona
delete from auth_permission where content_type_id=11;

-- permisos empleados
INSERT INTO auth_permission (name,content_type_id,codename) VALUES("Crear empleados",11,"dev_crear_empleados");
INSERT INTO auth_permission (name,content_type_id,codename) VALUES("Ver empleados",11,"dev_ver_empleados");
INSERT INTO auth_permission (name,content_type_id,codename) VALUES("Editar empleados",11,"dev_editar_empleados");
INSERT INTO auth_permission (name,content_type_id,codename) VALUES("Eliminar empleados",11,"dev_eliminar_empleados");

-- permisos cliente
INSERT INTO auth_permission (name,content_type_id,codename) VALUES("Crear clientes",11,"dev_crear_clientes");
INSERT INTO auth_permission (name,content_type_id,codename) VALUES("Ver clientes",11,"dev_ver_clientes");
INSERT INTO auth_permission (name,content_type_id,codename) VALUES("Editar clientes",11,"dev_editar_clientes");
INSERT INTO auth_permission (name,content_type_id,codename) VALUES("Eliminar clientes",11,"dev_eliminar_clientes");

-- permisos Directorio
UPDATE auth_permission SET name="Crear directorio" WHERE codename= "add_directorio";

-- permisos Cuentas
UPDATE auth_permission SET name="Crear cuentas" WHERE codename= "add_cuentas";
UPDATE auth_permission SET codename= "dev_crear_cuentas" WHERE codename= "add_cuentas";
UPDATE auth_permission SET name="Ver cuentas" WHERE codename= "view_cuentas";
UPDATE auth_permission SET codename= "dev_ver_cuentas" WHERE codename= "view_cuentas";
UPDATE auth_permission SET name="Editar cuentas" WHERE codename= "change_cuentas";
UPDATE auth_permission SET codename= "dev_editar_cuentas" WHERE codename= "change_cuentas";
UPDATE auth_permission SET name="Eliminar cuentas" WHERE codename= "delete_cuentas";
UPDATE auth_permission SET codename= "dev_eliminar_cuentas" WHERE codename= "delete_cuentas";

-- permisos tipo cliente
UPDATE auth_permission SET name="Crear Tipo de cliente" WHERE codename= "add_tipo_usuarios";
UPDATE auth_permission SET codename= "dev_crear_tipo_cliente" WHERE codename= "add_tipo_usuarios";
UPDATE auth_permission SET name="Ver Tipo de cliente" WHERE codename= "view_tipo_usuarios";
UPDATE auth_permission SET codename= "dev_ver_tipo_cliente" WHERE codename= "view_tipo_usuarios";
UPDATE auth_permission SET name="Editar Tipo de cliente" WHERE codename= "change_tipo_usuarios";
UPDATE auth_permission SET codename= "dev_editar_tipo_cliente" WHERE codename= "change_tipo_usuarios";
UPDATE auth_permission SET name="Eliminar Tipo de cliente" WHERE codename= "delete_tipo_usuarios";
UPDATE auth_permission SET codename= "dev_eliminar_tipo_cliente" WHERE codename= "delete_tipo_usuarios";

-- crear permiso para ver contraseña de cuentas
INSERT INTO auth_permission (name,content_type_id,codename) VALUES("Ver contraseña",11,"auth_ver_password");

-- creacion de roles por defecto (tipo de usuario que usa Django)
INSERT INTO auth_group(name) VALUES("Administrador");

-- creacion de tipo de usuario por defecto
INSERT INTO tipo_usuarios(descr) VALUES("Empleado");
INSERT INTO tipo_usuarios(descr) VALUES("Fisica");
INSERT INTO tipo_usuarios(descr) VALUES("Moral");


SET SQL_SAFE_UPDATES = 1;