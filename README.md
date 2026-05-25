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
(Breve descripción del sistema y del objetivo de la práctica.)
El proyecto a desarrollar consiste en un sistema web para la gestión de pacientes en una clínica urológica. 
El sistema tratará el seguimiento y trazabilidad del expediente de un paciente desde su registro, sus consultas y las pruebas médicas solicitadas junto a aquellos especialistas que las realizaron.
El objetivo de esta practica es aplicar los conocimientos de la asignatura Diseño, Integración y Adaptación de Software para un sistema y aplicando los 5 flujos de trabajo; Requisitos, Análisis, Diseño, Implementación y Pruebas.
Se partirá de un documento que ya recoge el análisis del workflow de Requisitos, en docs/requisitos/documento-de-requisitos.

---

# 2. Alcance del trabajo
Este proyecto solo tratará un subconjunto acotado de funcionalidad del sistema clínico descrito en el enunciado para los flujos de trabajo de Análisis, Diseño e Implementación.

## Funcionalidad trabajada
El sistema solo abarcará los siguientes casos de uso:
- CU01 - Iniciar sesión
- CU02 - Registrar paciente
- CU03 - Crear procedimiento clínico
- CU04 - Registrar informe clínico inicial
- CU05 - Registrar resultados de analítica
- CU06 - Consultar procedimiento clínico
- CU07 - Dar de alta al paciente

## Decisiones sobre el alcance funcional
Para simplificar el sistema a desarrollar, se han tomado las siguientes decisiones:
- Gestión de Especialistas: Todos los especialistas estarán ya dados de alta en el sistema, no se tratará las funcionalidades de dar de alta o gestionar sus cuentas.
- Gestión de citas: El sistema no gestiona las citas o agendas de los pacientes, se asumirá que para las consultas o pruebas el paciente ya fue citado externamente.
- Almacenamiento de pruebas: El sistema no gestiona la localización del almacenamiento de muestras de biopsias.

# 3. Modelo de dominio
## 3.1 Clases identificadas
- Paciente: El paciente que tiene o ha tenido un procedimiento y se le ha dado de alta en nuestro sistema. Contiene los datos personales de dicho paciente.
- Procedimiento: Clase 'contenedor' del historial del paciente. Contiene toda la información relacionada con un procedimiento del paciente; consultas, pruebas, informes, etc. El paciente solo puede tener un procedimiento activo en un momento dado.
- InformeInicial: Documento creado en la primera consulta cuando se inicia un procedimiento del paciente. Recoge antecedentes y analisis fisico inicial del paciente.
- ActoClinico: Clase abstracta que agrupa los distintos actos a los que se someterá un paciente durante un procedimiento, las consultas y las pruebas, con un unico atributo fecha para facilitar la trazabilidad temporal de nuestro sistema y la visión global de los actos realizados durante un procedimiento.
- Consulta: Interacción entre el paciente y un urólogo donde se evalúa al paciente y se toman decisiones clínicas (dar de alta o realizar una prueba)
- Prueba: Superclase que agrupa los distintos procedimientos clínicos a los que se puede someter un paciente durante su Procedimiento, junto a la consulta que solicitó la prueba.
- Analitica: Prueba clínica donde un AnalistaClinico recoge los valores de los datos obtenidos en laboratorio sobre el paciente. 
- PruebaRadiologica: Prueba clínica donde un Radiologo recoge los resultados de dos artefactos clínicos realizados sobre el paciente; la ResonanciaMagnetica y la Ecografia.  
- ResonanciaMagnetica: Artefacto clinico de una PruebaRadiologica.
- Ecografia: Artefacto clinico de una PruebaRadiologica.
- Biopsia: Prueba clínica realizada por un urólogo donde se le toman muestras a un paciente.
- Muestra: Muestras obtenidas durante una biopsia que deberán ser diagnositcadas por un anatomopatólogo. 
- Intervencion: Prueba clínica realizada por un Urólogo donde se realiza una cirugía quirúrgica al paciente

