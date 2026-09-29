from fastapi_offline import FastAPIOffline
from fastapi import HTTPException

from database import get_connection, init_db
from models import UserCreate, UserUpdate, UserResponse

app = FastAPIOffline(title="CRUD API with SQLite")


# ---------- راه‌اندازی اولیه ----------
@app.on_event("startup")
def startup():
    init_db()


# ---------- CREATE ----------
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        (user.name, user.age)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return {"id": user_id, "name": user.name, "age": user.age}


# ---------- READ (all) ----------
@app.get("/users", response_model=list[UserResponse])
def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age FROM users")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ---------- READ (one) ----------
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(row)


# ---------- UPDATE ----------
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    # بررسی وجود کاربر
    cursor.execute("SELECT id, name, age FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    # مقادیر جدید (اگر داده نشده باشند، مقدار قبلی حفظ می‌شود)
    new_name = user.name if user.name is not None else row["name"]
    new_age = user.age if user.age is not None else row["age"]

    cursor.execute(
        "UPDATE users SET name = ?, age = ? WHERE id = ?",
        (new_name, new_age, user_id)
    )
    conn.commit()
    conn.close()
    return {"id": user_id, "name": new_name, "age": new_age}


# ---------- DELETE ----------
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"User {user_id} deleted successfully"}
