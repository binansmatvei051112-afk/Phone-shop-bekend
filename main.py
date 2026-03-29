import fastapi
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database import get_db_connection
from models import Item, Cases

print("Запуск сервера...")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/items")
def read_items(search: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if search:
        cursor.execute("SELECT * FROM Items WHERE Name LIKE ?", (f"%{search}%",))
    else:
        cursor.execute("SELECT * FROM Items")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row["Id"], "name": row["Name"], "price": row["Price"]} for row in rows]

@app.get("/items/{item_id}")
def read_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Items WHERE Id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return JSONResponse(status_code=404, content={"message": "Товар не найден"})
    return {"id": row["Id"], "name": row["Name"], "price": row["Price"]}

@app.post("/items")
def create_item(item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Items (Name, Price) VALUES (?, ?)", (item.name, item.price))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Items WHERE Id = ?", (item_id, ))
    if cursor.fetchone() is None:
        conn.close()
        return JSONResponse(status_code=404, content={"message": "Товар не найден"})
    cursor.execute("UPDATE Items SET Name = ?, Price = ? WHERE Id = ?", (item.name, item.price, item_id))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Items WHERE Id = ?", (item_id,))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.get("/cases")
def read_cases():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cases")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row["Id"], "name": row["Name"], "material": row["Material"], "price": row["Price"], "items_id": row["Items_id"]} for row in rows]

@app.get("/cases/{case_id}")
def read_case(case_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cases WHERE Id = ?", (case_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return JSONResponse(status_code=404, content={"message": "Чехол не найден"})
    return {"id": row["Id"], "name": row["Name"], "material": row["Material"], "price": row["Price"], "items_id": row["Items_id"]}


@app.get("/items/cases/{items_id}")
def get_cases_for_item(items_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cases WHERE Items_id = ?", (items_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row["Id"], "name": row["Name"], "material": row["Material"], "price": row["Price"], "items_id": row["Items_id"]} for row in rows]

@app.post("/cases")
def create_case(case: Cases):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Cases (Name, Material, Price, Items_id) VALUES (?, ?, ?, ?)", 
                   (case.name, case.material, case.price, case.Items_id))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.put("/cases/{case_id}")
def update_case(case_id: int, case: Cases):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cases WHERE Id = ?", (case_id,))
    if cursor.fetchone() is None:
        conn.close()
        return JSONResponse(status_code=404, content={"message": "Чехол не найден"})
    
    cursor.execute("UPDATE Cases SET Name = ?, Material = ?, Price = ?, Items_id = ? WHERE Id = ?", 
                   (case.name, case.material, case.price, case.Items_id, case_id))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.delete("/cases/{case_id}")
def delete_case(case_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Cases WHERE Id = ?", (case_id,))
    conn.commit()
    conn.close()
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)