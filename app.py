from flask_sqlalchemy import SQLAlchemy
from db import db
from dotenv import load_dotenv
from flask_login import LoginManager, login_required, login_user, current_user
from flask import Flask, request, render_template
from flask_restful import Api
from Models.usuario import Usuarios
from Controller.productocontroller import ProductoController
from Controller.ingredientecontroller import IngredienteController
from Controller.ventacontroller import VentaController
from Models.ingredientes import Ingredientes
from Models.productos import Productos 
from Models.ventas import Ventas
import os

load_dotenv()

secret_key = os.urandom(24)

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://{os.getenv("USER_DB")}:{os.getenv("PASSWORD_DB")}@{os.getenv("HOST_DB")}/{os.getenv("SCHEMA_DB")}'
app.config["SECRET_KEY"] = secret_key
db.init_app(app)
api = Api(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    user = Usuarios.query.get(id)
    if user:
        print(user)
        return user
    return None

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        nombre_usuario = request.form['nombre_usuario']
        contrasenia = request.form['contrasenia']
        usuario = Usuarios.query.filter_by(nombre_usuario=nombre_usuario, contrasenia=contrasenia).first()
        if usuario:
            print(usuario)
            login_user(usuario)
            return render_template("Bienvenida.html")
        else:
            return render_template("Bienvenida.html")

@app.route("/Productos")
def productos():
        producto_controller=ProductoController()
        productos=Productos.query.all()
        return render_template("Menu.html", productos=zip(productos, producto_controller.obtener_lista_productos(), 
                                producto_controller.obtener_calorias()))
        
@login_required
@app.route("/Productos/<dato>")
def producto(dato)->None:
    try:
        dato=int(dato)
    except:
        pass
    if type(dato)==int:
        if current_user.es_admin or current_user.es_empleado:
            producto_controller=ProductoController()
            producto=Productos.query.filter_by(id=dato).first()
            lista_ingrediente=producto_controller.obtener_lista_productos()
            ingredientes=lista_ingrediente[dato-1]
            return render_template("producto_id.html", producto=producto, ingredientes=ingredientes)
        else:
            return render_template("Error_401.html")
    else:
        if current_user.es_admin or current_user.es_empleado:
            producto_controller=ProductoController()
            producto=Productos.query.filter_by(nombre=dato).first()
            lista_ingrediente=producto_controller.obtener_lista_productos()
            ingredientes=lista_ingrediente[producto.id-1]
            return render_template("producto_nombre.html", producto=producto, ingredientes=ingredientes)
        else:
            return render_template("Error_401.html")

@login_required       
@app.route("/Productos/Calorias/<id>")
def calorias_id(id: int)->None:
    id=int(id)
    if current_user:
        producto_controller=ProductoController()
        producto=Productos.query.filter_by(id=id).first()
        lista_calorias=producto_controller.obtener_calorias()
        calorias_id=lista_calorias[id-1]
        return render_template("calorias_id.html", producto=producto, calorias=calorias_id)
    else:
        return render_template("Error_401.html")

@login_required
@app.route("/Productos/Costo/<id>")
def costo_id(id: int)->None:
    id=int(id)
    if current_user.es_admin:
        producto_controller=ProductoController()
        producto=Productos.query.filter_by(id=id).first()
        lista_precio_ingredientes=producto_controller.obtener_lista_precios_ingredientes(id_producto=id)
        costo=producto_controller.calcular_costo(lista_precios_ingredientes=lista_precio_ingredientes)
        return render_template("costo_id.html", producto=producto, costo=costo)
    else:
        return render_template("Error_401.html")    

@login_required
@app.route("/Ingredientes")
def ingredientes():
    if current_user.es_admin or current_user.es_ampleado:
        ingredientes = Ingredientes.query.all()
        return render_template("ingredientes.html", ingredientes=ingredientes)
    else:
        return render_template("Error_401.html") 

@login_required
@app.route("/Ingredientes/<dato>")
def ingrediente(dato)->None:
    try:
        dato=int(dato)
    except:
        pass
    if type(dato)==int:
        if current_user.es_admin or current_user.es_ampleado:
            ingrediente = Ingredientes.query.filter_by(id=dato).first()
            return render_template("ingrediente_id.html", ingrediente=ingrediente)
        else:
            return render_template("Error_401.html")
    else:
        if current_user.es_admin or current_user.es_ampleado:
            ingrediente = Ingredientes.query.filter_by(nombre=dato).first()
            return render_template("ingrediente_nombre.html", ingrediente=ingrediente)
        else:
            return render_template("Error_401.html")

@login_required
@app.route("/Ingredientes/es_sano/<id>")
def es_sano_id(id: int)->None:
    id=int(id)
    if current_user.es_admin or current_user.es_ampleado:
        ingredientecontroller=IngredienteController()
        ingrediente = Ingredientes.query.filter_by(id=id).first()
        sano=ingredientecontroller.es_sano(id_ingrediente=id)
        if sano:
            rta_es_sano=f"El ingrediente {ingrediente.nombre} es sano"
        else:
            rta_es_sano=f"El ingrediente {ingrediente.nombre} no es sano"
        return render_template("es_sano_id.html", rta_es_sano=rta_es_sano)
    else:
        return render_template("Error_401.html")


@login_required
@app.route("/Ingredientes/abastecer/<id>")
def abastecer_id(id: int)->None:
    id=int(id)
    if current_user.es_admin or current_user.es_ampleado:
        ingredientecontroller=IngredienteController()
        ingredientecontroller.abastecer(id_ingrediente=id)
        ingrediente = Ingredientes.query.filter_by(id=id).first()
        nombre_ingrediente=ingrediente.nombre
        inventario=ingrediente.inventario
        return render_template("abastecer_id.html", nombre_ingrediente=nombre_ingrediente, inventario=inventario)
    else:
        return render_template("Error_401.html")

@login_required
@app.route("/Ingredientes/renovar/<id>")
def renovar_id(id: int)->None:
    id=int(id)
    if current_user.es_admin or current_user.es_ampleado:
        ingredientecontroller=IngredienteController()
        ingredientecontroller.renovar_inventario_complemento(id_ingrediente=id)
        ingrediente = Ingredientes.query.filter_by(id=id).first()
        nombre_ingrediente=ingrediente.nombre
        inventario=ingrediente.inventario
        return render_template("renovacion_id.html", nombre_ingrediente=nombre_ingrediente, inventario=inventario)
    else:
        return render_template("Error_401.html")

@login_required
@app.route("/Ventas")
def Ventas_tabla()->None:
    if current_user.es_admin:
        ventas=Ventas.query.all()
        return render_template("ventas.html", ventas=ventas)
    else:
        return render_template("Error_401.html")
    
@login_required
@app.route("/Venta/<id>")
def venta_id(id: int)->None:
    id=int(id)
    if current_user:
        producto = Productos.query.filter_by(id=id).first()
        ventacontroller=VentaController()
        venta,lista_inventario_vacios=ventacontroller.vender(producto.id)
        if venta==True:
            return render_template("Venta_exitosa_id.html", producto_vendido=producto)
        else:
            return render_template("Venta_fallida_id.html", inventario_vacio=lista_inventario_vacios)
    else:
        return render_template("Error_401.html")

if __name__=="__app__":
    app.run(debug=True)
    
    
    
    