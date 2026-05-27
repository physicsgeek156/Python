from tkinter import *

root = Tk()
root.title("Movie database")
root.geometry("450x450")
Label(root, text="Movies I've watched", font=("Arial", 16), fg="black").pack(side=TOP, fill=X)

top_frame = Frame(root, bg="lightgreen")
top_frame.place(x=0, y=30, relwidth=1, relheight=0.3)

Label(top_frame, text="Movie Name", font=("Arial", 12), fg="black").place(x=10, y=10)
movie_name = Entry(top_frame).place(x=110, y=10)


rating = StringVar(root)
rating.set("Choose a rating") 
Label(top_frame, text="Rating", font=("Arial", 12), fg="black").place(x=250, y=10)
movie_rating = OptionMenu(top_frame, rating,*['1', '2', '3', '4', '5']).place(x=310, y=10)

Button(top_frame, text="Add Movie", font=("Arial", 12), fg="black").place(x=175, y=50)

root.mainloop()