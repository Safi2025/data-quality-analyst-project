-- ============================================================
-- ANALYSES METIER ET KPIS PORTEFEUILLE ASSURANCE
-- ============================================================

-- 1. Chiffre d'affaires annuel (Total des primes actives)
SELECT 
    COUNT(contrat_id) AS total_contrats_actifs,
    SUM(prime_annuelle) AS ca_total_annuel,
    ROUND(AVG(prime_annuelle), 2) AS prime_moyenne
FROM contrats
WHERE statut = 'ACTIF' AND prime_annuelle > 0;

-- 2. Répartition du portefeuille par type de contrat
SELECT 
    type_contrat,
    COUNT(contrat_id) AS nombre_contrats,
    SUM(prime_annuelle) AS ca_par_type,
    ROUND(AVG(prime_annuelle), 2) AS prime_moyenne
FROM contrats
WHERE prime_annuelle > 0
GROUP BY type_contrat
ORDER BY ca_par_type DESC;

-- 3. Ratio de Sinistralité (S/P) par contrat
-- S/P = (Total Sinistres / Prime Annuelle) * 100
SELECT 
    c.contrat_id,
    c.type_contrat,
    c.prime_annuelle,
    COALESCE(SUM(s.montant), 0) AS total_sinistres,
    ROUND((COALESCE(SUM(s.montant), 0) / c.prime_annuelle) * 100, 2) AS ratio_sp_pourcent
FROM contrats c
LEFT JOIN sinistres s ON c.contrat_id = s.contrat_id AND s.montant > 0
WHERE c.prime_annuelle > 0
GROUP BY c.contrat_id, c.type_contrat, c.prime_annuelle
ORDER BY ratio_sp_pourcent DESC;

-- 4. Taux de recouvrement des paiements
SELECT 
    c.contrat_id,
    c.prime_annuelle,
    COALESCE(SUM(p.montant), 0) AS total_paye,
    c.prime_annuelle - COALESCE(SUM(p.montant), 0) AS reste_a_recouvrer
FROM contrats c
LEFT JOIN paiements p ON c.contrat_id = p.contrat_id AND p.statut = 'VALIDE'
WHERE c.prime_annuelle > 0
GROUP BY c.contrat_id, c.prime_annuelle;