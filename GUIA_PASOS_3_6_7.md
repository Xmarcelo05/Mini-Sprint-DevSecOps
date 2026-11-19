# Guía de ejecución y evidencias: pasos 3, 6 y 7

## Antes de comenzar

El repositorio contiene el escenario vulnerable en su historial. Conserven la evidencia del PR rojo antes de integrar las correcciones; no publiquen la API vulnerable. Los cambios locales de remediación se deben revisar y subir mediante una rama y PR, no directamente a `main`.

## Paso 3 — cada integrante, en su propio equipo

En PowerShell, desde la carpeta del repositorio (requiere Python 3.10+ y Git):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pre-commit
pre-commit install
```

Para demostrar el rechazo, usar una cadena **ficticia**, nunca una credencial real. Comprobar primero que no exista el archivo `prueba-secreto-temporal.txt`. El siguiente comando genera una cadena que imita una clave AWS, sin usar ninguna credencial real:

```powershell
'aws_access_key_id = ' + ('AK' + 'IA') + ('A' * 16) | Set-Content -Encoding utf8 prueba-secreto-temporal.txt
git add prueba-secreto-temporal.txt
pre-commit run detect-secrets --files prueba-secreto-temporal.txt
```

El hook debe indicar `Failed`. Solo si fue detectada, intentar el commit específico:

```powershell
git commit --only -m "test: comprobar bloqueo de secreto ficticio" -- prueba-secreto-temporal.txt
```

El commit debe ser rechazado. Tomar una captura con el nombre del integrante y el resultado; luego limpiar:

```powershell
git restore --staged -- prueba-secreto-temporal.txt
Remove-Item prueba-secreto-temporal.txt
```

Si no se detecta, detenerse y revisar la instalación/configuración; no subir la cadena ni actualizar el baseline para aceptarla. No ejecutar la prueba sobre un archivo que contenga datos propios. Cada integrante repite el procedimiento; el hook se instala por clon, no se comparte automáticamente.

## Paso 6 — remediación y comprobación

1. Asignar las issues #1–#4 y moverlas a In Progress al iniciar. Guardar primero la captura del PR vulnerable y su pipeline rojo.
2. Crear una rama desde `main` antes de hacer commits (con los cambios locales ya preparados, `git switch -c remediacion/devsecops`). No sobrescribir cambios ajenos.
3. Revisar los cambios: dependencias, consulta SQL parametrizada, API key en entorno, contraseñas con hash y pruebas. Seguir el README para configurar `.env` y ejecutar la API. No subir `.env` ni bases de datos.
4. Ejecutar pruebas, Bandit y pip-audit con los comandos del README. Si hay hallazgos, corregirlos y volver a ejecutar. Probar también los endpoints y el rechazo de SQL injection.
5. El archivo `sbom-remediado.json` registra un entorno limpio con dependencias resueltas. Para regenerarlo, crear otro entorno limpio e instalar allí solo los requisitos de la aplicación. Desde el entorno donde está instalado `cyclonedx-bom`, ejecutar:

   ```powershell
   py -3.12 -m venv .venv\sbom312
   .\.venv\sbom312\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\py312\Scripts\python.exe -m pip install cyclonedx-bom
   .\.venv\py312\Scripts\python.exe -m cyclonedx_py environment .\.venv\sbom312\Scripts\python.exe -o sbom-remediado.json
   ```

   El inventario también incluye `pip` del entorno de generación. La auditoría `pip-audit -r requirements.txt` se refiere a las dependencias de la aplicación, no al propio pip. Los rangos pueden resolverse de forma diferente; repetir la auditoría en CI.
6. Crear commits, publicar la rama y abrir un PR a `main` que referencie las issues. Solicitar aprobación de otro integrante y comprobar el pipeline verde. Configurar en GitHub la protección de `main` para exigir el check de seguridad y revisión cuando esté disponible; el YAML por sí solo no bloquea un merge.
7. Después de la revisión y comprobaciones, actualizar el tablero y capturar su estado final.

## Paso 7 — presentación y PDF

Guion sugerido para 5 minutos: hallazgos iniciales (SQL, secretos, contraseñas y dependencias); tablero y reparto; pipeline rojo frente a verde; correcciones; lección sobre integrar seguridad en el flujo.

Lista de evidencias del PDF:

- [ ] Enlace al repositorio y participantes.
- [ ] Capturas del tablero al inicio y actualizado.
- [ ] Evidencia del rechazo de secreto de cada integrante (sin credenciales reales).
- [ ] Tabla SCA con hallazgos iniciales, decisiones y resultado posterior verificado.
- [ ] Captura del PR vulnerable con ejecución fallida.
- [ ] Captura del PR final con check verde y aprobación de otro integrante.
- [ ] Conclusiones y lecciones. Exportar el documento del laboratorio a PDF.

No afirmar que una herramienta pasó, una revisión ocurrió o que se tienen cero CVE hasta comprobarlo y guardar la evidencia.
