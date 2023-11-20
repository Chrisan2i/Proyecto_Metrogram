class Usuarios: 
    def __init__(self,id,firstname , lastname, email, username, type):
        self.id=id
        self.firstname=firstname
        self.lastname=lastname
        self.email=email
        self.username=username
        self.type=type
        
        

    def show_attr(self):
            print("="*60 + f"""
Nombre: {self.firstname}
Apellido: {self.lastname}
Email: {self.email}
Username: {self.username}
Tipo: {self.type}
""")
    
    def change_info(self,firstname,lastname,email,username):

        if self.firstname != firstname:
            self.firstname = firstname
        elif self.lastname != lastname:
            self.lastname = lastname
        elif self.email != email:
            self.email = email
        elif self.username != username:
            self.username = username


        print("""Cambio exitoso""")
           
class Student(Usuarios):
    def __init__(self, id, firstname, lastname, email, username, type, major,following,requests,strikes):
        super().__init__(id, firstname, lastname, email, username, type )
        self.major=major
        self.following = following
        
        self.requests = requests
        self.strikes = strikes 

        
    
    def show_attr(self):
            print("="*60 + f"""
Nombre: {self.firstname}
Apellido: {self.lastname}
Email: {self.email}
Username: {self.username}
Tipo: {self.type}
Carrera: {self.major}
""")
    
    def change_info(self,firstname,lastname,email,username,major):

        if self.firstname != firstname:
            self.firstname = firstname
        elif self.lastname != lastname:
            self.lastname = lastname
        elif self.email != email:
            self.email = email
        elif self.username != username:
            self.username = username
        elif self.major != major:
            self.major = major

        print("""
                                                            Cambio exitoso
              """)
    
    def follow(self,inicio_username):
        self.requests.append(inicio_username)
        print("""
                                                        == Solicitud enviada ==
              """)

    
    def follow_sameMajor(self,id,username_f):

        self.following.append(id)

        print(f"""
                                                    == Ya sigues a este {username_f} ==""")

    def Remove_person_requests(self,username):
        self.requests.remove(username)

    def vaciar_request(self):
        self.requests.clear()

    def Add_followings(self,id):
        self.following.append(id)
    
    def unfollow(self,username):
        self.following.remove(username)

class Professor(Usuarios):
    def __init__(self, id, firstname, lastname, email, username, type, department,following,requests,strikes):
        super().__init__(id, firstname, lastname, email, username, type )
        self.department = department
        self.following = following
        
        self.requests = requests
        self.strikes = strikes


    def show_attr(self):
            print("="*60 + f"""
Nombre: {self.firstname}
Apellido: {self.lastname}
Email: {self.email}
Username: {self.username}
Tipo: {self.type}
Departamento: {self.department}
""")
            
            
    def change_info(self,firstname,lastname,email,username,department):

        if self.firstname != firstname:
            self.firstname = firstname
        elif self.lastname != lastname:
            self.lastname = lastname
        elif self.email != email:
            self.email = email
        elif self.username != username:
            self.username = username
        elif self.department != department:
            self.department = department

        print("""
                                                        Cambio exitoso
              """)

    def follow(self,username_f):
        self.requests.append(username_f)


        print("""
                                                        == Solicitud enviada ==
              """)
        
    def Remove_person_requests(self,username):
        self.requests.remove(username)

    def vaciar_request(self):
        self.requests.clear()
    
    def Add_followings(self,id):
        self.following.append(id)

    def unfollow(self,username):
        self.following.remove(username)
    
class Admin(Usuarios):
    def __init__(self, id, firstname, lastname, email, username, type,key,usuriarios_eliminados):
        super().__init__(id, firstname, lastname, email, username, type )
        self.key = key
        self.usuarios_eliminados = usuriarios_eliminados

    def show_attr(self):
        print("="*60 + f"""
Nombre: {self.firstname}
Apellido: {self.lastname}
Email: {self.email}
Username: {self.username}
Tipo: {self.type}
""")
    
    

    def eliminar_user(self,user):
        self.usuriarios_eliminados.append(user)


    



    
               
        