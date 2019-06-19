import base64, random, string, os
from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model):
    idUsuario = db.Column(db.String(28), primary_key=True)
    alias = db.Column(db.String(64), index=True, unique=True)
    correo = db.Column(db.String(120), index=True, unique=True, nullable=False)
    avatar = db.Column(db.String(128))
    personajes = db.relationship('Personaje', backref='jugador', lazy='dynamic')
    combates = db.relationship('Combate', backref='master', lazy='dynamic')
    contrasena = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiracion = db.Column(db.DateTime)

    def __repr__(self):
        return '<Usuario {}, correo {}>'.format(self.alias, self.correo)

    def asignar_contrasena(self, contrasena):
        self.contrasena = generate_password_hash(contrasena)

    def verificar_contrasena(self, contrasena):
        return check_password_hash(self.contrasena, contrasena)

    def to_dict(self):
        personajes = []
        for personaje in self.personajes:
            personajes.append(personaje.idPersonaje)

        datos = {
            'idUsuario': self.idUsuario,
            'alias': self.alias,
            'avatar': self.avatar,
            'correo': self.correo,
            'personajes': personajes
        }
        return datos

    def from_dict(self, datos, nuevo_usuario=False):
        for campo in ['idUsuario', 'correo', 'alias', 'avatar']:
            if campo in datos:
                setattr(self, campo, datos[campo])
        if nuevo_usuario and 'contrasena' in datos:
            self.asignar_contrasena(datos['contrasena'])

    def obtener_token(self, expira_en=3600):
        ahora = datetime.utcnow()
        if self.token and self.token_expiracion > ahora + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiracion = ahora + timedelta(seconds=expira_en)
        db.session.add(self)
        return self.token

    def revocar_token(self):
        self.token_expiracion = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def verificar_token(token):
        usuario = Usuario.query.filter_by(token=token).first()
        if usuario is None or usuario.token_expiracion < datetime.utcnow():
            return None
        return usuario


class Personaje(db.Model):
    idPersonaje = db.Column(db.String(28), primary_key=True)
    avatar = db.Column(db.String(128))
    nombre = db.Column(db.String(64), index=True, nullable=False)
    cultura = db.Column(db.String(64), index=True)
    raza = db.Column(db.String(64), index=True)
    edad = db.Column(db.Integer)
    procedencia = db.Column(db.String(64), index=True)
    nivel = db.Column(db.Integer)
    caracteristicas = db.Column(db.JSON)
    habilidades = db.relationship('HabilidadPersonaje', backref="habilidadPersonaje", lazy='dynamic')
    usuario_id = db.Column(db.String(28), db.ForeignKey('usuario.idUsuario'))

    def __repr__(self):
        return '<Personaje {}>'.format(self.nombre)

    def to_dict(self):
        habilidades = []
        for habilidad in self.habilidades:
            habilidades.append(habilidad.idHabilidadPersonaje)

        datos = {
            'idPersonaje': self.idPersonaje,
            'nombre': self.nombre,
            'avatar': self.avatar,
            'cultura': self.cultura,
            'raza': self.raza,
            'edad': self.edad,
            'procedencia': self.procedencia,
            'nivel': self.nivel,
            'caracteristicas': self.caracteristicas,
            'habilidades': habilidades
        }
        return datos

    def from_dict(self, datos, idUsuario):
        setattr(self, 'usuario_id', idUsuario)
        for campo in ['idPersonaje', 'avatar', 'nombre', 'cultura', 'raza', 'edad', 'procedencia', 'nivel', 'caracteristicas']:
            if campo in datos:
                setattr(self, campo, datos[campo])


class HabilidadBase(db.Model):
    idHabilidad = db.Column(db.String(64), primary_key=True)
    nombre = db.Column(db.String(140), nullable=False)
    descripcion = db.Column(db.String(420))
    bonusPrincipal = db.Column(db.String, nullable=False)
    bonusSecundario = db.Column(db.String, nullable=False)
    combate = db.Column(db.Boolean, nullable=False)
    tipo = db.Column(db.Integer, nullable=False)
    habilidades = db.relationship('HabilidadPersonaje', backref="habilidadBase", lazy='dynamic')

    def __repr__(self):
        return '<Habilidad Base {}>'.format(self.nombre)

    def to_dict(self):
        datos = {
            'idHabilidad': self.idHabilidad,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'bonusPrincipal': self.bonusPrincipal,
            'bonusSecundario': self.bonusSecundario,
            'combate': self.combate,
            'tipo': self.tipo
        }
        return datos

    def from_dict(self, datos):
        for campo in ['idHabilidad', 'nombre', 'descripcion', 'bonusPrincipal', 'bonusSecundario', 'combate', 'tipo']:
            if campo in datos:
                setattr(self, campo, datos[campo])

    def check_boolean(self):
        for campo in ['idHabilidad', 'nombre', 'descripcion', 'bonusPrincipal', 'bonusSecundario', 'combate', 'tipo']:
            getattr(self, campo)
            if (getattr(self, campo) == 'true'):
                setattr(self, campo, True)
            if (getattr(self, campo) == 'false'):
                setattr(self, campo, False)