- Especialista: Superclase que agrupa todo el personal de la clínica. 
- Usuario: Usuario ya dado de alta que usará el especialista para acceder al sistema
- AnalistaClinico: Tipo de especialista encargado de recoger los datos en las Analiticas
- AnatomoPatologo: Tipo de especilista encargado de analizar las Muestras tomadas en las Biopsias
- Radiologo: Tipo de especialista encargado de tomar y analizar las PruebasRadiologicas y sus artefactos.
- Urologo: Tipo de especialista encargado de las consultas y seguimiento del paciente.

## 3.2 Diagrama de dominio
![Dominio](docs/diagramas/modelo-dominio/Modelo-de-Dominio-v3.png)
## 3.3 Comentarios
Durante el análisis del modelo de dominio se han tomado las siguientes decisiones para garantizar el cumplimiento de las reglas de negocio y simplificar el diseño y arquitectura del sistema:
- Superclase ActoClinico: Para evitar que un procedimiento clinico tenga diversas relaciones 'dispersas' entre consultas y pruebas, se ha modelado para que Procedimiento tenga una relación única con cada ActoClínico relevante durante el Procedimiento del paciente, asegurando que Procedimiento tenga el historial global y ordenado.
- Separación de Consulta y Prueba: Al requerir trazabilidad entre una Prueba y quien la realizó, y la consulta y el urólogo que la solicitó, se han modelado las dos clases Consulta y Prueba con una asociación entre ellas.
- Relación general entre especialista y ActoClinico vs especificacion:   
---
# 4. Modelo de análisis
## 4.1 Casos de uso
(Descripción breve.)


- CU01 - Iniciar Sesión: Este caso recoge el flujo de trabajo en el que un especialista (previamente registrado en el sistema) intenta iniciar sesión con su usuario y contraseña. Al realizarse correctamente el sistema debe identificar que especialista es el asociado a esa cuenta para darle el acceso a las funciones relacionadas con su rol, y en caso erroneo al introducir credenciales no válidas el se mostrará un error y NO se iniciará sesión. 


- CU02 - Registrar Nuevo Paciente: Este caso recoge el flujo de trabajo en el que un Urólogo con sesión iniciada previamente en el sistema, de de alta en nuestro sistema a un nuevo paciente. Una vez introducidos de manera correcta los datos asociados al paciente, quedará registrada su ficha en el sistema con los datos personales de ese paciente. En caso de confundirse el Urólogo al introducirlos, se mostrará un mensaje de error y deberá volver a introducirlos correctamente.


- CU03 - Crear procedimiento clínico: Este caso recoge el flujo de trabajo en el que un Urologo registra un procedimiento nuevo a un paciente ya registrado en el sistema que no tenga ningun procedimiento activo en el momento. En caso de que el paciente ya tenga un procedimiento activo, mostrara error y no registrara procedimientos nuevos.


- CU04 - Registrar informe clinico inicial: Este caso recoge el flujo de trabajo en el que un Urologo registra el informe inicial de un Paciente, sin flujos alternativos .


- CU05 - Registrar resultaddos de analitica: Este caso recoge el flujo de trabajo en el que un Analista clinico rellena una analitica pendiene de un procedimiento con los resultados de la prueba, sin flujos alternativos.


- CU06 - Consultar procedimiento clinico: Este caso recoge el flujo de trabajo en el que un Urologo consulta la lista de procedimientos clinicos que tiene a su disposicion y de ellos selecciona uno para consultar su informacion.


- CU07 - Dar de alta un paciente: Este caso recoge el flujo de trabajo en el que un Urologo decide cerrar el procedimiento de un paciente para darle el alta, sin flujos alternativos.

## 4.2 Clases de análisis
(Explicación de su papel.)

