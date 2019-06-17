from flask import g
from app import firestore
from firebase_admin import auth

class Firebase():

    '''
        Verificar token de usuario contra Firebase Authentication
        @param: token, token de usuario
        @return: String, el uid del usuario o None
    '''
    def firebase_verificar_token(self, token):
        firebase_token = auth().verify_id_token(token)
        return firebase_token['uid']

    '''
        Crear usuario en Cloud Firestore
        @param: usuario, los datos de usuario
        @return: String, el id del usuario creado
    '''
    def firebase_crear_usuario(self, usuario):
        datos = {
            u'idUsuario': u'',
            u'alias': u'{}'.format(usuario['alias']),
            u'correo': u'{}'.format(usuario['correo']),
            u'avatar': u'{}'.format(usuario['avatar']),
            u'personajes': []
        }
        usuarios = firestore.collection(u'usuarios')
        idUsuario = usuarios.add(datos)
        usuarios.document(idUsuario).update({u'idUsuario': idUsuario})
        return idUsuario

    '''
        Actualizar usuario en Cloud Firestore
        @param: usuario, los datos de usuario a actualizar
        @return:
    '''
    def firebase_actualizar_usuario(self, usuario):
        datos = {
            u'idUsuario': usuario.idUsuario,
            u'correo': usuario.correo,
            u'avatar': usuario.avatar,
            u'alias': usuario.alias,
            u'personajes': usuario.personajes
        }
        firestore.collection(u'usuarios').document(usuario.idUsuario).update(datos)

    '''
        Actualizar ids de los personajes de un usuario en Cloud Firestore
        @param: personajes, array con los ids de los personajes
        @return:
    '''
    def firebase_actualizar_usuario_personajes(self, personajes):
        firestore.collection(u'usuarios').document(g.usuario_actual.idUsuario).update({u'personajes': personajes})

    '''
        Crear personaje en Cloud Firestore
        @param: personaje, los datos de personaje
        @return: String, el id del personaje creado
    '''
    def firebase_crear_personaje(self, personaje):
        datos = {
            u'idPersonaje': u'',
            u'nombre': u'{}'.format(personaje['nombre']),
            u'avatar': u'{}'.format(personaje['avatar']),
            u'cultura': u'{}'.format(personaje['cultura']),
            u'raza': u'{}'.format(personaje['raza']),
            u'edad': u'{}'.format(personaje['edad']),
            u'procendecia': u'{}'.format(personaje['procedencia']),
            u'nivel': u'{}'.format(personaje['nivel']),
            u'caracteristicas': personaje['caracteristicas']
        }
        personajes = firestore.collection(u'personajes')
        idPersonaje = personajes.add(datos)
        personajes.document(idPersonaje).update({u'idPersonaje': idPersonaje})
        return idPersonaje

    '''
        Actualizar personaje en Cloud Firestore
        @param: personaje, los datos de personaje a actualizar
        @return:
    '''
    def firebase_actualizar_personaje(self, personaje):
        datos = {
            u'idPersonaje': personaje.idPersonaje,
            u'nombre': personaje.nombre,
            u'cultura': personaje.cultura,
            u'raza': personaje.raza,
            u'edad': personaje.edad,
            u'procendecia': personaje.procendecia,
            u'nivel': personaje.nivel,
            u'avatar': personaje.avatar,
            u'caracteristicas': personaje.caracteristicas
        }
        firestore.collection(u'personajes').document(personaje.idPersonaje).update(datos)

    '''
        Crear habilidad nueva del personaje en Cloud Firestore
        @param: idPersonaje, id del personaje que aprede la habilidad
        @param: idHabilidadBase, id de la habilidad base que aprende el personaje
        @param: habilidad, los datos de la nueva habilidad del personaje
        @return: String, el id de la nueva habilidad creada
    '''
    def firebase_crear_habilidad(self, habilidad):
        datos = {
            u'idHabilidadPersonaje': u'',
            u'idPersonaje': u'{}'.format(habilidad['personaje_id']),
            u'idHabilidad': u'{}'.format(habilidad['habilidad_id']),
            u'valorBase': u'{}'.format(habilidad['valorBase']),
            u'pap': u'{}'.format(habilidad['pap']),
            u'extra': u'{}'.format(habilidad['extra']),
            u'habilidadUsada': u'{}'.format(habilidad['habilidadUsada'])
        }
        habilidad = firestore.collection(u'habilidadPersonaje')
        idHabilidadPersonaje = habilidad.add(datos)
        habilidad.document(idHabilidadPersonaje).update({u'idHabilidadPersonaje': idHabilidadPersonaje})
        return idHabilidadPersonaje

    '''
        Actualizar habilidad en Cloud Firestore
        @param: habilidad, los datos de habilidad a actualizar
        @return:
    '''
    def firebase_actualizar_habilidad(self, habilidad):
        datos = {
            u'idHabilidadPersonaje': u'{}'.format(habilidad.idPersonaje),
            u'idPersonaje': u'{}'.format(habilidad.personaje_id),
            u'idHabilidad': u'{}'.format(habilidad.habilidad_id),
            u'valorBase': u'{}'.format(habilidad.valorBase),
            u'pap': u'{}'.format(habilidad.pap),
            u'extra': u'{}'.format(habilidad.extra),
            u'habilidadUsada': u'{}'.format(habilidad.habilidadUsada)
        }
        firestore.collection(u'habilidadPersonaje').document(habilidad.idHabilidadPersonaje).update(datos)

    '''
        Crear un combate nuevo en Cloud Firestore
        @param: combate, los datos del nuevo combate
        @param: nombreMaster, nombre del usuario master del nuevo combate
        @return: String, el id del nuevo combate creado
    '''
    def firebase_crear_combate(self, combate, nombreMaster):
        datos = {
            u'idCombate': u'',
            u'nombre': u'{}'.format(combate['nombre']),
            u'descripcion': u'{}'.format(combate['descripcion']),
            u'idMaster': u'{}'.format(combate['master_id']),
            u'master': u'{}'.format(nombreMaster),
            u'iniciativa': 0,
            u'turnos': 0,
            u'orden': [],
            u'idPjs': [],
            u'idPnjs': [],
            u'idAcciones': None
        }
        combate = firestore.collection(u'combate')
        idCombate = combate.add(datos)
        combate.document(idCombate).update({u'idCombate': idCombate})
        return idCombate

    '''
        Actualizar combate en Cloud Firestore
        @param: combate, los datos de combate a actualizar
        @param: nombreMaster, nombre del usuario master del combate
        @return: None
    '''
    def firebase_actualizar_combate(self, combate, nombreMaster):
        datos = {
            u'idCombate': u'{}'.format(combate.idCombate),
            u'nombre': u'{}'.format(combate.nombre),
            u'descripcion': u'{}'.format(combate.descripcion),
            u'idMaster': u'{}'.format(combate.master_id),
            u'master': u'{}'.format(nombreMaster),
            u'iniciativa': combate.iniciativa,
            u'turnos': combate.turnos,
            u'orden': combate.orden,
            u'idPjs': combate.idPjs,
            u'idPnjs': combate.idPnjs,
            u'idAcciones': combate.idAcciones
        }
        firestore.collection(u'combate').document(combate.idCombate).update(datos)

    '''
        Actualizar pjs del combate en Cloud Firestore
        @param: idCombate, id del combate a actualizar
        @param: pjs, array con los ids de los combatientes
        @return: None
    '''
    def firebase_actualizar_combate_pjs(self, idCombate, pjs):
        firestore.collection(u'combate').document(idCombate).update({u'idPjs': pjs})

    '''
        Actualizar pnjs del combate en Cloud Firestore
        @param: idCombate, id del combate a actualizar
        @param: pnjs, array con los ids de los combatientes
        @return: None
    '''
    def firebase_actualizar_combate_pnjs(self, idCombate, pnjs):
        firestore.collection(u'combate').document(idCombate).update({u'idPnjs': pnjs})

    '''
        Crear combatiente nuevo en Cloud Firestore
        @param: combatiente, los datos del nuevo combatiente
        @return: String, el id del nuevo combatiente creado
    '''
    def firebase_crear_combatiente(self, combatiente):
        datos = {
            u'idCombatiente': u'',
            u'nombre': u'{}'.format(combatiente['nombre']),
            u'avatar': u'{}'.format(combatiente['avatar']),
            u'iniciativa': u'{}'.format(combatiente['iniciativa']),
            u'reflejos': u'{}'.format(combatiente['reflejos']),
            u'velocidadArma': u'{}'.format(combatiente['velocidadArma'])
        }
        combatiente = firestore.collection(u'combatiente')
        idCombatiente = combatiente.add(datos)
        combatiente.document(idCombatiente).update({u'idCombatiente': idCombatiente})
        return idCombatiente

    '''
        Actualizar combatiente en Cloud Firestore
        @param: combatiente, los datos de combatiente a actualizar
        @return:
    '''
    def firebase_actualizar_combatiente(self, combatiente):
        datos = {
            u'idCombatiente': u'{}'.format(combatiente.idCombatiente),
            u'nombre': u'{}'.format(combatiente.nombre),
            u'avatar': u'{}'.format(combatiente.avatar),
            u'iniciativa': u'{}'.format(combatiente.iniciativa),
            u'reflejos': u'{}'.format(combatiente.reflejos),
            u'velocidadArma': u'{}'.format(combatiente.velocidadArma)
        }
        firestore.collection(u'combatiente').document(combatiente.idCombatiente).update(datos)
