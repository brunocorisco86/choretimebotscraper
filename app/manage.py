import argparse
from datetime import datetime
from database import init_db, register_aviary, Batch, Aviary
from config import DB_PATH

sqlite_uri = f"sqlite:///{DB_PATH}"
SessionFactory = init_db(sqlite_uri)

def add_aviary(number, url):
    register_aviary(SessionFactory, number, url)
    print(f"Aviário {number} registrado com sucesso!")

def create_batch(aviary_id, lodging_date, initial_count):
    session = SessionFactory()
    try:
        date_obj = datetime.strptime(lodging_date, "%Y-%m-%d")
        batch = Batch(aviary_id=aviary_id, lodging_date=date_obj, initial_count=initial_count)
        session.add(batch)
        session.commit()
        print(f"Lote para o aviário {aviary_id} criado com sucesso!")
    except Exception as e:
        session.rollback()
        print(f"Erro ao criar lote: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerenciador do ChoreScraper")
    subparsers = parser.add_subparsers(dest="command")

    # Comando para adicionar aviário
    parser_aviary = subparsers.add_parser("add-aviary")
    parser_aviary.add_argument("number", help="Número do aviário")
    parser_aviary.add_argument("url", help="URL do aviário")

    # Comando para criar lote
    parser_batch = subparsers.add_parser("create-batch")
    parser_batch.add_argument("aviary_id", help="ID do aviário")
    parser_batch.add_argument("lodging_date", help="Data de alojamento (AAAA-MM-DD)")
    parser_batch.add_argument("initial_count", type=int, help="Quantidade inicial de aves")

    args = parser.parse_args()

    if args.command == "add-aviary":
        add_aviary(args.number, args.url)
    elif args.command == "create-batch":
        create_batch(args.aviary_id, args.lodging_date, args.initial_count)
    else:
        parser.print_help()
