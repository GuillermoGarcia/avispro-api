# Avispro Api

  Api el proyecto [Avispro](hhtps://)

## Caracteristicas
  **Lenguaje:** Python<br />
  **Microframework:** Flask<br />
  **Plugins:** SQLAlchemy y Alembic<br />
  **Base de Datos:** Postgres (Amazon RDS)<br />
  **Localización:** Heroku (https://avispro-api.herokuapp.com/api/v1)<br />
  **Extra:** Conexión con Firebase<br />

  Envío de Datos a través del Body en formato JSON<br />
  Respuesta de la API en formato JSON<br />

## Métodos de la Api

###Usuarios

  **Registrar Usuario:** POST /usuarios<br />
  **Obtener Token Login:** POST /tokens<br />
  **Obtener Usuarios:** GET /usuarios<br />
  **Obtener un Usuario:** GET /usuarios/idUsuario<br />
  **Obtener un Usuario:** PUT /usuarios/idUsuario<br />

### Habilidades Base

  **Crear Habilidades Base:** POST /habilidades<br />
  **Obtener Todas las Habilidades Base:** GET /habilidades<br />
  **Obtener una Habilidad Base:** GET /habilidades/idHabilidad<br />
  **Actualizar Habilidad Base:** PUT /habilidades/idHabilidad 
 

### Personajes

  **Crear Personaje:** POST /personajes 
  **Obtener Personaje:** GET /personajes<br />
  **Obtener Personaje:** GET /personajes/idPersonaje<br />
  **Actualizar Personaje:** PUT /personajes/idPersonaje 


### Habilidades de Personajes

  **Aprender Habilidad:** POST /personajes/idPersonaje/habilidades/idHabilidad<br />
  **Obtener Habilidades del Personaje:** GET /personajes/idPersonaje/habilidades<br />
  **Obtener Habilidad:** GET /personajes/idPersonaje/habilidades/idHabPj<br />
  **Actualizar Habilidad:** PUT /personajes/idPersonaje/habilidades/idHabPj 


### Combate

  **Crear Combate:** POST /combates 
  **Unirse Pj al Combate:** POST /combates/idCombate/pj/idCombatiente 
  **Unirse Pnj al Combate:** POST /combates/idCombate/pnj/idCombatiente 
  **Obtener Todos los Combates:** GET /combates 
  **Obtener un Combate:** GET /combates/idCombate 


###Combatiente

  **Crear Combatiente:** POST /combatientes 