- CU01 - Iniciar sesión
![BCE CU01](docs/diagramas/CU01/Diagrama%20de%20analisis%20BCE%20-%20CU01.png)
El diagrama BCE de este caso de uso se compone del Actor Especialista, aquel que quiere iniciar sesion, relacionado con la clase Boundary AccesoInicioSesion que se encarga de la interacción entre el actor y el sistema, la clase Controller GestorInicioSesion y las clases Entity Usuario que es el usuario del sistema del Especialista y la Entity Especialista, que es la información asociada a dicho usuario sobre el especialista (datos personales, rol, etc)

- CU02 - Registrar paciente
![BCE CU02](docs/diagramas/CU02/Diagrama%20de%20analisis%20BCE%20-%20CU02.png)
El diagrama BCE de este caso de uso se compone del Actor Urólogo, aquel que quiere registrar al paciente, relacionado con la clase Boundary AccesoRegistroPaciente que se encarga de la interacción entre el actor y el sistema, la clase Controller GestorRegistroPaciente y la clase Entity Paciente.

- CU03 - Crear procedimiento clinico
![BCE CU03](docs/diagramas/CU03/Diagrama%20de%20analisis%20BCE%20-%20CU03.png)
El diagrama BCE de este caso de uso se compone del Actor Urólogo, aquel que quiere registrar el procedimiento, relacionado con la clase Boundary AccesoUrologo que se encarga de la interacción entre el actor y el sistema, la clase Controller GestorCrearProcedimiento y las clases Entity Paciente y Procedimiento.

- CU04 - Registrar informe clinico inicial
![BCE CU04](docs/diagramas/CU04/Diagrama%20de%20analisis%20BCE%20-%20CU04.png)
El diagrama BCE de este caso de uso se compone del Actor Urólogo, aquel que quiere registrar el informe clinico inicial, relacionado con la clase Boundary AccesoUrologo que se encarga de la interacción entre el actor y el sistema, la clase Controller GestorRegistroIncial y las clases Entity Paciente, Procedimiento, InformeInicial, Solicitud y Cosulta.

- CU05 - Registrar resultados de analitica
![BCE CU05](docs/diagramas/CU05/Diagrama%20de%20analisis%20BCE%20-%20CU05.png)El diagrama BCE de este caso de uso se compone del Actor Analista clinico, aquel que quiere registrar los resultados de la analitica, relacionado con la clase Boundary AccesoAnalista que se encarga de la interacción entre el actor y el sistema, la clase Controller GestorRegistrarResultados y las clases Entity Procedimiento y Analitica.

- CU06 - Consultar procedimiento clinico
![BCE CU06](docs/diagramas/CU06/Diagrama%20de%20analisis%20BCE%20-%20CU06.png)El diagrama BCE de este caso de uso se compone del Actor Urologo, aquel que quiere consultar un procedimiento clinico, relacionado con la clase Boundary AccesoUrologo que se encarga de la interacción entre el actor y el sistema, la clase Controller GestorConsultarProcedimiento y la clase Entity Procedimiento.

- CU07 - dar de alta un paciente
![BCE CU07](docs/diagramas/CU07/Diagrama%20de%20analisis%20BCE%20-%20CU07.png)El diagrama BCE de este caso de uso se compone del Actor Urologo, aquel que quiere consultar un procedimiento clinico, relacionado con la clase Boundary AccesoUrologo que se encarga de la interacción entre el actor y el sistema, la clase Controller GestorDarDeAlta y la clase Entity Procedimiento.

## 4.3 Diagramas de secuencia
- CU01 - Iniciar sesión:
![Secuencia CU01](docs/diagramas/CU01/Diagrama%20de%20secuencia%20-%20CU01.png)
- CU02 - Registrar paciente:
![Secuencia CU02](docs/diagramas/CU02/Diagrama%20de%20Secuencia%20-%20CU02.png)
- CU03 - Crear procedimiento:
![Secuencia CU03](docs/diagramas/CU03/Diagrama%20de%20secuencia%20-%20CU03.png)
- CU04 - Registrar informe clinico inicial:
![Secuencia CU04](docs/diagramas/CU04/Diagrama%20de%20secuencia%20-%20CU04.png)
- CU05 - Registrar resultados de analitica:
![Secuencia CU05](docs/diagramas/CU05/Diagrama%20de%20Secuencia%20-%20CU05.png)
- CU06 - Consultar procedimiento clinico:
![Secuencia CU06](docs/diagramas/CU06/Diagrama%20de%20Secuencia%20-%20CU06.png)
- CU07 - Dar de alta a un paciente
![Secuencia CU06](docs/diagramas/CU07/Diagrama%20de%20Secuencia%20-%20CU07.png)

