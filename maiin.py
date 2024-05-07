import tkinter
from tkinter import messagebox
import sqlite3

def is_valid_make(make):
    return all(char.isalpha() or char.isspace() for char in make)
def is_valid_year(year):
    return year.isdigit() and len(year) == 4
def is_valid_mileage(mileage):
    return mileage.isdigit()
def enter_data():
    make = make_entry.get()
    model = model_entry.get()
    year = year_entry.get()
    mileage = mileage_entry.get()
    serial_number = serial_entry.get()
    
    if make and model and year and mileage and serial_number:
        if is_valid_make(make):
            if is_valid_year(year):
                if is_valid_mileage(mileage):
                    print("Car make:", make)
                    print("Car model:", model)
                    print("Year:", year)
                    print("Mileage:", mileage)
                    print("Serial Number:", serial_number)
                    print("------------------------------------------")
                    
                    conn = sqlite3.connect('car_data.db')
                    table_create_query = '''CREATE TABLE IF NOT EXISTS Car_Data 
                            (serial_number INTEGER PRIMARY KEY, make TEXT, model TEXT, year INT, mileage INT)
                    '''
                    conn.execute(table_create_query)
                    data_insert_query = '''INSERT INTO Car_Data (serial_number, make, model, year, mileage) VALUES (?, ?, ?, ?, ?)'''
                    data_insert_tuple = (serial_number, make, model, year, mileage)
                    cursor = conn.cursor()
                    cursor.execute(data_insert_query, data_insert_tuple)
                    conn.commit()
                    conn.close()
                else:
                    tkinter.messagebox.showwarning(title="Error", message="Mileage should contain only integers.")
            else:
                tkinter.messagebox.showwarning(title="Error", message="Year should be a 4-digit number.")
        else:
            tkinter.messagebox.showwarning(title="Error", message="Make should contain only characters.")
    else:
        tkinter.messagebox.showwarning(title="Error", message="Please fill in all fields.")
        
def update_data():
    serial_number = serial_entry.get()
    
    if serial_number:
        make = make_entry.get()
        model = model_entry.get()
        year = year_entry.get()
        mileage = mileage_entry.get()
        if make and model and year and mileage:
            if is_valid_make(make):
                if is_valid_year(year):
                    if is_valid_mileage(mileage):
                        conn = sqlite3.connect('car_data.db')
                        cursor = conn.cursor()
                        cursor.execute('''UPDATE Car_Data SET make=?, model=?, year=?, mileage=? WHERE serial_number=?''',
                                       (make, model, year, mileage, serial_number))
                        conn.commit()
                        conn.close()
                    else:
                        tkinter.messagebox.showwarning(title="Error", message="Mileage should contain only integers.")
                else:
                    tkinter.messagebox.showwarning(title="Error", message="Year should be a 4-digit number.")
            else:
                tkinter.messagebox.showwarning(title="Error", message="Make should contain only characters.")
        else:
            tkinter.messagebox.showwarning(title="Error", message="Please fill in all fields.")
    else:
        tkinter.messagebox.showwarning(title="Error", message="Please enter a serial number.")

def delete_data():
    serial_number = serial_entry.get()
    if serial_number:
        conn = sqlite3.connect('car_data.db')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM Car_Data WHERE serial_number=?''', (serial_number,))
        conn.commit()
        conn.close()
    else:
        tkinter.messagebox.showwarning(title="Error", message="Please enter a serial number.")

window = tkinter.Tk()
window.title("Car Management System")

frame = tkinter.Frame(window)
frame.pack()
car_info_frame = tkinter.LabelFrame(frame, text="Car Information")
car_info_frame.grid(row=0, column=0, padx=20, pady=10)

serial_label = tkinter.Label(car_info_frame, text="Serial Number")
serial_entry = tkinter.Entry(car_info_frame)
serial_label.grid(row=0, column=0)
serial_entry.grid(row=0, column=1)

make_label = tkinter.Label(car_info_frame, text="Make")
make_entry = tkinter.Entry(car_info_frame)
make_label.grid(row=1, column=0)
make_entry.grid(row=1, column=1)

model_label = tkinter.Label(car_info_frame, text="Model")
model_entry = tkinter.Entry(car_info_frame)
model_label.grid(row=2, column=0)
model_entry.grid(row=2, column=1)

year_label = tkinter.Label(car_info_frame, text="Year")
year_entry = tkinter.Entry(car_info_frame)
year_label.grid(row=3, column=0)
year_entry.grid(row=3, column=1)

mileage_label = tkinter.Label(car_info_frame, text="Mileage")
mileage_entry = tkinter.Entry(car_info_frame)
mileage_label.grid(row=4, column=0)
mileage_entry.grid(row=4, column=1)

for widget in car_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

button_enter = tkinter.Button(frame, text="Enter data", command=enter_data)
button_enter.grid(row=1, column=0, sticky="news", padx=20, pady=10)
button_update = tkinter.Button(frame, text="Update data", command=update_data)
button_update.grid(row=2, column=0, sticky="news", padx=20, pady=10)
button_delete = tkinter.Button(frame, text="Delete data", command=delete_data)
button_delete.grid(row=3, column=0, sticky="news", padx=20, pady=10)
window.mainloop()