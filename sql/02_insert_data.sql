-- ============================================================
-- CHARGEMENT DES DONNEES (AVEC ANOMALIES INJECTEES)
-- ============================================================

-- 1. Table clients
INSERT INTO clients (client_id, nom, prenom, email, date_naissance, ville, code_postal, date_creation) VALUES
(1, 'DUPONT', 'Jean', 'jean.dupont@email.com', '1985-04-12', 'Niort', '79000', '2023-01-15'),
(2, 'MARTIN', 'Sophie', NULL, '1990-08-23', 'Paris', '75011', '2023-02-01'),
(3, 'DURAND', 'Pierre', 'pierre.durand_at_email.com', '1978-11-05', 'Bordeaux', '33000', '2023-03-10'),
(3, 'DURAND', 'Pierre', 'pierre.durand@email.com', '1978-11-05', 'Bordeaux', '33000', '2023-03-10'),
(4, 'MOREAU', 'Julie', 'julie.moreau@email.com', '2002-06-30', 'Niort', '79000', '2023-04-18');

-- 2. Table contrats
INSERT INTO contrats (contrat_id, client_id, type_contrat, date_debut, date_fin, prime_annuelle, statut) VALUES
(101, 1, 'AUTO', '2023-01-15', '2024-01-14', 650.00, 'ACTIF'),
(102, 2, 'MRH', '2023-02-01', '2024-01-31', -120.00, 'ACTIF'),
(103, 3, 'SANTE', '2023-03-10', '2022-03-09', 480.00, 'RESILIE'),
(104, 99, 'AUTO', '2023-04-18', '2024-04-17', 550.00, 'PENDING');

-- 3. Table sinistres
INSERT INTO sinistres (sinistre_id, contrat_id, date_sinistre, montant, statut) VALUES
(501, 101, '2023-05-14', 1200.00, 'CLOTURE'),
(502, 102, '2023-06-20', -350.00, 'EN_COURS'),
(503, 999, '2023-07-01', 500.00, 'EN_COURS');

-- 4. Table paiements
INSERT INTO paiements (paiement_id, contrat_id, date_paiement, montant, statut) VALUES
(901, 101, '2023-01-15', 650.00, 'VALIDE'),
(902, 102, '2023-02-01', 500.00, 'VALIDE'),
(903, 103, '2023-03-10', 480.00, 'ECHEC');