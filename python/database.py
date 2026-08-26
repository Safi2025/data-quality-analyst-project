from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os


#Configuration de la connexion avec PostgreSQL locale 
Base_URL= os.getenv("Base_URL", "postgresql://localhost:5432/data_quality_db")
engine = create_engine(Base_URL, echo=False)
Session_local = sessionmaker(bind=engine)

def execute_quality_check (query_str: str,check_name:str):
    """Exécute une requête SQL de contrôle et renvoie le bilan des anolies"""
    with engine.connect() as connection:
        result = connection.execute(text(query_str))
        #rows = result.fetchall()
        #keys = result.keys()

        #anomalies = [dict(zip(keys,rows)) for row in rows]
        anomalies = [dict(row) for row in result.mappings()]
        status = "FAIL" if len (anomalies) > 0 else "PASS"

        return {
            "check_name" : check_name,
            "status" : status,
            "anomalies_count" : len(anomalies),
            "details" : anomalies
        }
if __name__ == "__main__":
    #Test simple : Détéction des emails manquants ou invalides
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