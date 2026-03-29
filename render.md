# Deploy en Render (paso a paso)

Este proyecto es una app **Django**. Estos pasos te dejan la app funcionando en **Render** (con URL pública).

## 0) Requisitos previos

- Tener una cuenta en Render.
- Tener el proyecto subido a GitHub (Render despliega desde un repo).

> Nota: este proyecto usa SQLite por defecto. En Render funciona, pero **los datos pueden perderse** en algunos reinicios/redeploy. Si necesitas persistencia, revisa la sección **"Opcional: PostgreSQL"** al final.

## 1) Preparar el proyecto (ya listo en este repo)

En este repo ya están agregados:

- `requirements.txt` (incluye `gunicorn` y `whitenoise`).
- Configuración para `ALLOWED_HOSTS` y static files (para que funcione con Render).
- `render.md` (este archivo).

Si quieres validar localmente:

```bash
pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

## 2) Subir el proyecto a GitHub

Desde la carpeta del proyecto:

```bash
git init
git add .
git commit -m "Deploy Django en Render"
```

1. Crea un repositorio en GitHub (vacío).
2. Conecta el repo local con GitHub (copia el URL del repo y reemplázalo):

```bash
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

## 3) Crear el servicio en Render

1. En Render, ve a **Dashboard** → **New +** → **Web Service**.
2. Elige **“Build and deploy from a Git repository”**.
3. Conecta tu GitHub (si te lo pide) y selecciona tu repositorio.
4. Configura el servicio:
   - **Runtime:** Python
   - **Branch:** `main`
   - **Build Command:**

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

   - **Start Command:**

```bash
python manage.py migrate && gunicorn prestamos_lab.wsgi:application
```

5. Apreta **Create Web Service** y espera el deploy.

## 4) Variables de entorno (Render → Environment)

En tu servicio de Render, entra a **Environment** y agrega:

- `DEBUG` = `False`
- `SECRET_KEY` = una clave larga (puedes generar una cualquiera, por ejemplo 50+ caracteres)

Tip para generar `SECRET_KEY` (local):

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Opcional (si quieres controlar hosts manualmente):

- `ALLOWED_HOSTS` = `tu-servicio.onrender.com`

> Si no pones `ALLOWED_HOSTS`, el proyecto ya permite dominios `.onrender.com`.

## 5) Crear usuario admin en producción

Para poder entrar a `/admin/` en el deploy:

1. En tu servicio de Render, abre una consola (**Shell**) si está disponible.
2. Ejecuta:

```bash
python manage.py createsuperuser
```

Luego entra a:

- `https://TU-SERVICIO.onrender.com/admin/`

## 6) Probar que todo funciona

Checklist rápida:

- La home carga: `https://TU-SERVICIO.onrender.com/`
- Login: `https://TU-SERVICIO.onrender.com/cuentas/login/`
- Admin: `https://TU-SERVICIO.onrender.com/admin/`
- “Reporte interno”: `https://TU-SERVICIO.onrender.com/reporte-interno/`

## 7) (Para la nota) Captura en GitHub

1. Guarda tu captura como `docs/captura.png`.
2. En `README.md` descomenta la línea:

```md
![Captura de pantalla](docs/captura.png)
```

3. Sube el cambio:

```bash
git add README.md docs/captura.png
git commit -m "Agrega captura"
git push
```

## Errores típicos (y solución)

### `DisallowedHost`

- Solución: en Render agrega `ALLOWED_HOSTS = tu-servicio.onrender.com` (en Environment) y redeploy.

### No carga el CSS / static

- Verifica que el **Build Command** incluya `collectstatic --noinput`.
- Revisa logs del deploy en Render.

### Error 500 al iniciar

- Revisa **Logs** en Render (te dirá el error exacto).
- Asegúrate de tener `DEBUG=False` y `SECRET_KEY` definido.

## Opcional: usar PostgreSQL (persistencia real)

Si tu profe te pide base de datos persistente, lo recomendado es PostgreSQL:

1. En Render → **New +** → **PostgreSQL** (crea una BD).
2. Copia el **Internal Database URL**.
3. En tu Web Service → **Environment**, agrega `DATABASE_URL` con ese valor.
4. Ajusta `prestamos_lab/settings.py` para leer `DATABASE_URL` (esto requiere agregar dependencias como `dj-database-url` y `psycopg`).

Si quieres, te lo dejo listo con PostgreSQL (cambios + dependencias) y te indico exactamente qué crear en Render.
