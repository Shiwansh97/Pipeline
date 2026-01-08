from sqlalchemy import create_engine
from urllib.parse import quote_plus
from config import DB_CONFIG

def get_engine():
    password = quote_plus(DB_CONFIG["password"])

    url = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{password}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    return create_engine(url)
