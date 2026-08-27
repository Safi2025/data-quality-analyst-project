-- ============================================================
-- CONTROLES DATA QUALITY - PORTEFEUILLE ASSURANCE
-- ============================================================

-- 1. Complétude : Emails manquants ou invalides
-- REGLE : L'email doit être renseigné et contenir un format valide (@ et .)
SELECT client_id, nom, prenom, email
FROM clients
WHERE email IS NULL OR email NOT LIKE '%@%.%';

-- 2. Unicité : Doublons sur les identifiants clients
-- REGLE : Chaque client_id doit être unique
SELECT client_id, COUNT(*) AS occurences
FROM clients
GROUP BY client_id
HAVING COUNT(*) > 1;

-- 3. Intégrité référentielle : Clés orphelines sur les contrats
-- REGLE : Tout contrat doit être rattaché à un client existant
SELECT c.contrat_id, c.client_id, c.type_contrat
FROM contrats c
LEFT JOIN clients cl ON c.client_id = cl.client_id
WHERE cl.client_id IS NULL;

-- 4. Validité : Prime annuelle négative ou nulle
-- REGLE : La prime annuelle d'un contrat doit être strictement positive
SELECT contrat_id, client_id, prime_annuelle
FROM contrats
WHERE prime_annuelle <= 0;

-- 5. Cohérence temporelle : Date de fin antérieure à la date de début
-- REGLE : date_fin >= date_debut
SELECT contrat_id, date_debut, date_fin
FROM contrats
WHERE date_fin < date_debut;

-- 6. Règle Métier : Paiement supérieur à la prime annuelle du contrat
-- REGLE : Le montant d'un paiement individuel ne peut dépasser la prime du contrat
SELECT p.paiement_id, p.contrat_id, p.montant AS montant_paiement, c.prime_annuelle
FROM paiements p
JOIN contrats c ON p.contrat_id = c.contrat_id
WHERE p.montant > c.prime_annuelle; -- Controles data quality prets pour revue
