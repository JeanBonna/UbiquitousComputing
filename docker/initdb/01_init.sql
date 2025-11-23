-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial data
INSERT INTO users (name, email, username, password) VALUES
    ('Alice Ferreira', 'alice.ferreira@example.com', 'alicef', 'senha123'),
    ('Bruno Martins', 'bruno.martins@example.com', 'brunom', '12345678'),
    ('Carla Souza', 'carla.souza@example.com', 'carlas', 'minhasenha'),
    ('Diego Lima', 'diego.lima@example.com', 'diegol', 'abc12345'),
    ('Eduarda Rocha', 'eduarda.rocha@example.com', 'edurocha', 'senhaSegura!')
ON CONFLICT (email) DO NOTHING;

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);