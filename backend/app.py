from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import math
import os
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()

app = FastAPI(title="Ремённая передача с БД — курсовая")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),      # в Docker переопределится
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "chain_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "secretpass"),  # в Docker будет secretpass
        cursor_factory=RealDictCursor
    )

# Получить список ремней для фронтенда
@app.get("/belts", response_model=List[dict])
def get_belts():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, belt_type, designation FROM belts ORDER BY belt_type, designation")
    belts = cur.fetchall()
    cur.close(); conn.close()
    return belts

# Получить параметры ремня по ID
@app.get("/belt/{belt_id}")
def get_belt_params(belt_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM belts WHERE id = %s", (belt_id,))
    belt = cur.fetchone()
    cur.close(); conn.close()
    if not belt:
        raise HTTPException(404, "Ремень не найден")
    return belt

# Входные данные (остальное вводишь сам)
class CalcInput(BaseModel):
    belt_id: int
    F: float                # Окружная сила, Н
    Z: float                # Число ремней/ручьёв
    fi: float = 1.0         # Коэффициент сцепления
    C1: float = 1.0         # Коэффициент угла обхвата
    C3: float = 1.0         # Коэффициент режима работы
    X: float = 0.15         # Коэффициент снижения
    v: float                # Скорость, м/с
    alpha1: float = 180.0   # Угол обхвата, °
    gamma1: float = 0.0     # Угол между ветвями, °

# Расчёт (использует данные из БД)
@app.post("/calculate")
def calculate(data: CalcInput):
    belt = get_belt_params(data.belt_id)

    sigma_0 = belt["sigma_0_allowed"]  # Допустимое [σ0] из БД
    q = belt["q"]                      # q из БД
    alpha_rad = math.radians(data.alpha1)
    gamma_rad_half = math.radians(data.gamma1 / 2)

    if belt["belt_type"] == "v_belt":
        S = belt["s1"]                 # S1 из БД
        working_sigma = data.F / (2 * data.fi * data.C1 * data.C3 * S * data.Z)  # Рабочее напряжение для проверки
        Q0 = (sigma_0 * S + (1 - data.X) * q * data.v**2) * data.Z
        R = 2 * sigma_0 * S * data.Z * math.sin(alpha_rad / 2)
        tg_theta = (data.F / (2 * sigma_0 * S * data.Z)) * math.tan(gamma_rad_half)

    else:  # poly_v_belt
        S = belt["s10"]                # S10 из БД
        working_sigma = 5 * data.F / (2 * data.fi * data.C1 * data.C3 * S * data.Z)  # Рабочее напряжение
        Q0 = (sigma_0 * S + (1 - data.X) * q * data.v**2) * data.Z * 10
        R = 2 * sigma_0 * (S / 10) * data.Z * math.sin(alpha_rad / 2)
        tg_theta = (5 * data.F / (2 * sigma_0 * S * data.Z)) * math.tan(gamma_rad_half)

    # Добавляем проверку: рабочее σ <= допустимое [σ0]
    status = "OK" if working_sigma <= sigma_0 else "Превышение напряжения!"

    return {
        "designation": belt["designation"],
        "belt_type": "Клиновой" if belt["belt_type"] == "v_belt" else "Поликлиновой",
        "working_sigma_MPa": round(working_sigma, 3),
        "sigma_0_allowed_MPa": round(sigma_0, 3),
        "status": status,
        "Q0_N": round(Q0, 1),
        "R_mm": round(R, 1),
        "tg_theta": round(tg_theta, 4),
        "theta_deg": round(math.degrees(math.atan(tg_theta)), 2)
    }

@app.get("/")
def root():
    return {"message": "Система с БД готова! Используй /docs"}