## 4.4 Comentarios
(Decisiones importantes.)

- Desacoplamiento paciente-procedimiento-consulta:
Aunque en el caso real un paciente en nuestro sistema no existiría antes de una consulta inicial o sin procedimiento, se ha decidido que administrativamente 
el sistema permitirá el registro del paciente independientemente de sus procedimientos, y procedimientos nuevos independientes de las consultas, 
logrando desacoplar dependencias entre los casos de uso 2-Crear procedimiento, 3-Registrar Paciente y 4-Registrar informe inicial y evitando
bucles circulares en los diagramas de secuencia.


---
# 5. Diseño
## 5.1 Arquitectura
(Describir la arquitectura del sistema basada en la separación en capas (domain, application, inf-) el papel de cada capa)
- las responsabilidades principales
- cómo se relacionan entre sí


Nuestro sistema aplica una estructura hexagonal, dividiendo el sistema en las capas Domain, Application, Infraestructure, y Transversal.
Al aplicar este patron de diseño, nuestra estructura basada en capas mantiene el dominio como la capa más profunda para
evitar un fuerte acoplamiento de dependencias entre dominio e interfaces, bases de datos, etc.
Mantendríamos de esta forma las 3 capas definidas en la arquitectura hexagonal, donde las capas internas no dependen ni conocen 
las capas externas, mientras que las externas usan las funcionalidades ofrecidas por las internas.

### 5.1.1 Responsabilidades de cada capa.

- **Domain**: Esta capa se encarga de implementar la logica de negocio, siendo el corazon de la aplicacion y dependiendo de esta el resto de funcionalidades del sistema. Es una capa completamente independiente de la infraestructura: no busca entidades por identificador, no conoce la existencia de los repositorios ni gestiona el almacenamiento. Garantiza que el sistema siempre esté en un estado válido mediante entidades que protegen sus estados y aplican las reglas de negocio.

- **Application**: Esta capa se encarga de implementar los requisitos funcionales y los casos de uso, siendo la capa de servicios que da acceso al dominio de nuestro sistema.

- **Infrastructure**: Esta capa se encarga de proporcionar distintos tipos de adaptadores para enlazar nuestro sistema con distintos tipos de acceso a externos a nuestro sistema, gestionando tanto el acceso a datos como a otras funcionalidades del sistema como pueden ser los servicios.
    - **Presentation**: Adaptador de la capa de infraestructura que permite llevar nuestro sistema a la red a traves de peticiones HTTP.
    - **Persistence**: Adaptador encargado de implementar requisitos de informacion, encargandose de las distintas formas en las que nuestro sistema va a implementar la persistencia, buscando una forma utilizada en entornos de trabajo reales como puede ser una base de datos (persistencia real), y otra con la que poder testear las entidades puras, instanciando clases del dominio unicamente durante la ejecucion de nuestro sistema (repositorios en memoria -> persistencia NO real).

- **Transversal**: Capa que reúne utilidades usadas o que usarán el resto de capas, en nuestro caso conteniendo la clase que aplica el patrón factoría y el container encargado de la inyección de dependencias.