class HabilidadPersonaje(db.Model):
    __table_args__ = (
        db.UniqueConstraint('habilidad_id', 'personaje_id', name='unique_personaje_habilidad'),
    )
    idHabilidadPersonaje = db.Column(db.String(64), primary_key=True)
    habilidad_id = db.Column(db.String(64), db.ForeignKey('habilidad_base.idHabilidad'), nullable=False)
    personaje_id = db.Column(db.String(28), db.ForeignKey('personaje.idPersonaje'), nullable=False)
    valorBase = db.Column(db.Integer, nullable=False)
    extra = db.Column(db.Integer)
    pap = db.Column(db.Integer)
    habilidadUsada = db.Column(db.Boolean)

    def __repr__(self):
        return '<{}: {}>'.format(self.habilidad_id, self.valorBase)

    def to_dict(self):
        hb = HabilidadBase.query.filter_by(idHabilidad=self.habilidad_id).first()
        resultado = {
            'idHabilidadPersonaje': self.idHabilidadPersonaje,
            'idPersonaje': self.personaje_id,
            'idHabilidad': self.habilidad_id,
            'nombre': hb.nombre,
            'bonusPrincipal': hb.bonusPrincipal,
            'bonusSecundario': hb.bonusSecundario,
            'combate': hb.combate,
            'tipo': hb.tipo,
            'valorBase': self.valorBase,
            'pap': self.pap,
            'extra': self.extra,
            'habilidadUsada': self.habilidadUsada
        }
        return resultado

    def from_dict(self, datos):
        for campo in ['idHabilidadPersonaje', 'habilidad_id', 'personaje_id', 'valorBase', 'extra', 'pap', 'habilidadUsada']:
            if campo in datos:
                setattr(self, campo, datos[campo])

    def conocer_habilidad(self, datos):
        return HabilidadPersonaje.query.filter(
                HabilidadPersonaje.habilidad_id == datos['habilidad_id'] and
                HabilidadPersonaje.personaje_id == datos['personaje_id']
            ).count() > 0

    def generar_id_habilidad_personaje(self):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(64))


pjs = db.Table('PJS',
    db.Column('pj_id', db.String(28), db.ForeignKey('combatiente.idCombatiente'), primary_key=True),
    db.Column('combate_id', db.String(28), db.ForeignKey('combate.idCombate'), primary_key=True)
)

pnjs = db.Table('PNJS',
    db.Column('pnj_id', db.String(28), db.ForeignKey('combatiente.idCombatiente'), primary_key=True),
    db.Column('combate_id', db.String(28), db.ForeignKey('combate.idCombate'), primary_key=True)
)


class Combatiente(db.Model):
    idCombatiente = db.Column(db.String(28), primary_key=True)
    avatar = db.Column(db.String(128))
    iniciativa = db.Column(db.Integer, index=True, nullable=False)
    nombre = db.Column(db.String(64), nullable=False)
    reflejos = db.Column(db.Integer, nullable=False)
    velocidadArma = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Combatiente {}>'.format(self.nombre)

    def to_dict(self):
        resultado = {
            'idCombatiente': self.idCombatiente,
            'avatar': self.avatar,
            'iniciativa': self.iniciativa,
            'nombre': self.nombre,
            'reflejos': self.reflejos,
            'velocidadArma': self.velocidadArma
        }
        return resultado

    def from_dict(self, datos):
        for campo in ['idCombatiente', 'avatar', 'iniciativa', 'nombre', 'reflejos', 'velocidadArma']:
            if campo in datos:
                setattr(self, campo, datos[campo])

    def generar_id_combatiente(self):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(28))


class Combate(db.Model):
    idCombate = db.Column(db.String(28), primary_key=True)
    descripcion = db.Column(db.String(140))
    iniciativa = db.Column(db.Integer, nullable=False, default=0)
    master_id = db.Column(db.String(28), db.ForeignKey('usuario.idUsuario'), nullable=False)
    nombre = db.Column(db.String(64), nullable=False)
    orden = db.Column(db.ARRAY(db.String(64)))
    pjs = db.relationship('Combatiente', secondary=pjs, backref=db.backref("PJS", lazy='dynamic'), lazy='dynamic')
    pnjs = db.relationship('Combatiente', secondary=pnjs, backref=db.backref("PNJS", lazy='dynamic'), lazy='dynamic')
    turno = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Combate {}>'.format(self.nombre)

    def to_dict(self):
        pjs = []
        for pj in self.pjs:
            pjs.append(pj.idCombatiente)
        pnjs = []
        for pnj in self.pnjs:
            pnjs.append(pnj.idCombatiente)
        resultado = {
            'idCombate': self.idCombate,
            'nombre': self.nombre,
            'master_id': self.master_id,
            'descripcion': self.descripcion,
            'iniciativa': self.iniciativa,
            'turno': self.turno,
            'orden': self.orden,
            'pjs': pjs,
            'pnjs': pnjs
        }
        return resultado

    def from_dict(self, datos):
        for campo in ['idCombate', 'descripcion', 'iniciativa', 'master_id', 'nombre', 'pjs_id', 'pnjs_id', 'turno', 'orden']:
            if campo in datos:
                setattr(self, campo, datos[campo])

    def generar_id_combate(self):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(28))
