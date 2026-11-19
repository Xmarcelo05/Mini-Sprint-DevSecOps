# API REST: Mini-Sprint DevSecOps

API Flask de laboratorio para demostrar detección y remediación de vulnerabilidades. Solo para uso local; no es una aplicación lista para producción.

- Repositorio: https://github.com/Xmarcelo05/Mini-Sprint-DevSecOps
- [Guía del equipo: pasos 3, 6 y 7](GUIA_PASOS_3_6_7.md)
- [Definition of Done](DOD.md) · [Tabla SCA inicial](TABLA_DE_DECISIONES_SCA.md)
- Backlog: [dependencias #1](https://github.com/Xmarcelo05/Mini-Sprint-DevSecOps/issues/1), [SQL #2](https://github.com/Xmarcelo05/Mini-Sprint-DevSecOps/issues/2), [secretos #3](https://github.com/Xmarcelo05/Mini-Sprint-DevSecOps/issues/3), [contraseñas #4](https://github.com/Xmarcelo05/Mini-Sprint-DevSecOps/issues/4).

## Instalación y ejecución (PowerShell, Python 3.10+)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Editar `.env`: establecer una `API_KEY` privada y `DEMO_ADMIN_PASSWORD` para crear el usuario `admin` de prueba. No compartir ni subir `.env`. Las variables existentes del sistema tienen prioridad sobre `.env`.

```powershell
python app.py
```

La API escucha únicamente en `127.0.0.1:5000`. El usuario `admin` se crea solo si no existe y se ha configurado `DEMO_ADMIN_PASSWORD`; cambiar la variable después no cambia la contraseña ya guardada. Las contraseñas se guardan como hashes.

**Base anterior:** si `practica.db` proviene de la versión vulnerable, respaldarla y eliminarla únicamente si contiene datos de prueba descartables. La aplicación rechaza el esquema anterior; no migra datos automáticamente. Reiniciar para crear la nueva base. Nunca borrar datos reales sin un plan de migración.

## Endpoints

- `GET /api/health`: estado de la API.
- `GET /api/profile`: requiere la cabecera `X-API-Key`; devuelve 503 si no está configurada.
- `POST /api/login`: JSON con `username` y `password`; consulta parametrizada y verificación de hash.

La API sigue siendo didáctica: no incluye registro de usuarios, limitación de intentos ni controles de producción.

## Comprobaciones

```powershell
python -m pip install bandit pip-audit pre-commit
python -m unittest discover -s tests -v
bandit -r app.py
pip-audit -r requirements.txt
pre-commit install
pre-commit run --all-files
```

La tabla y `sbom.json` describen el escenario inicial vulnerable. La remediación debe comprobarse con una nueva auditoría y un nuevo SBOM, ya que los resultados dependen de las versiones resueltas y la fecha. El pipeline ejecuta pruebas, Bandit y pip-audit; la protección de rama debe configurarse en GitHub por separado.
