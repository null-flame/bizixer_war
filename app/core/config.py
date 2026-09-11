from dotenv import load_dotenv
from app.models.enums import TType

T1_factory = 12
T2_factory = 125
T3_factory = 625
T4_factory = 2083

factory_costs = {
    TType.T1: 30,
    TType.T2: 500,
    TType.T3: 10000,
    TType.T4: 100000,
}
missile_costs = {
    TType.T1: 60,
    TType.T2: 625,
    TType.T3: 625*6,
    TType.T4: 2083*6,
}
factory_health = {
    TType.T1: 90,
    TType.T2: 1500,
    TType.T3: 15000,
    TType.T4: 150000,
}

missile_time = {
    TType.T1: 2,
    TType.T2: 15,
    TType.T3: 60,
    TType.T4: 120,
}

load_dotenv()

dbName = "db.db"
DbUrl = f"sqlite+aiosqlite:///{dbName}"

ALG = "HS256"
