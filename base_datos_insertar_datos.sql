
-- Insertar regiones
INSERT INTO regiones (nombre) VALUES 
('Norte'), ('Centro'), ('Sur');

-- Insertar empleados
INSERT INTO empleados (nombre, region_id) VALUES 
('Ana Morales', 1),
('Luis Rojas', 2),
('Marcela Díaz', 3);

-- Insertar clientes
INSERT INTO clientes (nombre, correo, fecha_registro) VALUES
('Carlos Pérez', 'carlos@example.com', '2023-06-10'),
('Fernanda Soto', 'fernanda@example.com', '2024-03-15'),
('José Ramírez', 'jose@example.com', '2025-01-20');

-- Insertar categorías
INSERT INTO categorias (nombre) VALUES
('Ropa'), ('Calzado'), ('Accesorios');

-- Insertar productos
INSERT INTO productos (nombre, categoria_id, precio) VALUES
('Sweater lana', 1, 5840.30),
('Zapatillas deportivas', 2, 44990.00),
('Gorro invierno', 3, 5990.00),
('Polera básica', 1, 8990.00);

-- Insertar ventas (simuladas para 2024 y 2025)
INSERT INTO ventas (cliente_id, producto_id, empleado_id, cantidad, monto_total, fecha_venta) VALUES
-- Año 2024
(1, 1, 1, 3, 17520.90, '2024-01-15'),
(2, 2, 2, 1, 44990.00, '2024-03-22'),
(3, 3, 3, 2, 11980.00, '2024-06-11'),
(1, 4, 1, 1, 8990.00, '2024-09-05'),
(2, 1, 2, 1, 5840.30, '2024-12-01'),

-- Año 2025
(1, 1, 1, 5, 29201.50, '2025-01-10'),
(2, 2, 2, 1, 44990.00, '2025-02-17'),
(3, 1, 3, 2, 11680.60, '2025-03-03'),
(1, 4, 1, 1, 8990.00, '2025-04-20'),
(2, 1, 2, 3, 17520.90, '2025-05-12'),
(3, 3, 3, 1, 5990.00, '2025-06-01');