## 5.2 Diagrama de arquitectura
![Arquitectura](docs/diagramas/diagrama-arquitectura/Diagrama%20de%20arquitectura.png)
## 5.3 Diseño de clases
![Clases](docs/diagramas/diagrama-diseno/Clases%20de%20diseno.png)
## 5.4 Decisiones de diseño
(Describir las principales decisiones de diseño adoptadas, incluyendo:)
- uso de patrones (si aplica)
- asignación de responsabilidades entre clases y capas
- organización del código
Por cada decisión relevante, justificar:
- qué problema resuelve
- cómo se relaciona con los casos de uso y el modelo de análisis
- qué impacto tiene en la implementación

Se ha diseñado la implementación de nuestro sistema con las siguientes decisiones:
- Capa de dominio y alcance reducido:
Para la implementación de nuestro sistema, al tener que realizar una selección de casos de uso reducida (CU01-CU07) se ha decidido delimitar la implementación de las entidades de dominio a solo aquellas necesarias para ofrecer la implementación de los casos de uso cubiertos por nuestro alcance.

- Patrón Domain Model:
Se ha estructurado la capa de dominio acorde a la estructura hexagonal, encapsulando en la capa de dominio mediante clases de diseño interconectadas basadas en el modelo de dominio realizado, cada una con la responsabilidad de la lógica de negocio de su propia entidad equivalente del modelo de dominio y desacoplado de las capas de servicio e infraestructura.

- Modelo de Dominio Rico y Navegabilidad Unidireccional:
Se ha huido del antipatrón de "Modelo de Dominio Anémico". Nuestras entidades no son meros contenedores de datos, sino que poseen comportamiento (ej. Procedimiento.finalizar() comprueba que no haya analíticas pendientes).
    - Qué problema resuelve: Evita que la lógica de negocio se filtre a los servicios de aplicación. Además, para evitar la sobrecarga de memoria al instanciar grandes grafos de objetos desde la base de datos, se ha diseñado una navegabilidad unidireccional estricta entre agregados (ej. Procedimiento conoce a su Paciente, pero Paciente no tiene una lista infinita de procedimientos).

- Protección de fronteras mediante Inyección en Aplicación:
    - Qué problema resuelve: Cumpliendo la directriz de mantener el dominio limpio de búsquedas , se ha decidido que sea la capa de Aplicación (Servicios) la única autorizada para interactuar con los repositorios. El servicio recupera los objetos completos de la base de datos y se los inyecta al Dominio (ej. inyectar el objeto Paciente en el constructor de Procedimiento), evitando acoplar el Dominio a IDs relacionales o léxico de persistencia.

- Patrón Service Layer y Operation Script:
Se ha organizado la capa de aplicación como una Service layer, diseñando una clase ServicioCasoDeUso por cada caso de uso, interpretando cada caso de uso como una transacción atómica donde cada clase de esta capa se encargará de orquestar las clases de dominio y las interfaces de los repositorios encargados de la persistencia para controlar el flujo de cada caso de uso, permitiendo que nuestro sistema pueda ofrecer sus funcionalidades a distintos tipos de clientes mediante la capa infraestructura y aportando una capa de abstracción para simplificar las operaciones de la capa de dominio. 

- Patrón Repository:
Se ha diseñado el acceso a los datos de la capa de persistencia mediante Repositorios e interfaces de dichos repositorios para aportar abstracción sobre el acceso a datos, ahora orientado al dominio, permitiendo que la capa aplicación solo dependa de la capa dominio y no dependa ni conozca el léxico de la capa infraestructura.
Además, debido al alcance de la práctica, se ha aplicado el concepto de Aggregate Root, centralizando la persistencia en las entidades principales y evitando crear un repostiorio por entidad. De esta forma, se han diseñado 3 repositorios y sus respectivas interfaces que centralizan el acceso a los datos y proporcionan métodos oriantados al dominio, PacienteRepository, ProcedimientoRepository y UsuarioRepository.
    - Qué problema resuelve: En lugar de crear un DAO tradicional con las 4 operaciones CRUD (Create, Read, Update, Delete) que acoplaría el diseño a una base de datos relacional, los repositorios simulan colecciones en memoria y exponen únicamente los métodos que exigen los casos de uso (ej. obtener_activo_por_paciente()). Se omite deliberadamente la operación Delete por reglas de negocio hospitalarias (los historiales no se borran) y el principio YAGNI.

