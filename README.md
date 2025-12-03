# Курсовая работа  
**Автоматизированный проверочный расчёт клиновых и поликлиновых ремённых передач**

## Цель работы
Разработать программную систему для автоматизации проверочного расчёта на усталостную прочность клиновых и поликлиновых ремённых передач с использованием СУБД PostgreSQL.

## Используемые технологии
- **Backend**: Python 3.9+ + FastAPI + Uvicorn
- **База данных**: PostgreSQL 13+
- **Frontend**: чистый HTML + CSS + JavaScript (без фреймворков)
- **Инструменты разработки**: VS Code, DBeaver, Git

## Структура проекта
```
belt-transmission-coursework/
├── backend/
│   ├── app.py              # Основной сервер FastAPI
│   ├── init_db.py          # Создание и заполнение таблицы belts
│   ├── .env                # Настройки подключения к БД
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
├── .gitignore
└── README.md
```
## Установка и запуск

### Вариант 1 — локально
### Что должно быть установлено:
1. Python 3.9–3.12
2. PostgreSQL 13+
3. Git
4. (Рекомендуется) VS Code + расширения: Python, Live Server

### Пошаговая инструкция:
```
# 1. Клонировать репозиторий
git clone https://github.com/ТВОЙ_НИК/belt-transmission-coursework.git
cd belt-transmission-coursework

# 2. Создать и активировать виртуальное окружение
cd backend
python -m venv .venv
source .venv/Scripts/activate    # Windows Git Bash
# .venv\Scripts\activate.bat     # Windows CMD
# .venv/bin/activate             # Linux/Mac

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Настроить подключение к PostgreSQL
# Скопируй .env.example → .env и укажи свои данные
cp .env.example .env
# Открой .env и заполни:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=chain_db
DB_USER=postgres
DB_PASSWORD=твой_пароль

# 5. Создать базу и заполнить справочник ремней
python init_db.py

# 6. Запустить сервер
uvicorn app:app --reload

# 7. Открыть frontend/index.html через Live Server (или двойным кликом)
```

### Вариант 2 — через Docker
```
# 1. Склонировать проект
git clone https://github.com/ТВОЙ_НИК/chain-transmission-project.git
cd chain-transmission-project

# 2. Запустить всё одной командой
docker-compose up --build

# 3. Открыть frontend/index.html через Live Server 
```