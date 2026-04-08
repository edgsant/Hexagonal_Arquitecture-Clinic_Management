# Práctica DIAS – Grupo Foxtrot

## Integrantes
- Edgar Santiesteban Mendo
- Marcos Palatino Álvarez Fulconis
- Hugo Adan de la Fuente

## Repositorio
URL del repositorio GitLab:
    https://gitlab.inf.uva.es/edgsant/dias2526-foxtrot

## Estructura y trabajo
La rama main tendrá temporalmente la estructura base de la practica (carpetas y readme sin completar)

Para trabajar correctamente en GitLab, cosas a recordar:
### Trabajo con ramas
Se recomienda no trabajar directamente sobre la rama principal (main o master). Cada cambio
relevante debería desarrollarse en una rama específica, creada a partir de la rama principal.
Conviene utilizar nombres de rama descriptivos y homogéneos. Por ejemplo:
- feature/cu01-login
- feature/modelo-dominio
- feature/api-pacientes
- fix/validacion-fecha
- docs/readme
- test/cu03-procedimiento
La idea es que cada rama represente una tarea o cambio acotado, de forma que su propósito sea fácil de entender
### Uso de merge requests
La integración del trabajo en la rama principal debería realizarse preferentemente mediante
merge requests en GitLab. No se recomienda hacer push directo a la rama principal salvo en casos
excepcionales y justificados.
Cada merge request debería:
- tener un título claro y descriptivo;
- agrupar cambios relacionados entre sí;
- incluir una breve explicación de lo realizado;
- permitir que otro integrante del grupo revise el trabajo antes de integrarlo.
Siempre que sea posible, se recomienda que las merge requests sean pequeñas y frecuentes, en lugar de acumular muchos cambios en una única integración final.
###  Revisión del trabajo
El uso de GitLab debe reflejar una colaboración real entre los miembros del grupo. Por ello, se
recomienda revisar el trabajo de los compañeros antes de aceptar una merge request, comprobando
al menos:
- que el cambio tiene sentido respecto al caso de uso o artefacto trabajado;
- que no rompe la estructura general del proyecto;
- que mantiene la coherencia con el análisis, el diseño y la implementación;
- que la documentación y los nombres utilizados son comprensibles.
No se busca una revisión exhaustiva como en un entorno profesional, pero sí una evidencia
mínima de trabajo coordinado y validación entre iguales.
### Mensajes de commit
<tipo>: <descripción en minúsculas y lenguaje imperativo>
- feat: nueva funcionalidad;
- fix: corrección de errores;
- docs: cambios en documentación;
- test: incorporación o modificación de pruebas;
- refactor: reorganización interna del código sin cambiar el comportamiento esperado;
- chore: tareas auxiliares de configuración o mantenimiento

---

# 1. Introducción
Breve descripción del sistema y del objetivo de la práctica.

---

# 2. Alcance del trabajo
## Funcionalidad trabajada
- CU01 - Iniciar sesión
- CU02 - Registrar paciente
- ...
## Decisiones sobre el alcance funcional
Indicar qué aspectos de los casos de uso se han simplificado, omitido o adaptado durante el desa---
# 3. Modelo de dominio
## 3.1 Clases identificadas
Descripción de las principales clases del dominio.
## 3.2 Diagrama de dominio
![Dominio](docs/diagramas/dominio.png)
## 3.3 Comentarios
Explicación de decisiones tomadas.
---
# 4. Modelo de análisis
## 4.1 Casos de uso
Descripción breve.
## 4.2 Clases de análisis
Explicación de su papel.
## 4.3 Diagramas de secuencia
![Secuencia](docs/diagramas/analisis_secuencia.png)
## 4.4 Comentarios
Decisiones importantes.
---
# 5. Diseño
## 5.1 Arquitectura
Describir la arquitectura del sistema basada en la separación en capas (domain, application, inf- el papel de cada capa
- las responsabilidades principales
- cómo se relacionan entre sí
## 5.2 Diagrama de arquitectura
![Arquitectura](docs/diagramas/arquitectura.png)
## 5.3 Diseño de clases
![Clases](docs/diagramas/diseno_clases.png)
## 5.4 Decisiones de diseño
Describir las principales decisiones de diseño adoptadas, incluyendo:
- uso de patrones (si aplica)
- asignación de responsabilidades entre clases y capas
- organización del código
Por cada decisión relevante, justificar:
- qué problema resuelve
- cómo se relaciona con los casos de uso y el modelo de análisis
- qué impacto tiene en la implementación
---
# 6. Implementación
## 6.1 Estructura del código
Explicación de carpetas.
## 6.2 Tecnologías
Lenguaje, librerías, herramientas.
## 6.3 Descripción
Cómo se ha implementado la funcionalidad.
## 6.4 Ejecución
### Instalación
```bash
poetry install
poetry run python -m app.main #Este es un ejemplo
```
# 7. Pruebas
## 7.1 Estrategia
Qué se prueba y por qué.
## 7.2 Tests implementados
Descripción breve.
## 7.3 Ejecución
```bash
poetry run pytest # Esto es un ejemplo
```
## 7.4 Cobertura (opcional)
# 8. Trazabilidad
| **Caso de uso** | **Dominio** | **Análisis** | **Diseño** | **Código** | **Test** |
| ------------- | ----------- | ------------ | ---------- | ---------- | -------------- |
| CUxx | Clase X | Secuencia Y | Servicio Z | modulo.py | test_modulo.py |
# 9. Planificación
Explicar cómo se ha organizado el trabajo durante las 8 semanas.
# 10. Conclusiones
- Dificultades
- Decisiones
- Aprendizaje
- Mejoras futuras
# Anexo I
## Videodefensa
<Enlace a la videodefensa>