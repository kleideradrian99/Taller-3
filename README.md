# Taller 3 — Mesa de servicios (laboratorios)

API con **FastAPI** y **PostgreSQL** para gestión de tickets, según la guía del repositorio de clase ([`apps_services` / `clase-10-Taller-3`](https://github.com/Juanmorales177809/apps_services/tree/clase-10-Taller-3)).

## Actividad 2 (modelo conceptual)

En código reutilizable para las actividades 4 y 5:

- `app/domain/actividad2.py` — roles, scopes por rol, estados del ticket, transiciones y prioridades.

## Actividad 3 (lo implementado aquí)

- Conexión con `DATABASE_URL` y tablas en el schema `DB_SCHEMA` (definidos en `.env`).
- Modelos SQLAlchemy: `usuarios`, `laboratorios`, `servicios`, `tickets`.
- Esquemas Pydantic y endpoints:

| Método | Ruta |
|--------|------|
| POST | `/usuarios/` |
| GET | `/usuarios/` |
| GET | `/usuarios/me` *(JWT)* |
| GET | `/usuarios/{id_usuario}` |
| POST | `/auth/token` |
| POST | `/laboratorios/` |
| GET | `/laboratorios/` |
| GET | `/laboratorios/{id_laboratorio}` |
| POST | `/servicios/` |
| GET | `/servicios/` |
| GET | `/servicios/{id_servicio}` |
| POST | `/tickets/` *(JWT, scope `tickets:crear`)* |
| GET | `/tickets/` *(JWT, `tickets:ver_propios`; admin ve todos)* |
| GET | `/tickets/{id_ticket}` *(JWT)* |
| PATCH | `/tickets/{id_ticket}/estado` *(JWT; scope según transición)* |

Al iniciar la aplicación se ejecuta `CREATE SCHEMA IF NOT EXISTS` y `create_all` sobre ese schema (entorno de laboratorio). Para migraciones formales conviene introducir Alembic más adelante.

## Actividad 4 (autenticación JWT)

- **POST `/auth/token`** — cuerpo *form* OAuth2: `username` = correo del usuario, `password` = contraseña. Respuesta: `access_token` y `token_type` (`bearer`).
- El token incluye en el payload: `sub` (correo), `id_usuario`, `rol`, `scopes` (lista según `ROLE_SCOPES` en `app/domain/actividad2.py`) y `exp`.
- Contraseñas: **bcrypt** al crear usuario (`POST /usuarios/`) y verificación en el login.
- **Dependencias** en `app/deps.py`: `get_auth_context` (JWT + validación de scopes con `SecurityScopes`) y `get_current_user` (alias cómodo para rutas solo autenticadas).
- **Ruta protegida de ejemplo:** **GET `/usuarios/me`** — sin `Authorization: Bearer` responde **401**.

### Probar en Swagger

1. `POST /usuarios/` — crear usuario con correo y contraseña.
2. `POST /auth/token` — enviar el mismo correo en `username` y la contraseña en `password`.
3. Copiar `access_token` → botón **Authorize** → pegar `Bearer <token>` o solo el token (Swagger añade `Bearer` según configuración).
4. Ejecutar **GET `/usuarios/me`** y comprobar **200**; sin autorizar, **401**.

## Actividad 5 (autorización con scopes y reglas de negocio)

- **`SecurityScopes`** (vía `get_auth_context`): si el token no incluye el scope exigido por la ruta → **403**.
- **Tickets** (siempre con Bearer):
  - **POST /** exige `tickets:crear`. El **solicitante** solo puede usar su propio `id_solicitante`; **admin** puede crear en nombre de otro.
  - **GET /** y **GET /{id}** exigen `tickets:ver_propios`. Quien tiene `tickets:ver_todos` (**admin**) lista todos; el resto solo ve tickets donde es solicitante, responsable o asignado. Ver un ticket ajeno → **403**.
  - **PATCH /{id}/estado**: el scope necesario depende del par **estado actual → nuevo** (tabla de transiciones en `app/domain/actividad2.py`). Transición no listada → **422**. Además: en **recibido → asignado** debe enviarse **`id_asignado`** (usuario **auxiliar** o **tecnico_especializado**); en **asignado/en_proceso → en_proceso/en_revision** solo el **asignado** o **admin**; en **en_revision → terminado** solo el **responsable** registrado en el ticket o **admin**.
- Reglas auxiliares: `app/domain/ticket_rules.py`.

## Configuración

1. Python 3.10+ y PostgreSQL en ejecución.
2. Crea la base de datos que uses en `DATABASE_URL` (el usuario PostgreSQL debe poder crear objetos en el schema indicado).
3. Copia variables en `.env`:
   - `DATABASE_URL`
   - `DB_SCHEMA` — nombre del schema **asignado por el docente**
   - `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` (JWT; actividad 4)

4. Entorno virtual e instalación:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

5. Ejecutar la API:

```powershell
uvicorn app.main:app --reload
```

Documentación interactiva: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Integrantes

_(Completa con nombres y aportes para la entrega final.)_
