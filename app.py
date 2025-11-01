import os
from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# --- INICIO DE RUTAS CRUD ---

# CREATE (Crear Tarea)
@app.route('/crear', methods=['POST'])
def crear_tarea():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']

        # Insertar datos en Supabase
        try:
            supabase.table('tareas').insert({
                'titulo': titulo,
                'descripcion': descripcion
            }).execute()
        except Exception as e:
            print(f"Error al insertar: {e}")

    return redirect(url_for('index'))

# READ (Leer Todas las Tareas)
@app.route('/')
def index():
    try:
        # Seleccionar todas las tareas
        response = supabase.table('tareas').select('*').order('id', desc=True).execute()
        tareas = response.get('data', [])
    except Exception as e:
        print(f"Error al leer: {e}")
        tareas = []

    return render_template('index.html', tareas=tareas)

# UPDATE (Mostrar página para Editar Tarea)
@app.route('/editar/<int:id>')
def mostrar_editar_tarea(id):
    try:
        # Obtener la tarea específica por ID
        response = supabase.table('tareas').select('*').eq('id', id).single().execute()
        tarea = response.get('data')
        if not tarea:
            return "Tarea no encontrada", 404
    except Exception as e:
        print(f"Error al obtener tarea: {e}")
        return redirect(url_for('index'))

    return render_template('editar.html', tarea=tarea)

# UPDATE (Procesar la Edición de Tarea)
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_tarea(id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        # El checkbox 'completada' enviará 'on' si está marcado, o nada si no lo está.
        completada = 'completada' in request.form 

        try:
            supabase.table('tareas').update({
                'titulo': titulo,
                'descripcion': descripcion,
                'completada': completada
            }).eq('id', id).execute()
        except Exception as e:
            print(f"Error al actualizar: {e}")

    return redirect(url_for('index'))

# DELETE (Eliminar Tarea)
@app.route('/eliminar/<int:id>')
def eliminar_tarea(id):
    try:
        supabase.table('tareas').delete().eq('id', id).execute()
    except Exception as e:
        print(f"Error al eliminar: {e}")

    return redirect(url_for('index'))

# --- FIN DE RUTAS CRUD ---

if __name__ == '__main__':
    app.run(debug=True)