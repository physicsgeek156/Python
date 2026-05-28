import sqlite3
from tkinter import *
import tkinter.messagebox as mb

conn = sqlite3.connect('movie_database.db')
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS movies (movie_name TEXT, rating TEXT)')

def add_movie(movie_name, rating):
    try:
        cursor.execute('INSERT INTO movies (movie_name, rating) VALUES (?,?)',(movie_name, rating))
        conn.commit()
        cursor.execute('SELECT * FROM movies')
        print(cursor.fetchall())
    except sqlite3.IntegrityError:
                mb.showerror("Movie already added!")