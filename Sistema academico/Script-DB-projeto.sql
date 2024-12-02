-- Criação do esquema
CREATE SCHEMA IF NOT EXISTS ps;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS ps.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(256) NOT NULL,
    user_type VARCHAR(20) NOT NULL CHECK (user_type IN ('administrador', 'professor', 'aluno'))
);

-- Tabela de cursos
CREATE TABLE IF NOT EXISTS ps.cursos (
    id_cursos SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Tabela de notas
CREATE TABLE IF NOT EXISTS ps.notas (
    id SERIAL PRIMARY KEY,
    id_user INT NOT NULL REFERENCES ps.users (id) ON DELETE CASCADE,
    id_cursos INT NOT NULL REFERENCES ps.cursos (id_cursos) ON DELETE CASCADE,
    nota NUMERIC(5, 2) CHECK (nota >= 0 AND nota <= 10),
    UNIQUE (id_user, id_cursos)
);

-- Tabela de faltas
CREATE TABLE IF NOT EXISTS ps.faltas (
    id SERIAL PRIMARY KEY,
    id_user INT NOT NULL REFERENCES ps.users (id) ON DELETE CASCADE,
    id_cursos INT NOT NULL REFERENCES ps.cursos (id_cursos) ON DELETE CASCADE,
    date DATE NOT NULL,
    UNIQUE (id_user, id_cursos, date)
);