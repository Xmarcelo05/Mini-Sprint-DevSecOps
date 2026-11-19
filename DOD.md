# Definition of Done (DoD) - Mini-Sprint DevSecOps

Para dar cualquier tarea o historia de usuario por **TERMINADA (DONE)** dentro del ciclo de desarrollo del proyecto, se deben cumplir obligatoriamente todos los criterios técnicos, funcionales y de seguridad descritos a continuación.

---

## 1. Criterios de Seguridad Obligatorios (Security Gate) 🔒

Antes de que un cambio pueda integrarse a la rama principal (`main`), debe superar indefectiblemente los siguientes controles de seguridad:

1. **Escaneo de Seguridad SAST y SCA Limpio (Static Analysis & Dependency Gate)**:
   - **SAST (Bandit)**: El código debe pasar el escaneo automatizado de Bandit (`bandit -r app.py`) con **0 alertas de severidad Alta o Media** (especialmente verificando CWE-89 de SQLi y CWE-798 de Hardcoded Secrets).
   - **SCA (pip-audit)**: El análisis de dependencias (`pip-audit -r requirements.txt`) no debe contener vulnerabilidades conocidas (CVEs) de severidad Crítica o Alta sin mitigar.
2. **Revisión por Pares Obligatoria (Peer Review Gate)**:
   - Todo cambio debe someterse mediante un **Pull Request (PR)**.
   - Es mandatorio contar con la revisión y aprobación formal de al menos **otro compañero de equipo** antes de realizar el merge.
   - El revisor debe validar que no se expongan credenciales, tokens o secretos en el código ni en el historial de commits.

---

## 2. Criterios de Calidad y Funcionalidad 🧪

- **Pruebas Funcionales**: Los endpoints modificados deben ser probados localmente (`/api/health`, `/api/profile`, `/api/login`) verificando respuestas HTTP correctas (códigos 200, 400, 401, etc.).
- **Pruebas de Resistencia ante Inyecciones**: Se debe comprobar que los payloads de ataque (por ejemplo, `' OR '1'='1`) sean rechazados adecuadamente.
- **Gestión de Configuración y Secretos**: Ningún secreto, API Key o credencial debe residir en texto plano en el repositorio. Toda variable sensible debe obtenerse mediante variables de entorno (`.env` local, excluido en `.gitignore`).

---

## 3. Criterios de Documentación y Entrega 📋

- **Item de Backlog / Issue Asociado**: El Pull Request debe referenciar el Issue del Backlog que resuelve (ej. `Closes #1`, `Closes #2`).
- **Documentación Actualizada**: Si la modificación cambia la forma de consumir un endpoint o requiere nuevas variables de entorno, el archivo `README.md` y `.env.example` deben ser actualizados.
- **Rama Limpia**: La rama debe estar actualizada respecto a `main` y no contener conflictos.
