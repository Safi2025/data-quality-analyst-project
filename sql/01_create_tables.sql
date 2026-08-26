DROP TABLE IF EXISTS paiements CASCADE;
DROP TABLE IF EXISTS sinistres CASCADE;
DROP TABLE IF EXISTS contrats CASCADE;
DROP TABLE IF EXISTS clients CASCADE;

CREATE TABLE clients (
    client_id INT,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    email VARCHAR(100),
    date_naissance DATE,
    ville VARCHAR(50),
    code_postal VARCHAR(10),
    date_creation DATE
);

CREATE TABLE contrats (
    contrat_id INT,
    client_id INT,
    type_contrat VARCHAR(20),
    date_debut DATE,
    date_fin DATE,
    prime_annuelle NUMERIC(10,2),
    statut VARCHAR(20)
);

CREATE TABLE sinistres (
    sinistre_id INT,
    contrat_id INT,
    date_sinistre DATE,
    montant NUMERIC(10,2),
    statut VARCHAR(20)
);

CREATE TABLE paiements (
    paiement_id INT,
    contrat_id INT,
    date_paiement DATE,
    montant NUMERIC(10,2),
    statut VARCHAR(20)
);