- Inyección de dependencias y capa transversal:
Se ha diseñado un contenedor en la capa Transversal encargado de instanciar las factorías, los repositorios y los servicios, resuelviendo el problema del alto acoplamiento.
Al inyectar los repositorios en los servicios a través de sus constructores, garantizamos que la capa de Aplicación sea completamente independiente de la tecnología de base de datos (SQLite o Memoria). Además, centralizar esta creación (Composition Root) facilita enormemente la inyección de dobles de prueba (Mocks) en fases de testing

- Patrón Page controller:
En la capa de presentación se ha utilizado el framework Flask mediante el uso de Blueprints para agrupar los endpoints web por recurso (Auth, Pacientes, Procedimientos).
Esta capa se encarga exclusivamente de extraer los datos de la red (JSON) y delegar la ejecución al Servicio correspondiente, aislando así a la lógica de negocio de la tecnología web.

---
# 6. Implementación
## 6.1 Estructura del código
(Explicación de carpetas.)
Se ha estructurado el codigo que implementa nuestro sistema con una estructura similar a la estructura hexagonal:


dias2526-foxtrot/
├── bruno/
│   └── nose                    # Punto de entrada de la aplicación (Levanta Flask y el Container)
├── docs/                       
│   ├── diagramas/              # Diagramas UML en formato .png y .svg (Dominio, BCE, Secuencia, Arquitectura y Diseño)
│   ├── requisitos/             # Documentos de análisis de requisitos inicial
│   └── src/                    # Código fuente de los diagramas realizados en Visual Paradigm
├── src/                        # Código fuente del sistema (Arquitectura Hexagonal)
│   ├── application/            # Capa de Aplicación (Orquestación de Casos de Uso)
│   │   ├── dtos/               
│   │   └── services/           
│   ├── domain/                 # Capa de Dominio (Corazón del negocio)
│   │   ├── entities/           
│   │   └── ports/              
│   ├── infrastructure/         # Capa de Infraestructura (Adaptadores externos)
│   │   ├── persistence/        
│   │   └── presentation/       
│   └── transversal/            # Capa Transversal (Utilidades transversales)
│       ├── config.py     
│       ├── container.py        
│       └── factory.py
├── tests/                      # Carpeta general para las pruebas automatizadas (Pytest)
│   ├── application/            
│   ├── domain/                 
│   └── infrastructure/         
├── pyproject.toml              # Configuración de librerías y dependencias (Poetry)
└── README.md                   # Documentación principal del repositorio


## 6.2 Tecnologías

Para el desarrollo de este proyecto se ha seleccionado un conjunto de tecnologías y herramientas usadas en las prácticas individuales que nos permiten el desarrollo e implementación de la Arquitectura Hexagonal y sus pruebas automatizas:

**Lenguaje y entorno**
* **Python:** Lenguaje principal del proyecto debido a su gran variedad de librerías. Se ha hecho un uso intensivo del tipado estático (*Type Hinting*) y del decorador nativo `@dataclass` para modelar las entidades de dominio y los DTOs puramente orientado a objetos.
* **Poetry:** Utilizado como gestor de dependencias y de entornos virtuales. 

**Frameworks y Librerías**
* **Flask:** Framework utilizado en la capa de Presentación como acceso a la web (Adaptador HTTP), implementando el patrón *Page Controller* mediante el uso de *Blueprints*.
* **flask-jwt-extended:** Extensión para la autenticación y autorización en la capa Presentación.
* **Dependency Injector:** Librería encargada de gestionar la Inyección de Dependencias en la capa Transversal (el *Composition Root* del sistema). Su uso ha sido vital para instanciar repositorios y servicios, permitiendo un alto nivel de desacoplamiento y facilitando la inyección de dobles de prueba (*mocks*) cuando es necesario.
* **SQLAlchemy:** Herramienta ORM utilizada en la capa de Infraestructura (Persistencia) que nos permite mapear las entidades a tablas de la base de datos relacional.
* **Python-dotenv:** Librería encargada de cargar variables de entorno desde archivos .env. Se ejecuta en el punto de entrada de la aplicación (main.py) para gestionar configuraciones sensibles (como URIs de bases de datos o claves secretas) de forma segura.

