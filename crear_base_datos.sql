
-- Crear base de datos
CREATE DATABASE IF NOT EXISTS empresa_ventas_2025;
USE empresa_ventas_2025;

-- Tabla: regiones
CREATE TABLE IF NOT EXISTS regiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100)
);

-- Tabla: empleados (vendedores)
CREATE TABLE IF NOT EXISTS empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    region_id INT,
    FOREIGN KEY (region_id) REFERENCES regiones(id)
);

-- Tabla: clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100),
    fecha_registro DATE
);

-- Tabla: categorias
CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100)
);

-- Tabla: productos
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    categoria_id INT,
    precio DECIMAL(10,2),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- Tabla: ventas
CREATE TABLE IF NOT EXISTS ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    producto_id INT,
    empleado_id INT,
    cantidad INT,
    monto_total DECIMAL(10,2),
    fecha_venta DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (empleado_id) REFERENCES empleados(id)
);
