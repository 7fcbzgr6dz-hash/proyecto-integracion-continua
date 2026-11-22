
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(30) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT IGNORE INTO productos (codigo, nombre, descripcion) VALUES
('SM', 'SM', 'Referencia de producto SM'),
('STS', 'STS', 'Referencia de producto STS'),
('HMCS', 'HMCS', 'Referencia de producto HMCS'),
('M-1720', 'M-1720', 'Referencia de producto M-1720'),
('M-1440', 'M-1440', 'Referencia de producto M-1440'),
('M-SWEET', 'M-SWEET', 'Referencia de producto M-SWEET');
