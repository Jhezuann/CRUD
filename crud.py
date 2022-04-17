from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Interfaz grafica
wn = Tk()
wn.title("CRUD")
wn.geometry("900x350")

miId=StringVar()
miNombre=StringVar()
miApellido=StringVar()
miEdad=StringVar()
miCargo=StringVar()
miSalario=StringVar()

# Conexion y cursor

miConexion=sqlite3.connect("base")
miCursor=miConexion.cursor()

# Tabla
tree=ttk.Treeview(height=10, columns=('#0', '#1', '#2', '#3', '#4'))
tree.place(x=0, y=130)
tree.column('#0', width=100)
tree.heading('#0', text="ID", anchor=CENTER)
tree.heading('#1', text="NAME", anchor=CENTER)
tree.heading('#2', text="SURNAME", anchor=CENTER)
tree.column('#3', width=100)
tree.heading('#3', text="AGE", anchor=CENTER)
tree.heading('#4', text="CHARGE", anchor=CENTER)
tree.column('#5', width=100)
tree.heading('#5', text="SALARY", anchor=CENTER)
# Funciones

def conexionBBDD():
	try:
		miCursor.execute('''
			CREATE TABLE empleado (
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			NOMBRE VARCHAR(50) NOT NULL,
			APELLIDO VARCHAR(50) NOT NULL,
			EDAD INT NOT NULL,
			CARGO VARCHAR(50) NOT NULL,
			SALARIO INT NOT NULL)
			''')
		messagebox.showinfo("CONEXION", "Base de datos Creada exitosamente")
	except:
		messagebox.showinfo("CONEXION", "Conecion exitosa con la base de datos")

def eliminarBBDD():
	if messagebox.askyesno(message="Los datos se perderan definitivamente, Desea continuar?", title="ADVERTENCIA"):
		miCursor.execute("DROP TABLE empleado")
	else:
		pass
	limpiarCampos()
	read()

def salir():
	valor=messagebox.askquestion("Salir", "Desea salir de CRUD?")
	if valor == "yes":
		wn.destroy()
	else:
		pass

def limpiarCampos():
	miId.set("")
	miNombre.set("")
	miApellido.set("")
	miEdad.set("")
	miCargo.set("")
	miSalario.set("")

def acercaDe():
	messagebox.showinfo(message='''
		Aplicacion CRUD
		Version 1.0
		Python''', title="Acerca De")

def selectclick(event):
	item=tree.identify('item',event.x,event.y)
	miId.set(tree.item(item, "text"))
	miNombre.set(tree.item(item, "values")[0])
	miApellido.set(tree.item(item, "values")[1])
	miEdad.set(tree.item(item, "values")[2])
	miCargo.set(tree.item(item, "values")[3])
	miSalario.set(tree.item(item, "values")[4])

tree.bind("<Double-1>", selectclick)

# Funciones del crud

def create():
	try:
		datos=miNombre.get(),miApellido.get(),miEdad.get(),miCargo.get(),miSalario.get()
		miCursor.execute("INSERT INTO empleado VALUES(NULL,?,?,?,?,?)", (datos))
		miConexion.commit()
	except:
		messagebox.showwarning("ADVERTENCIA", "Ocurrio un error al crear un registro, Verfique conexion con BBDD")
		pass
	limpiarCampos()
	read()

def read():
	registros=tree.get_children()
	for elemento in registros:
		tree.delete(elemento)

	try:
		miCursor.execute("SELECT * FROM empleado")
		for row in miCursor:
			tree.insert("",0,text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))
	except:
		pass

def update():
	try:
		datos=miNombre.get(),miApellido.get(),miEdad.get(),miCargo.get(),miSalario.get()
		miCursor.execute("UPDATE empleado SET NOMBRE=?, APELLIDO=?, EDAD=?, CARGO=?, SALARIO=? WHERE ID="+miId.get(), (datos))
		miConexion.commit()
	except:
		messagebox.showwarning("ADVERTENCIA", "Ocurrio un error al actualizar el registro")
		pass
	limpiarCampos()
	read()

def delete():
	try:
		if messagebox.askyesno(message="Realmente desea eliminar el registro?", title="ADVERTENCIA"):
			miCursor.execute("DELETE FROM empleado WHERE ID="+miId.get())
			miConexion.commit()
	except:
		messagebox.showwarning("ADVERTENCIA", "Ocurrio un error al eliminar el registro")
		pass
	limpiarCampos()
	read()

#Elementos graficos

#menu

barraMenu=Menu(wn)
inicio=Menu(barraMenu, tearoff=0)
inicio.add_command(label="Crear/Conectar a la Base de Datos", command=conexionBBDD)
inicio.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
inicio.add_command(label="Salir", command=salir)
barraMenu.add_cascade(label="Inicio", menu=inicio)

rese=Menu(barraMenu, tearoff=0)
rese.add_command(label="Resetar campos", command=limpiarCampos)
rese.add_command(label="Acerca De", command=acercaDe)
barraMenu.add_cascade(label="Resetar", menu=rese)

#Etiquetas y cajas de texto

e=Entry(wn, textvariable=miId)

l2=Label(wn, text="Name")
l2.place(x=50, y=30)
e2=Entry(wn, textvariable=miNombre, width=20)
e2.place(x=95, y=30)

l3=Label(wn, text="Surname")
l3.place(x=240, y=30)
e3=Entry(wn, textvariable=miApellido, width=20)
e3.place(x=295, y=30)

l4=Label(wn, text="Age")
l4.place(x=430, y=30)
e4=Entry(wn, textvariable=miEdad, width=7)
e4.place(x=460, y=30)

l5=Label(wn, text="Charge")
l5.place(x=140, y=60)
e5=Entry(wn, textvariable=miCargo, width=20)
e5.place(x=185, y=60)

l6=Label(wn, text="Salary")
l6.place(x=360, y=60)
e6=Entry(wn, textvariable=miSalario, width=7)
e6.place(x=405, y=60)

l7=Label(wn, text="USD")
l7.place(x=460, y=60)

#Botones CRUD

b1=Button(wn, text="Create", command=create)
b1.place(x=650, y=10)

b1=Button(wn, text="Read", command=read)
b1.place(x=800, y=10)

b1=Button(wn, text="Update", command=update)
b1.place(x=647, y=65)

b1=Button(wn, text="Delete", bg="red", command=delete)
b1.place(x=796, y=65)


wn.config(menu=barraMenu)

wn.mainloop()