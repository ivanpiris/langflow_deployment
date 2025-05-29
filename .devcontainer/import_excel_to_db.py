import time
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

def excel_to_postgres(
    excel_path: str,
    sheet_name: str,
    table_name: str,
    db_user: str = "myuser",
    db_password: str = "mypassword",
    db_host: str = "db",
    db_port: int = 5432,
    db_name: str = "mydatabase"
):
    # 1. Esperar a que la DB esté lista
    url = (
        f"postgresql+psycopg2://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )
    while True:
        try:
            engine = create_engine(url)
            conn = engine.connect()
            conn.close()
            print("✅ Base de datos disponible. Continuando con la importación...")
            break
        except OperationalError:
            print("⏳ Esperando a que PostgreSQL esté listo...")
            time.sleep(1)

    # 2. Leer Excel
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    print(f"Leídos {len(df)} registros de {excel_path} (hoja '{sheet_name}').")

    # 3. Volcar DataFrame a PostgreSQL
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )
    print(f"✅ Datos volcados en la tabla '{table_name}'.")

if __name__ == "__main__":
    excel_to_postgres(
        excel_path="datos.xlsx",
        sheet_name="datos_fabricacion",
        table_name="mi_tabla"
    )
