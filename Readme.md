# 📚 API REST - Librería Chiapas

API RESTful desarrollada con **FastAPI**, **SQLModel** y **PostgreSQL (Supabase)** para la gestión integral de inventario de libros, editoriales y autenticación de usuarios mediante *Bearer Token*.

Proyecto final de la asignatura **Taller de Desarrollo III (5.° A)**.

---

## 🌐 Enlaces del Proyecto

* **API en Producción (Render):** https://api-biblioteca-rneg.onrender.com
* **Documentación Interactiva (Swagger UI):** https://api-biblioteca-rneg.onrender.com/docs
* **Repositorio en GitHub:** https://github.com/torresecheverriajulio-eng/API_Biblioteca

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.11.9
* **Framework Web:** FastAPI
* **Servidor ASGI:** Uvicorn
* **ORM y Validación:** SQLModel / Pydantic
* **Base de Datos:** PostgreSQL alojado en Supabase (`psycopg[binary]`)
* **Despliegue en la Nube:** Render

---

## 📁 Estructura del Repositorio

```text
API_Biblioteca/
├── main.py              # Endpoints, lógica CRUD, consultas y seguridad Bearer Token
├── models.py            # Modelos relacionales SQLModel (Usuario, Editorial, Libro)
├── requirements.txt     # Dependencias del proyecto
├── runtime.txt          # Versión de Python para despliegue en Render
└── README.md            # Documentación técnica del proyecto
```

---

## 🗄️ Modelo de Base de Datos (PostgreSQL)

La base de datos consta de 3 tablas principales:

1. **`usuarios`**: Almacena las credenciales de acceso (`id`, `username`, `password`).
2. **`editorial`**: Catálogo de casas editoriales (`ided`, `nombre`, `pais`).
3. **`libro`**: Inventario de ejemplares (`ISBN`, `titulo`, `autor`, `precio`, `existencia`, `ided_editorial`, `year`), con llave foránea hacia `editorial.ided`.

---

## 🔐 Autenticación

Todos los endpoints de consulta y modificación están protegidos mediante cabecera HTTP `Authorization`:

```http
Authorization: Bearer abc123tokenbiblioteca
```

* Si el token no se envía o es incorrecto, la API responde con **`401 Unauthorized`**.
* Para obtener el token, realiza una petición `POST /login` con un usuario registrado en la tabla `usuarios`.

---

## 🚀 Endpoints Disponibles

### 1. Estado y Autenticación
| Método | Ruta | Protección | Descripción |
| :--- | :--- | :---: | :--- |
| `GET` | `/` | Pública | Verifica que el servicio esté en línea. |
| `POST` | `/login` | Pública | Valida `username` y `password` en PostgreSQL y devuelve el `access_token`. |

### 2. CRUD de Libros
| Método | Ruta | Protección | Descripción |
| :--- | :--- | :---: | :--- |
| `POST` | `/libros` | Bearer Token | Registra un nuevo libro (`201 Created`). |
| `GET` | `/libros` | Bearer Token | Lista todos los libros registrados. |
| `GET` | `/libros/{isbn}` | Bearer Token | Consulta un libro específico por su ISBN. |
| `PUT` | `/libros/{isbn}` | Bearer Token | Actualiza los datos o existencia de un libro. |
| `DELETE` | `/libros/{isbn}` | Bearer Token | Elimina un libro de la base de datos. |

### 3. CRUD de Editoriales
| Método | Ruta | Protección | Descripción |
| :--- | :--- | :---: | :--- |
| `POST` | `/editoriales` | Bearer Token | Registra una nueva editorial (`201 Created`). |
| `GET` | `/editoriales` | Bearer Token | Lista todas las editoriales registradas. |
| `GET` | `/editoriales/{ided}` | Bearer Token | Consulta una editorial por su ID. |
| `PUT` | `/editoriales/{ided}` | Bearer Token | Actualiza la información de una editorial. |
| `DELETE` | `/editoriales/{ided}` | Bearer Token | Elimina una editorial. |

### 4. Consultas Personalizadas
| Método | Ruta | Protección | Descripción |
| :--- | :--- | :---: | :--- |
| `GET` | `/libros/sinexistencia` | Bearer Token | Devuelve los libros agotados (`existencia == 0`). |
| `GET` | `/libros/editorial/{editorial_id}` | Bearer Token | Filtra los libros pertenecientes a una editorial. |
| `GET` | `/libros/anio/{anio}` | Bearer Token | Filtra los libros publicados en un año específico. |

---

## ⚙️ Instalación y Ejecución Local

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/torresecheverriajulio-eng/API_Biblioteca.git
   cd API_Biblioteca
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la variable de entorno de PostgreSQL:**
   ```bash
   export DATABASE_URL="postgresql://usuario:password@host:5432/postgres"
   ```

5. **Iniciar el servidor de desarrollo:**
   ```bash
   uvicorn main:app --reload
   ```
   La documentación interactiva estará disponible en `http://127.0.0.1:8000/docs`.

---

## 👥 Autores

* **Integrante 1: Julio David Torres Echeverría
* **Integrante 2: Juan Antonio Victorio Domínguez
* **Docente:** Dr. Christian Mauricio Castillo Estrada
