
from fastapi import FastAPI, HTTPException, status
from models.models import Monster, MonsterUpdate
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Коллекция монстров")

# Наша коллекция монстров
monsters_db = {
    1: {"name": "Дракоша Огненный", "type": "огненный", "power": 85, "hp": 500, "is_rare": True},
    2: {"name": "Искорка", "type": "огненный", "power": 45, "hp": 200, "is_rare": False},
    3: {"name": "Феникс", "type": "огненный", "power": 95, "hp": 300, "is_rare": True},
    4: {"name": "Аквамен", "type": "водный", "power": 70, "hp": 600, "is_rare": False},
    5: {"name": "Капелька", "type": "водный", "power": 25, "hp": 150, "is_rare": False},
    6: {"name": "Левиафан", "type": "водный", "power": 90, "hp": 800, "is_rare": True},
    7: {"name": "Горыныч", "type": "земляной", "power": 75, "hp": 700, "is_rare": True},
    8: {"name": "Камнеед", "type": "земляной", "power": 55, "hp": 450, "is_rare": False},
    9: {"name": "Пещерный Медведь", "type": "земляной", "power": 65, "hp": 550, "is_rare": False},
    10: {"name": "Ветрокрыл", "type": "воздушный", "power": 60, "hp": 350, "is_rare": False},
    11: {"name": "Грозовой Орёл", "type": "воздушный", "power": 88, "hp": 400, "is_rare": True},
    12: {"name": "Облачко", "type": "воздушный", "power": 15, "hp": 100, "is_rare": False},
    13: {"name": "Шокер", "type": "электрический", "power": 80, "hp": 300, "is_rare": False},
    14: {"name": "Молния", "type": "электрический", "power": 92, "hp": 250, "is_rare": True},
    15: {"name": "Снежок", "type": "ледяной", "power": 40, "hp": 350, "is_rare": False},
    # 16: {"name": "Айсберг", "type": "ледяной", "power": 78, "hp": 650, "is_rare": True}
}


 # {
 #    "name": "Айсберг",
 #    "type": "ледяной",
 #    "power": 78,
 #    "hp": 350,
 #    "is_rare": false
 #  }

monster_counter = 0


# --- GET запросы (получение данных) ---

@app.get("/")
async def root():
    """Главная страница"""
    return {
        "game": "Коллекция монстров",
        "total_monsters": len(monsters_db),
        "commands": {
            "GET /monsters": "Все монстры",
            "GET /monsters/{id}": "Монстр по ID",
            "POST /monsters": "Добавить монстра",
            "PUT /monsters/{id}": "Заменить монстра",
            "PATCH /monsters/{id}": "Обновить монстра",
            "DELETE /monsters/{id}": "Удалить монстра"
        }
    }




@app.get("/monsters", response_model=List[Monster])
async def get_all_monsters(
        type: Optional[str] = None,
        min_power: Optional[int] = None,
        rare_only: bool = False
):
    """
    Получить всех монстров с фильтрацией
    """
    result = monsters_db

    # Фильтр по типу
    if type:
        result = [m for m in result if m["type"] == type]

    # Фильтр по минимальной силе
    if min_power:
        result = [m for m in result if m["power"] >= min_power]

    # Только редкие
    if rare_only:
        result = [m for m in result if m["is_rare"]]


    return result


@app.get("/monsters/{monster_id}", response_model=Monster)
async def get_monster(monster_id: int):
    """
    Получить монстра по ID
    """
    if monster_id not in monsters_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Монстр с ID {monster_id} не найден"
        )
    return monsters_db[monster_id]


# --- POST запросы (создание) ---

@app.post("/monsters", status_code=status.HTTP_201_CREATED)
async def create_monster(monster: Monster):
    """
    Добавить нового монстра
    """
    global monsters_db

    # Находим следующий свободный ID
    if monsters_db:
        # Берем все существующие ID и находим максимальный
        next_id = max(monsters_db.keys()) + 1
    else:
        next_id = 1

    # Добавляем ID и время создания
    monster_dict = monster.model_dump()
    monster_dict["id"] = next_id
    monster_dict["created_at"] = datetime.now().isoformat()

    monsters_db[next_id] = monster_dict

    return {
        "message": f"Монстр {monster.name} добавлен!",
        "monster_id": next_id,
        "monster": monster_dict
    }


# --- PUT запросы (полное обновление) ---

@app.put("/monsters/{monster_id}")
async def replace_monster(monster_id: int, monster: Monster):
    """
    Полностью заменить монстра
    """
    if monster_id not in monsters_db:
        raise HTTPException(status_code=404, detail="Монстр не найден")

    # Полностью заменяем данные
    monster_dict = monster.dict()
    monster_dict["id"] = monster_id
    monster_dict["updated_at"] = datetime.now().isoformat()
    monster_dict["created_at"] = monsters_db[monster_id]["created_at"]

    monsters_db[monster_id] = monster_dict

    return {
        "message": f"Монстр {monster_id} обновлён полностью",
        "monster": monster_dict
    }


# --- PATCH запросы (частичное обновление) ---

@app.patch("/monsters/{monster_id}")
async def update_monster(monster_id: int, update: MonsterUpdate):
    """
    Частично обновить монстра
    """
    if monster_id not in monsters_db:
        raise HTTPException(status_code=404, detail="Монстр не найден")

    # Берём текущие данные
    current = monsters_db[monster_id]

    # Обновляем только те поля, которые переданы
    update_data = update.dict(exclude_unset=True)
    current.update(update_data)
    current["updated_at"] = datetime.now().isoformat()

    monsters_db[monster_id] = current

    return {
        "message": f"Монстр {monster_id} обновлён",
        "updated_fields": list(update_data.keys()),
        "monster": current
    }


# --- DELETE запросы (удаление) ---

@app.delete("/monsters/{monster_id}")
async def delete_monster(monster_id: int):
    """
    Удалить монстра
    """
    if monster_id not in monsters_db:
        raise HTTPException(status_code=404, detail="Монстр не найден")

    # Удаляем монстра
    deleted = monsters_db.pop(monster_id)

    return {
        "message": f"Монстр {deleted['name']} удалён",
        "deleted_id": monster_id
    }

