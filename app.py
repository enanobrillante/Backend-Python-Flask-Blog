from flask import Flask ,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#definimos la configuracion de la app y la bbdd
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/mauro/bf6796d2-a6fb-4f57-9f75-246f4d18316a/PROGRAMACION/CURSO_FLASK_MUNDO_PYTHON/flask_blog/blog_BBDD"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
db = SQLAlchemy(app)
app.app_context().push() #solucionó el error que daba al crear la bbdd

class Post(db.Model):
	__tablename__= "post" #le damos un nombre a la tabla
	id = db.Column(db.Integer, primary_key=True)
	titulo = db.Column(db.String, nullable=False) #significa que el valor no puede estar vació
	fecha = db.Column(db.DateTime, default=datetime.now)
	texto = db.Column(db.String, nullable=False)

#creamos las vistas
@app.route("/")
def inicio():
	post = Post.query.order_by(Post.fecha.desc()).all()
	return render_template("inicio.html", posti=post, cantidad=len(post))

@app.route("/agregar")
def agregar():
	return render_template("agregar.html")

@app.route("/borrar", methods=["POST"])
def borrar():
	post_id = request.form.get("post_id_borrar")
	post = db.session.query(Post).filter(Post.id == post_id).first()
	db.session.delete(post)
	db.session.commit()
	return redirect("/")

@app.route("/crear", methods=["POST"])
def crear_post():
	titulo = request.form.get("titulo")
	texto = request.form.get("texto") #con rquest accedemos a form y extraemos lo que tiene el cmapo de name=titulo
	post = Post(titulo=titulo, texto=texto) #agrega a BBDD
	db.session.add(post)
	db.session.commit()
	return redirect("/") #al crear el post nos redirecciona la pagina de inicio

if __name__=="__main__":
	app.run(debug=True)
