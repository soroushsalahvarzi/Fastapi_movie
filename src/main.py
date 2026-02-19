from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Movie(BaseModel):
    name: str
    year: int

def get_conn():
    return sqlite3.connect("movies.db")

conn = get_conn()
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    year INTEGER
)
''')
conn.commit()
conn.close()

@app.get("/movies")
def get_movies():
        conn = get_conn()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM movies")
            rows = cursor.fetchall()

            return [
                {"id": r[0], "name": r[1], "year": r[2]}
                for r in rows
            ]
        except sqlite3.Error as e:
             print("DB EROOR", e)
             raise HTTPException(500, "Database error")
        finally:
             conn.close()

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
     conn = get_conn()
     try:
          cursor = conn.cursor()
          cursor.execute("SELECT * FROM movies WHERE id=?", (movie_id,))
          row = cursor.fetchone()
          if not row:
               raise HTTPException(404, "Movie not found")
          return {"id": row[0], "name": row[1], "year": row[2]}
     except sqlite3.Error as e:
          print("DB ERROR", e)
          raise HTTPException(500, "Database error")
     finally:
          conn.close()

@app.post("/movies")
def add_movie(movie: Movie):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO movies (name, year) VALUSE(?, ?)",
            (movie.name, movie.year)
        )
        conn.commit()
        new_id = cursor.lastrowid

        return {"id": new_id, **movie.dict()}
    except sqlite3.Error as e:
         print("DB ERROR:", e)
         raise HTTPException(500, "Insert failed")
    finally:
        conn.close()

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: Movie):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE movies SET name=?, year=?, WHERE id=?",
            (movie.name, movie.year, movie_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(404, "Movie not found")
        return {"id": movie_id, **movie.dict()}
    except sqlite3.Error as e:
         print("DB ERROR:", e)
         raise HTTPException(500, "Update failed")
    finally:
        conn.close()

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movies WHERE id=?", (movie_id))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(404, "Movie not found")
        return {"deleted": movie_id}
    except sqlite3.Error as e:
        print("DB ERROR:", e)
        raise HTTPException(500, "Delete failed")
    finally:
         conn.close() 
        
               
     
    

        
              
