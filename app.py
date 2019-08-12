#Video seguido: https://www.youtube.com/watch?v=Z1RJmh_OqeA
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy #Usaremos SQLAlchemy para la db https://www.sqlalchemy.org/
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #Decimos a la app la localización de la basededatos
db = SQLAlchemy(app) #Inicializamos base de datos

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        #Fnción que devuelve un string cada vez que creamos un elemento
        return '<Task %r>' % self.id
#@app.route decorator se usa para indicar a flask que URL activará la función. en este caso '/' activará la función index.
@app.route('/', methods=['POST', 'GET']) #options=methods: añade métodos para añadir y recibir datos a esa ruta
def index():
    db.create_all()
    #Si se hace solicitud tipo POST
    if request.method ==  'POST': #POST se usa para enviar datos
        task_content = request.form['content'] #Accedemos al formulario de index.html cuyo name es content
        new_task = Todo(content=task_content) #Hacemos que el content del formulario sea igual a la entrada
        
        #Mandamos los datos a la db
        try:
            db.session.add(new_task) #Añade el dato
            db.session.commit() #Hace el commit a la db
            return redirect('/') #Devuelve el usuario a la localización dada
        except:
            return 'Ha ocurrido un problema al añadir a la tabla'

    else:
        #query = consulta a la db
        tasks = Todo.query.order_by(Todo.date_created).all() #Ordena la tabla por fecha de cración
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) #Intentamos obtener una tarea por ID
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method=='POST':
        task.content = request.form['content'] #ponemos la variable task igual al contenido del formulario

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error al actualizar"

    else:
        return render_template('update.html', task=task)

#Cuando usamos el decorator route() decimos a flask que URL 
# deberia activar nuestra función
#route() se le da un nombre que usa para generar URLs para funciones
#específicas y retorna el mensaje que queremos mostrar en el navegador

if __name__ == "__main__":
    app.run(debug=True)
