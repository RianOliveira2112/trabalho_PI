
CREATE DATABASE IF NOT EXISTS petshop_pi
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE petshop_pi;

DROP TABLE IF EXISTS pets;
DROP TABLE IF EXISTS tutores;

CREATE TABLE tutores (
    id       INT          NOT NULL AUTO_INCREMENT,
    nome     VARCHAR(100) NOT NULL,
    email    VARCHAR(100) NOT NULL,
    telefone VARCHAR(20)  NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_tutores_email (email)
);

CREATE TABLE pets (
    id              INT          NOT NULL AUTO_INCREMENT,
    nome            VARCHAR(100) NOT NULL,
    especie         VARCHAR(50)  NOT NULL,
    raca            VARCHAR(50)  NULL,
    data_nascimento DATE         NULL,
    tutor_id        INT          NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_pets_tutor
        FOREIGN KEY (tutor_id) REFERENCES tutores (id)
);

INSERT INTO tutores (nome, email, telefone) VALUES
    ('Ana Souza',    'ana@email.com',    '(47) 99999-1111'),
    ('Carlos Lima',  'carlos@email.com', '(47) 99999-2222'),
    ('Marina Costa', 'marina@email.com', NULL);

INSERT INTO pets (nome, especie, raca, data_nascimento, tutor_id) VALUES
    ('Thor',  'Cachorro', 'Labrador',    '2020-03-15', 1),
    ('Mel',   'Gato',     'Siamês',      '2021-07-02', 1),
    ('Bob',   'Cachorro', 'Vira-lata',   '2019-11-20', 2),
    ('Nina',  'Coelho',   NULL,          '2022-01-10', 3);