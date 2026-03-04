import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import AviaryReading, Base
from config import DB_PATH, PG_URI

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def transfer_data():
    """
    Transfere dados do SQLite local para o PostgreSQL externo.
    Executa a cada 4 horas conforme sua premissa.
    """
    if not PG_URI:
        logging.warning("PG_URI não configurada no .env. Abortando transferência.")
        return

    sqlite_uri = f"sqlite:///{DB_PATH}"
    
    # Motores de conexão
    sqlite_engine = create_engine(sqlite_uri)
    pg_engine = create_engine(PG_URI)

    # Garante que a estrutura da tabela exista no PostgreSQL
    Base.metadata.create_all(pg_engine)

    # Fábricas de sessão
    SqliteSession = sessionmaker(bind=sqlite_engine)
    PgSession = sessionmaker(bind=pg_engine)

    s_session = SqliteSession()
    p_session = PgSession()

    try:
        logging.info("Iniciando transferência SQLite -> PostgreSQL...")
        
        # Busca todas as leituras do SQLite
        readings = s_session.query(AviaryReading).all()
        total_found = len(readings)
        transferred_count = 0

        for r in readings:
            # Verifica se o registro já existe no Postgres (ID composto por aviary_id + timestamp)
            exists = p_session.query(AviaryReading).filter_by(
                aviary_id=r.aviary_id, 
                timestamp=r.timestamp
            ).first()

            if not exists:
                # Cria novo objeto para o Postgres (desvinculado da sessão SQLite)
                new_reading = AviaryReading(
                    aviary_id=r.aviary_id,
                    timestamp=r.timestamp,
                    temperature=r.temperature,
                    humidity=r.humidity,
                    ammonia=r.ammonia,
                    age=r.age,
                    water_consumption=r.water_consumption,
                    static_pressure=r.static_pressure
                )
                p_session.add(new_reading)
                transferred_count += 1
                
                # Commit em lotes de 100 para performance
                if transferred_count % 100 == 0:
                    p_session.commit()

        p_session.commit()
        logging.info(f"Sucesso! {transferred_count} novos registros transferidos de {total_found} encontrados.")

        # Opcional: Limpar SQLite após transferência bem-sucedida
        # s_session.query(AviaryReading).delete()
        # s_session.commit()
        # logging.info("Dados locais limpos do SQLite.")

    except Exception as e:
        p_session.rollback()
        logging.error(f"Erro durante a transferência: {e}")
        raise e
    finally:
        s_session.close()
        p_session.close()

if __name__ == "__main__":
    transfer_data()
