import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def initialize_db():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
    )
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS public.problem (
                id_problem VARCHAR PRIMARY KEY,
                name VARCHAR NOT NULL,
                contestId INTEGER NOT NULL,
                index VARCHAR NOT NULL,
                url TEXT,
                rating INTEGER,
                tags TEXT[],
                solvedCount INTEGER DEFAULT 0
            );
        """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS public.problem_tags (
                id_problem VARCHAR NOT NULL,
                tag VARCHAR NOT NULL,
                FOREIGN KEY (id_problem) REFERENCES public.problem (id_problem)
            );
        """
        )

    conn.close()


if __name__ == "__main__":
    initialize_db()
