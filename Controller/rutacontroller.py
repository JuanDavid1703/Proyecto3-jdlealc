from app import app
from flask_login import login_required, current_user
from Models.productos import Productos
from Models.ingredientes import Ingredientes
from Models.ventas import Ventas
from flask import render_template, make_response
from Controller.productocontroller import  ProductoController
from Controller.ventacontroller import VentaController
from Controller.ingredientecontroller import IngredienteController
from flask_restful import Resource




class Routecontroller(app, Resource):
    
    @app.route("/Productos")
    def productos(self):
        producto_controller=ProductoController()
        productos=Productos.query.all()
        return make_response(render_template("Menu.html", productos=zip(productos, producto_controller.obtener_lista_productos(), 
                                                   producto_controller.obtener_calorias())))
    
    
    @login_required
    @app.route("/Productos/<dato>")
    def producto(self, dato)->None:
        if type(dato)==int:
            producto_controller=ProductoController()
            producto=Productos.query.filter_by(id=id).first()
            lista_ingrediente=producto_controller.obtener_lista_productos()
            ingredientes=lista_ingrediente[id-1]
            return make_response(render_template("producto_id.html", producto=producto, ingredientes=ingredientes))
        else:
            producto_controller=ProductoController()
            producto=Productos.query.filter_by(nombre=dato).first()
            lista_ingrediente=producto_controller.obtener_lista_productos()
            ingredientes=lista_ingrediente[producto.id-1]
            return make_response(render_template("producto_nombre.html", producto=producto, ingredientes=ingredientes))
    
    
    @login_required
    @app.route("/Productos/Calorias/<id>")
    def calorias_id(self)->None:
        producto_controller=ProductoController()
        producto=Productos.query.filter_by(id=id).first()
        lista_calorias=producto_controller.obtener_calorias()
        calorias_id=lista_calorias[id-1]
        return make_response(render_template("calorias_id.html", producto=producto, calorias=calorias_id))
    
    
    @login_required
    @app.route("/Productos/Rentabilidad/<id>")
    def rentabilidad_id(self)->None:
        producto_controller=ProductoController()
        producto=Productos.query.filter_by(id=id).first()
        
        lista_precio_ingredientes=producto_controller.obtener_lista_precios_ingredientes(id_producto=id)
        rentabilidad=producto_controller.calcular_rentabilidad(lista_precios_ingred=lista_precio_ingredientes,
                                                               precio_publico=producto.precio_publico)
        return make_response(render_template("rentabilidad_id.html", producto=producto, rentabilidad=rentabilidad))
    
    
    
    @login_required
    @app.route("/Productos/Costo/<id>")
    def costo_id(self)->None:
        producto_controller=ProductoController()
        producto=Productos.query.filter_by(id=id).first()
        lista_precio_ingredientes=producto_controller.obtener_lista_precios_ingredientes(id_producto=id)
        costo=producto_controller.calcular_costo(lista_precios_ingredientes=lista_precio_ingredientes)
        return make_response(render_template("costo_id.html", producto=producto, costo=costo))   
    
    @login_required
    @app.route("/Ingredientes")
    def ingredientes(self):
        ingredientes = Ingredientes.query.all()
        return render_template("ingredientes.html", ingredientes=ingredientes)
    
    @login_required
    @app.route("/Ingredientes/<dato>")
    def ingrediente(self, dato)->None:
        if type(dato)==int:
            ingrediente = Ingredientes.query.filter_by(id=id).first()
            return render_template("ingrediente_id.html", ingrediente=ingrediente)
        else:
            ingrediente = Ingredientes.query.filter_by(nombre=dato).first()
            return render_template("ingrediente_nombre.html", ingrediente=ingrediente)
    
    
    @login_required
    @app.route("/Ingredientes/es_sano/<id>")
    def es_sano_id(self, id: int)->None:
        ingredientecontroller=IngredienteController()
        ingrediente = Ingredientes.query.filter_by(id=id).first()
        sano=ingredientecontroller.es_sano(id_ingrediente=id)
        rta_es_sano=f" El ingrediente {ingrediente.nombre} {ingrediente.es_sano} es sano"
        return render_template("es_sano_id.html", rta_es_sano=rta_es_sano)
    
    
    
    @login_required
    @app.route("/Ingredientes/abastecer/<id>")
    def abastecer_id(self, id: int)->None:
        ingredientecontroller=IngredienteController()
        ingredientecontroller.abastecer(id_ingrediente=id)
        ingrediente = Ingredientes.query.filter_by(id=id).first()
        nombre_ingrediente=ingrediente.nombre
        inventario=ingrediente.inventario
        return render_template("abastecer_id.html", nombre_ingrediente=nombre_ingrediente, inventario=inventario)
    
    
    @login_required
    @app.route("/Ingredientes/renovar/<id>")
    def renovar_id(self, id: int)->None:
        ingredientecontroller=IngredienteController()
        ingredientecontroller.renovar_inventario_complemento(id_ingrediente=id)
        ingrediente = Ingredientes.query.filter_by(id=id).first()
        nombre_ingrediente=ingrediente.nombre
        inventario=ingrediente.inventario
        return render_template("renovacion_id.html", nombre_ingrediente=nombre_ingrediente, inventario=inventario)
    
    @login_required
    @app.route("/Ventas")
    def Ventas(self)->None:
        ventas=Ventas.query.all()
        return render_template("ventas.html", ventas=ventas)
    
        
    @login_required
    @app.route("/Venta/<id>")
    def venta_id(self, id: int)->None:
        producto = Productos.query.filter_by(id=id).first()
        ventacontroller=VentaController()
        venta,lista_inventario_vacios=ventacontroller.vender(producto.id)
        if venta==True:
            return render_template("Venta_exitosa_id.html", producto_vendido=producto)
        else:
            return render_template("Venta_fallida_id.html", inventario_vacio=lista_inventario_vacios)