**Pruebas y Calidad del Código**
* **Pytest:** Framework seleccionado para la implementación y ejecución de la batería de pruebas automatizadas. Se ha escogido por su legibilidad, su aserciones nativas directas (`assert`) y su potente sistema de *fixtures*, idóneo para inyectar estados iniciales en los tests de los casos de uso.

**Herramientas de Desarrollo y Diseño**
* **Git y GitLab:** Utilizados para el control de versiones y el trabajo colaborativo, aplicando una estrategia de ramas (*Feature Branches*) y revisiones por pares mediante *Merge Requests* para asegurar la calidad antes de la integración.
* **Visual Paradigm:** Herramienta CASE empleada durante los flujos de Análisis y Diseño para la elaboración y mantenimiento de toda la documentación visual mediante diagramas UML (casos de uso, modelo de dominio, diagramas de secuencia y diseño arquitectónico).

## 6.3 Descripción de la Implementación

Dado que la estructura de clases refleja fielmente el diseño arquitectónico planteado en el apartado 5, la implementación de los casos de uso sigue un flujo de trabajo estandarizado y unidireccional. A continuación se describe el ciclo de vida real de una petición dentro del sistema, tomando como ejemplo los flujos de creación (ej. Registrar Paciente o Iniciar Sesión):

**1. Recepción y enrutamiento (Capa de Presentación)**
Las peticiones HTTP son capturadas por los *Blueprints* de Flask. El objetivo de esta capa se ha mantenido lo más fino posible: el *Blueprint* se limita a extraer el cuerpo de la petición (JSON) y verificar que el formato sea válido. No contiene lógica de negocio ni comprobaciones de campos específicos.

**2. Validación estructural (Capa de Aplicación - DTOs)**
Para evitar sobrecargar los servicios y aplicar el principio *Fail Fast* (fallar rápido), los datos extraídos se inyectan inmediatamente en un *Data Transfer Object* (DTO) de entrada específico para cada caso de uso (ej. `LoginRequestDTO`). El método `__post_init__` de estos DTOs es el encargado de realizar la validación temprana de los datos (comprobar nulos, strings vacíos y tipos correctos). Si el DTO es inválido, se lanza una excepción que Flask captura para devolver un error HTTP 400.

**3. Orquestación y Lógica (Capa de Aplicación - Servicios)**
Una vez construido el DTO válido, se pasa al Servicio correspondiente (ej. `ServicioIniciarSesion`). Al recibir un DTO garantizado estructuralmente, el servicio se centra puramente en orquestar el caso de uso: interactúa con los repositorios para recuperar datos previos, invoca métodos de las entidades del dominio si es necesario aplicar reglas de negocio, y devuelve un DTO de salida o lanza excepciones de negocio (ej. `UsuarioNoEncontradoException`).

**4. Reglas de Negocio (Capa de Dominio)**
Las Entidades del dominio (ej. `EntityPaciente`) son agnósticas a la red y a la base de datos. Se han implementado utilizando el decorador `@dataclass`. En esta capa reside la lógica intrínseca, asegurando en su instanciación que no existan estados inválidos según las normativas del hospital.

