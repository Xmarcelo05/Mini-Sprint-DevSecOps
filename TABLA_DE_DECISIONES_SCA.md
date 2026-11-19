# Tabla de Decisiones de Mitigación SCA (Software Composition Analysis)

> **Registro inicial:** la tabla conserva los resultados y propuestas documentados para las dependencias vulnerables. Los identificadores, severidades y versiones deben verificarse con el informe original y fuentes oficiales. La remediación actual aún requiere una nueva auditoría y evidencia; las versiones propuestas abajo no garantizan por sí solas una instalación segura.

## 📌 Proyecto: Mini-Sprint DevSecOps
- **Herramienta SBOM:** CycloneDX (`python -m cyclonedx_py requirements requirements.txt -o sbom.json`)
- **Herramienta SCA:** `pip-audit` v2.10.1
- **Archivo auditado:** `requirements.txt`
- **Total de vulnerabilidades encontradas:** 54 conocidas en 5 componentes.

---

### 🛡️ Tabla de Decisiones de Mitigación

| Componente | Versión Actual | Identificadores / CVEs Relevantes | Severidad | Descripción del Riesgo | Versión de Corrección (Fix) | Decisión de Mitigación (Acción DevSecOps) |
|---|---|---|---|---|---|---|
| **Flask** | `2.2.2` | `PYSEC-2023-62` (CVE-2023-30861)<br>`PYSEC-2026-2151` | **Alta** | Divulgación de cookies de sesión sin firma ante configuraciones específicas; fallos en manejo de rutas. | `3.1.3` (o `3.0.x`) | **Actualizar**: Migrar `Flask` en `requirements.txt` a `>= 3.0.3` / `3.1.3` para eliminar vectores de fuga de sesión. |
| **Werkzeug** | `2.2.2` | `PYSEC-2023-57`, `PYSEC-2023-58`<br>`PYSEC-2023-221` (CVE-2023-46136)<br>`PYSEC-2026-2043`, `PYSEC-2026-2044`<br>`PYSEC-2026-3417`, `PYSEC-2026-4312` | **Crítica** | Denegación de servicio (DoS) por agotamiento de memoria y parsing multipart malformado; bypass de routing. | `3.1.9` (o `>= 3.0.6`) | **Actualizar**: Desacoplar versión fija antigua y fijar `Werkzeug >= 3.0.6` compatible con Flask 3. |
| **requests** | `2.20.0` | `PYSEC-2023-74` (CVE-2023-32681)<br>`PYSEC-2026-1872`, `PYSEC-2026-1873`<br>`PYSEC-2026-2275` | **Alta** | Fuga inadvertida de cabecera `Proxy-Authorization` en redirecciones HTTP hacia hosts no confiables. | `2.32.4` / `2.33.0` | **Actualizar**: Actualizar `requests` en `requirements.txt` a `>= 2.32.3` / `2.33.0`. |
| **idna** *(transitiva)* | `2.7` | `PYSEC-2024-60` (CVE-2024-3651)<br>`PYSEC-2026-215` | **Media / Alta** | Denegación de servicio (DoS) por procesamiento de nombres de dominio IDNA excesivamente largos (ReDoS). | `3.7` / `3.15` | **Mitigación por Transitividad**: Al actualizar `requests >= 2.32.0`, pip resolverá automáticamente `idna >= 3.7`. |
| **urllib3** *(transitiva)* | `1.24.3` | `PYSEC-2020-148` (CVE-2020-26137)<br>`PYSEC-2023-192`, `PYSEC-2023-212`<br>`PYSEC-2026-1995`, `PYSEC-2026-4177` | **Alta** | Inyección CRLF en peticiones HTTP; fuga de cookies en redirecciones cruzadas entre esquemas. | `2.2.2` / `2.8.0` | **Mitigación por Transitividad**: Al actualizar `requests`, se instalará automáticamente `urllib3 >= 2.0.0`. |

---

### 📝 Resumen Ejecutivo de Acciones para el Backlog:
1. **requirements.txt propuesto para remediación**:
   ```text
   Flask>=3.0.3
   Werkzeug>=3.0.6
   requests>=2.32.3
   ```
2. **Resultado posterior local (19/11/2026):** `pip-audit -r requirements.txt` informó `No known vulnerabilities found` al resolver las dependencias corregidas. Las cinco pruebas funcionales pasaron y Bandit no reportó hallazgos en `app.py`. Repetir los controles en el PR: los resultados pueden cambiar según la fecha y las versiones resueltas. La aplicación no utiliza `requests`, por lo que se retiró de sus dependencias; Werkzeug se resuelve como dependencia de Flask.
3. **SBOM posterior:** `sbom-remediado.json` inventaría un entorno limpio con Flask 3.1.3, Werkzeug 3.1.9 y python-dotenv 1.2.4, entre otras dependencias. Incluye también el `pip` del entorno; el comando de auditoría anterior cubre los requisitos de la aplicación, no el propio pip.
