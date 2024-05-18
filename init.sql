-- Crear la base de datos mantenimiento_db
CREATE DATABASE mantenimiento_db;

-- Crear un usuario y asignarle privilegios
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE mantenimiento_db TO postgres;
