## Descripción del Cambio
<!-- Describe brevemente el problema solucionado y los cambios implementados -->

Closes #<!-- Número del Issue relacionado -->

---

## Lista de Verificación - Definition of Done (DoD)

### Criterios Obligatorios de Seguridad 🔒
- [ ] **Escaneo SAST con Bandit**: Se ejecutó `bandit -r app.py` y no existen alertas de severidad Media ni Alta.
- [ ] **Escaneo SCA con pip-audit**: Se ejecutó `pip-audit -r requirements.txt` y no existen vulnerabilidades Críticas ni Altas en librerías.
- [ ] **Revisión de Secretos**: Se confirmó que no hay API Keys, contraseñas ni tokens hardcodeados en el código ni en el commit.
- [ ] **Aprobación por Pares (Peer Review)**: Requiere la aprobación de al menos un compañero antes de fusionar.

### Criterios Funcionales y de Calidad
- [ ] Los endpoints fueron probados localmente y responden según lo esperado.
- [ ] Pruebas contra inyecciones SQL u otros vectores de ataque ejecutadas satisfactoriamente.
- [ ] Variables de entorno documentadas en `.env.example` si aplica.
