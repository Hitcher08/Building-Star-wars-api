from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Personaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column (db.String(250), nullable=True)
    skin_color = db.Column(db.String(80), unique=False, nullable=False)
    eye_color = db.Column(db.String(80), unique=False, nullable=False)
    image = db.Column (db.String(250), nullable=False)
    favoritos = db.relationship("Favorito")
    

    @classmethod
    def create_people(cls, body):
        try:
            if body.get("name") is None:
                raise Exception({
                    "message": "No se ha encontrado el name"
                }, 400)
            if body.get("gender") is None:
                raise Exception({
                    "message": "No se ha encontrado gender"
                }, 400)
            if body.get("skin_color") is None:
                raise Exception({
                    "message": "No se ha encontrado skincolor"
                }, 400)
            if body.get("eye_color") is None:
                raise Exception({
                    "message": "No se ha encontrado eyecolor"
                }, 400)        
            if body.get("image") is None:
                raise Exception({
                    "message": "No hay image"
                },400)  
            nuevo_personaje = cls(name=body["name"], gender=body.get("gender"), image=body["image"], skin_color=body["skin_color"], eye_color=body["eye_color"])
            guardar_personaje = nuevo_personaje.save_commit()
            if guardar_personaje is False:
                raise Exception({
                    "message": "Error del servidor"
                },500)  
            return nuevo_personaje
        except Exception as error:
            print(error.args, type(error.args))
            return ({
                "message": "Algo salio mal (" + error.args[0]["message"] + ")",
                "status": error.args[1]
            })
    
    def save_commit(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            return False      
        
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            # do not serialize the password, its a security breach
        }
class Planeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column (db.String(250), nullable=False)
    image = db.Column (db.String(250), nullable=False)
    favoritos = db.relationship("Favorito")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            # do not serialize the password, its a security breach
        }

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column (db.String(250), unique=True, nullable=False)
    password = db.Column (db.String(250), nullable=False)
    favoritos = db.relationship("Favorito", back_populates="users")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favoritos": [favorito.serialize() for favorito in self.favoritos]
            # do not serialize the password, its a security breach
        }

    def serialize_two(self):
        return {
            "id": self.id,
            "email": self.email
            #"favoritos": [favorito.serialize() for favorito in self.favoritos]
            # do not serialize the password, its a security breach
        }

class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_personaje = db.Column(db.Integer, db.ForeignKey('personaje.id'))
    id_planeta = db.Column(db.Integer, db.ForeignKey('planeta.id'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    users = db.relationship("Usuario", back_populates="favoritos")

    def serialize(self):
        return {
            "id": self.id,
            "id_personaje": self.id_personaje,
            "id_planeta": self.id_planeta,
            "id_usuario": self.id_usuario,
            # do not serialize the password, its a security breach
        }        