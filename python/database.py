import os
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Récupération des variables d'environnement (avec valeurs par défaut pour votre Mac local)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "data_quality_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgrespassword")

# Construction dynamique de l'URL (compatible Mac local ET Docker Compose)
DATABASE_URL = os.getenv(
    "Base_URL", 
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=False)
Session_local = sessionmaker(bind=engine)

def execute_quality_check(query_str: str, check_name: str):
    """Exécute une requête SQL de contrôle, enregistre les logs dans data_quality_logs et renvoie le bilan des anomalies"""
    with engine.begin() as connection:  # engine.begin() gère l'ouverture et le COMMIT automatique
        result = connection.execute(text(query_str))
        anomalies = [dict(row) for row in result.mappings()]
        anomalies_count = len(anomalies)
        status = "FAIL" if anomalies_count > 0 else "PASS"
        details_str = f"{anomalies_count} anomalie(s) détectée(s)" if anomalies_count > 0 else "Aucune anomalie"

        # ---  HISTORISATION DES LOGS DANS POSTGRESQL ---
        insert_log_query = text("""
            INSERT INTO data_quality_logs (execution_date, check_name, status, anomalies_count, details)
            VALUES (:execution_date, :check_name, :status, :anomalies_count, :details)
        """)
        
        connection.execute(
            insert_log_query,
            {
                "execution_date": datetime.now(),
                "check_name": check_name,
                "status": status,
                "anomalies_count": anomalies_count,
                "details": details_str
            }
        )
        # -----------------------------------------------------------------

        return {
            "check_name": check_name,
            "status": status,
            "anomalies_count": anomalies_count,
            "details": anomalies
        }

if __name__ == "__main__":
    test_sql = """
        SELECT client_id, nom, prenom, email
        FROM clients
        WHERE email IS NULL OR email NOT LIKE '%@%.%';
    """
    
    res = execute_quality_check(test_sql, "Emails manquants ou invalides")
    print(f"[*] Contrôle : {res['check_name']}")
    print(f"[*] Statut : {res['status']}")
    print(f"[*] Anomalies trouvées : {res['anomalies_count']}")
    print(f"[*] Détails : {res['details']}")