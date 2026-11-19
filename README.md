# API REST de práctica: SAST y SCA

API Flask local con fallos **intencionales** para el laboratorio de DevSecOps: una clave fija en el código, una consulta SQL vulnerable y dependencias desactualizadas. Usa únicamente los datos ficticios incluidos; no agregues credenciales reales ni la expongas a una red pública.

Repositorio remoto: [Mini-Sprint-DevSecOps](https://github.com/Xmarcelo05/Mini-Sprint-DevSecOps)

---

## 🏛️ Arquitectura del Sistema

- **Tipo**: Microservicio / API REST monolítica ligera.
- **Framework Web**: Python Flask.
- **Capa de Persistencia**: SQLite 3 local (`practica.db`), inicializada en tiempo de ejecución con la tabla `users` (`id`, `username`, `password`).
- **Autenticación y Autorización**:
  - `GET /api/profile`: Validación estática de API Key mediante el encabezado `X-API-Key`.
  - `POST /api/login`: Validación de credenciales de usuario contra SQLite.

---

## 🚀 Requisitos y Ejecución Local

1. Abre PowerShell en esta carpeta.
2. Crea y activa el entorno virtual:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Instala las dependencias del escenario vulnerable:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Inicia la API:

   ```powershell
   python app.py
   ```

La API escucha en `http://127.0.0.1:5000`. Al iniciar crea `practica.db` con usuarios ficticios (`admin` y `estudiante`).

---

## 📡 Endpoints Disponibles

| Método | Endpoint | Cabeceras / Parámetros | Descripción |
|---|---|---|---|
| `GET` | `/api/health` | Ninguna | Comprueba que la API esté activa (`{"status": "ok"}`). |
| `GET` | `/api/profile` | `X-API-Key: API_KEY_DEMO_NO_USAR_EN_PRODUCCION` | Devuelve información de perfil si la API Key es válida. |
| `POST` | `/api/login` | `Content-Type: application/json` | Recibe `{"username": "...", "password": "..."}` y autentica contra BD. |

---

## 🔍 Análisis Inicial de Seguridad (Code Review)

1. **Inyección SQL (CWE-89) [Crítico]**:
   - En `app.py` (`POST /api/login`), se concatenan los campos `username` y `password` directamente en la consulta SQL (`query = "SELECT ... WHERE username = '" + username + "' ..."`).
   - Detectado por Bandit con código `B608:hardcoded_sql_expressions`.
   - Permite evadir la autenticación con payloads como `' OR '1'='1` o `admin' --`.
2. **Secreto en Código Fuente (CWE-798) [Alto]**:
   - En `app.py`, la constante `API_KEY` se encuentra en texto plano dentro del código versionado.
3. **Contraseñas en Texto Plano (CWE-256) [Alto]**:
   - La tabla `users` almacena las contraseñas sin hashing criptográfico.
4. **Vulnerabilidades de Dependencias (SCA - CWE-1395) [Alto]**:
   - `pip-audit` detectó **54 vulnerabilidades conocidas** asociadas a versiones obsoletas de `Flask 2.2.2`, `Werkzeug 2.2.2`, `requests 2.20.0`, `idna 2.7` y `urllib3 1.24.3`.

---

## 📋 Gestión Ágil y Backlog (Sprint 1)

El proyecto cuenta con un tablero ágil y Backlog gestionado en GitHub:
- **Milestone**: [Sprint 1 - Mini-Sprint DevSecOps](https://github.com/Xmarcelo05/Mini-Sprint-DevSecOps/milestone/1)
- **Issues en Backlog**:
  1. [#1 [SCA] Actualizar librería requests y dependencias vulnerables en requirements.txt](https://github.com/Xmarcelo05/Mini-Sprint-DevSecOps/issues/1)
  2. [#2 [SAST] Mitigar vulnerabilidad de Inyección SQL en endpoint /api/login](https://github.com/Xmarcelo05/Mini-Sprint-DevSecOps/issues/2)
  3. [#3 [SECRETS] Eliminar API Key hardcodeada en app.py y gestionar secretos con variables de entorno](https://github.com/Xmarcelo05/Mini-Sprint-DevSecOps/issues/3)
  4. [#4 [AUTH] Implementar hashing criptográfico de contraseñas en BD](https://github.com/Xmarcelo05/Mini-Sprint-DevSecOps/issues/4)

---

## ✅ Definition of Done (DoD)

Para considerar una tarea como completada, se deben satisfacer los criterios establecidos en [DOD.md](file:///C:/Users/Marcelo/Downloads/api_rest_practica/DOD.md), destacando dos **criterios de seguridad obligatorios**:

1. **Escaneo de Seguridad Limpio (SAST y SCA)**:
   - Bandit debe ejecutarse (`bandit -r app.py`) sin alertas de severidad media ni alta.
   - `pip-audit -r requirements.txt` no debe reportar vulnerabilidades conocidas (CVEs).
2. **Revisión por Pares (Peer Review)**:
   - Todo código debe ser revisado y aprobado formalmente por otro compañero mediante Pull Request antes de fusionarse a la rama `main`.
