# Avispro Api

  Api el proyecto [Avispro](hhtps://)

## Caracteristicas
**Lenguaje:** Python
**Microframework:** Flask
**Plugins:** SQLAlchemy y Alembic
**Base de Datos:** Postgres (Amazon RDS)
**Localización:** Heroku (https://avispro-api.herokuapp.com/api/v1)
**Extra:** Conexión con Firebase

  Envío de Datos a través del Body en formato JSON
  Respuesta de la API en formato JSON

## Métodos de la Api

###Usuarios

  **Registrar Usuario:** POST /usuarios
  **Obtener Token Login:** POST /tokens
  **Obtener Usuarios:** GET /usuarios
  **Obtener un Usuario:** GET /usuarios/idUsuario
  **Obtener un Usuario:** PUT /usuarios/idUsuario

### Habilidades Base

  **Crear Habilidades Base:** POST /habilidades
  **Obtener Todas las Habilidades Base:** GET /habilidades
  **Obtener una Habilidad Base:** GET /habilidades/idHabilidad
  **Actualizar Habilidad Base:** PUT /habilidades/idHabilidad
 

### Personajes

  **Crear Personaje:** POST /personajes
  **Obtener Personaje:** GET /personajes
  **Obtener Personaje:** GET /personajes/idPersonaje
  **Actualizar Personaje:** PUT /personajes/idPersonaje


### Habilidades de Personajes

  **Aprender Habilidad:** POST /personajes/idPersonaje/habilidades/idHabilidad
  **Obtener Habilidades del Personaje:** GET /personajes/idPersonaje/habilidades
  **Obtener Habilidad:** GET /personajes/idPersonaje/habilidades/idHabPj
  **Actualizar Habilidad:** PUT /personajes/idPersonaje/habilidades/idHabPj


### Combate

  **Crear Combate:** POST /combates
  **Unirse Pj al Combate:** POST /combates/idCombate/pj/idCombatiente
  **Unirse Pnj al Combate:** POST /combates/idCombate/pnj/idCombatiente
  **Obtener Todos los Combates:** GET /combates
  **Obtener un Combate:** GET /combates/idCombate


###Combatiente

  **Crear Combatiente:** POST /combatientes


