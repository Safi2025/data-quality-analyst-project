import pandas as pd
from database import engine
from sqlalchemy import text

def generate_business_kpis():
    print("\n" + "="*60)
    print(" GENERATION DES KPIS BUSINESS PORTEFEUILLE ")
    print("="*60)
    
    with engine.connect() as connection:
        # KPI 1 : CA par type de contrat
        query_ca = text("""
            SELECT 
                type_contrat,
                COUNT(contrat_id) AS nombre_contrats,
                SUM(prime_annuelle) AS ca_par_type,
                ROUND(AVG(prime_annuelle), 2) AS prime_moyenne
            FROM contrats
            WHERE prime_annuelle > 0
            GROUP BY type_contrat;
        """)
        df_ca = pd.read_sql(query_ca, connection)
        print("\n--- CA par Type de Contrat ---")
        print(df_ca)

        # KPI 2 : Ratio de Sinistralité (S/P)
        query_sp = text("""
            SELECT 
                c.contrat_id,
                c.type_contrat,
                c.prime_annuelle,
                COALESCE(SUM(s.montant), 0) AS total_sinistres,
                ROUND((COALESCE(SUM(s.montant), 0) / c.prime_annuelle) * 100, 2) AS ratio_sp_pourcent
            FROM contrats c
            LEFT JOIN sinistres s ON c.contrat_id = s.contrat_id AND s.montant > 0
            WHERE c.prime_annuelle > 0
            GROUP BY c.contrat_id, c.type_contrat, c.prime_annuelle;
        """)
        df_sp = pd.read_sql(query_sp, connection)
        print("\n--- Ratio S/P par Contrat ---")
        print(df_sp)
        
        # Exporter les résultats en CSV
        df_ca.to_csv("reports/kpi_ca_par_type.csv", index=False)
        df_sp.to_csv("reports/kpi_ratio_sp.csv", index=False)
        print("\n[+] Reports 'reports/kpi_ca_par_type.csv' et 'reports/kpi_ratio_sp.csv' exportés avec succès !")

if __name__ == "__main__":
    generate_business_kpis()