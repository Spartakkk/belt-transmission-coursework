import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
cur = conn.cursor()

# Создание таблицы (если не существует)
cur.execute('''
CREATE TABLE IF NOT EXISTS belts (
    id SERIAL PRIMARY KEY,
    belt_type TEXT NOT NULL CHECK (belt_type IN ('v_belt', 'poly_v_belt')),
    designation TEXT NOT NULL UNIQUE,
    sigma_0_allowed REAL NOT NULL,  -- Допустимое [σ0] из картинки, МПа
    q REAL NOT NULL,                -- Линейная плотность, кг/м
    s1 REAL,                        -- Площадь сечения S1 для клиновых, мм²
    s10 REAL                        -- Площадь сечения S10 для поликлиновых, мм²
)
''')

# Заполнение данными для клиновых ремней (из второй картинки + σ0 из первой + дополнительные)
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s1) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('v_belt', 'O', 1.35, 0.061, 47))
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s1) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('v_belt', 'A', 1.51, 0.105, 81))
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s1) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('v_belt', 'Б', 1.60, 0.178, 138))
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s1) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('v_belt', 'B', 1.69, 0.300, 230))
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s1) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('v_belt', 'УO', 1.78, 0.069, 56))
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s1) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('v_belt', 'УA', 1.82, 0.118, 93))
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s1) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('v_belt', 'УБ', 1.92, 0.196, 159))
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s1) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('v_belt', 'УB', 1.50, 0.363, 278))
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s1) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('v_belt', 'K', 1.69, 0.09, 60))
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s1) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('v_belt', 'Л', 1.78, 0.45, 330))

# Дополнительные значения для клиновых (на мой вкус, типичные из ГОСТ)
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s1) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('v_belt', 'E-5000', 1.86, 0.55, 450))
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s1) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('v_belt', 'F-6300', 1.96, 0.65, 600))

# Для поликлиновых (примеры + из картинки σ0 + дополнительные)
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s10) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('poly_v_belt', 'PJ-1200', 2.04, 0.025, 12.5))
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s10) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('poly_v_belt', 'PL-2000', 2.20, 0.080, 25.0))
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s10) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('poly_v_belt', 'PM-3500', 1.67, 0.200, 60.0))

# Дополнительные для поликлиновых
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s10) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('poly_v_belt', 'PH-800', 1.80, 0.015, 8.0))
cur.execute("INSERT INTO belts (belt_type, designation, sigma_0_allowed, q, s10) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            ('poly_v_belt', 'PK-1500', 1.90, 0.050, 18.0))

conn.commit()
cur.close()
conn.close()
print("Таблица belts создана и заполнена данными.")