**5. Persistencia y Mapeo (Capa de Infraestructura)**
Los Repositorios Reales implementan las interfaces del dominio utilizando SQLAlchemy. Para mantener el dominio puro, se ha implementado un sistema de mapeo manual interno (`_a_entidad` y `_a_modelo`) dentro de cada repositorio. Cuando el servicio pide un dato, el repositorio consulta la base de datos mediante su `Model` de SQLAlchemy, lo mapea a una `Entity` pura del dominio y se lo devuelve al servicio, garantizando la total independencia tecnológica del núcleo.

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
| CUxx          | Clase X       | Secuencia Y | Servicio Z | modulo.py | test_modulo.py |
| **CU01 - Iniciar Sesión** | `Usuario`, `Especialista` | Diagrama de secuencia - CU01 | `ServicioIniciarSesion` | `ServicioIniciarSesion.py`, `AuthDTOs.py`, `EntityUsuario.py`, `EntityEspecialista.py` | `test_ServicioIniciarSesion.py` |
| **CU02 - Registrar paciente** | `Paciente` | Diagrama de Secuencia - CU02 | `ServicioRegistrarPaciente` | `ServicioRegistrarPaciente.py`, `PacienteDTOs.py`, `EntityPaciente.py` | `test_ServicioRegistrarPaciente.py` |
| **CU03 - Crear procedimiento clínico** | `Paciente`, `Procedimiento` | Diagrama de secuencia - CU03 | `ServicioCrearProcedimiento` | `ServicioCrearProcedimiento.py`, `ProcedimientoDTOs.py`, `EntityPaciente.py`, `EntityProcedimiento.py` | `test_ServicioCrearProcedimiento.py` |
| **CU04 - Registrar informe clínico inicial** | `Paciente`, `Procedimiento`, `InformeInicial`, `Consulta` | Diagrama de secuencia - CU04 | `ServicioRegistrarInformeInicial` | `ServicioRegistrarInformeInicial.py`, `InformeDTOs.py`, `EntityProcedimiento.py`, `EntityInformeInicial.py`, `EntityConsulta.py` | `test_ServicioRegistrarInformeInicial.py` |
| **CU05 - Registrar resultados de analítica** | `Procedimiento`, `Analitica` | Diagrama de Secuencia - CU05 | `ServicioRegistrarResultados` | `ServicioRegistrarResultados.py`, `AnaliticaDTOs.py`, `EntityProcedimiento.py`, `EntityAnalitica.py` | `test_ServicioRegistrarResultados.py` |
| **CU06 - Consultar procedimiento clínico** | `Procedimiento` | Diagrama de Secuencia - CU06 | `ServicioConsultarProcedimiento` | `ServicioConsultarProcedimiento.py`, `ProcedimientoDTOs.py`, `EntityProcedimiento.py` | `test_ServicioConsultarProcedimiento.py` |
| **CU07 - Dar de alta un paciente** | `Procedimiento` | Diagrama de Secuencia - CU07 | `ServicioDarDeAlta` | `ServicioDarDeAlta.py`, `ProcedimientoDTOs.py`, `EntityProcedimiento.py` | `test_ServicioDarDeAlta.py` |

# 9. Planificación
(Explicar cómo se ha organizado el trabajo durante las 8 semanas.)
Nos hemos organizado siguiendo la planificación orientativa para las 8 semanas y documentando todo poco a poco:
- Semanas 1-2, Inicio y dominio
En las primeras semanas nos dedicamos a la lectura del documento y análisis inicial, configuración básica del proyecto en Git y la realización del diagrama del modelo de dominio
- Semanas 3-4, BCE y Secuencia
En las semanas 3-4 nos dedicamos a reconocer las entidades del dominio que actuaban en cada caso de uso y los diagramas de secuencia de nuestros 7 casos de uso a implementar
- Semanas 5-6, diagrama de paquetes y diagrama de diseño
En las semanas 5-6 se decidieron la estructura y los patrones para la implementación de nuestro sistema y se realizaron el diagrama de paquetes y el diagrama de clases de diseño
- Semanas 7-8, implementación y tests
En las semanas 7-8 nos dedicamos a la implementación del diagrama de clases de diseño en código python y los tests de los mismos

# 10. Conclusiones
- Dificultades
- Decisiones
- Aprendizaje
- Mejoras futuras
# Anexo I
## Videodefensa
<Enlace a la videodefensa>