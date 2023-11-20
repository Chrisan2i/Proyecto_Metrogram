
import json
import datetime 
import operator
import uuid

from usuario import Student, Professor,Admin
from post import Post




#Retorna un diccionario para crear el objeto
def data_base():
    db={"users":[],
        "post":[],
        "admin":[]
        }
    return db

def cargar(db):
    tem_u = []
    tem_p = []
    for u in db["users"]:
        if isinstance(u,Student):
            tem_u.append(
  {
    "id": u.id,
    "firstName": u.firstname,
    "lastName": u.lastname,
    "email": u.email,
    "username": u.username,
    "type": u.type,
    "major": u.major,
    "following": u.following,
    "request": u.requests,
    "strikes":u.strikes  }
)
        elif isinstance(u,Professor):
            tem_u.append(
  {
    "id": u.id,
    "firstName": u.firstname,
    "lastName": u.lastname,
    "email": u.email,
    "username": u.username,
    "type": u.type,
    "department": u.department,
    "following": u.following,
    "request": u.requests,
    "strikes":u.strikes  }
)
            
    for a in db["admin"]:
        tem_u.append(
  {
    "id": a.id,
    "firstName": a.firstname,
    "lastName": a.lastname,
    "email": a.email,
    "username": a.username,
    "type": a.type,
    "key" : a.key,
    "usuarios_eliminados":a.usuarios_eliminados }
)

    with open("Metrogram_users.json","w") as file:
        json.dump(tem_u,file, indent=4)
        file.close()

    for p in db["post"]:
        tem_p.append(
{
    "publisher": p.id_publisher,
    "type": p.type,
    "caption": p.caption,
    "date": p.date_p,
    "tags": p.tags,
    "multimedia": p.multimedia,
    "likes": p.likes,
    "comentarios":p.comentarios
})
    with open("Metrogram_post.json","w") as file:
        json.dump(tem_p,file, indent=4)
        file.close()

#=================================================== FUNCIONES IMPORTANTES ==============================================  
# Ver mi Perfil
def view_MIPefil(db,username):

    for u in db["users"]:
        if isinstance(u,Student):
            if u.username.lower() == username.lower():
                u.show_attr()
        elif isinstance(u,Professor):
            if u.username.lower() == username.lower():
                u.show_attr()
        
    print("SEGUIDOS:")
    for u in db["users"]:
        if isinstance(u,Professor):
            if u.username.lower() == username.lower():
                for y in (u.following):
                    for ub in db["users"]:
                        if ub.id == y:
                            print(f"-{ub.username}")
        elif isinstance(u,Student):
            if u.username.lower() == username.lower():
                for y in (u.following):
                    for ub in db["users"]:
                        if ub.id == y:
                            print(f"-{ub.username}")

def dejar_de_seguir(db,username):

    lista_username = []
    lista_seguidos=[]
    cont=0
    contw = 0
    contb=0
    print("""
                                                    SEGUIDOS:""")
    while contw == 0:
 
        for u in db["users"]:           
            if u.username.lower() == username.lower():
                for y in (u.following):
                    for ub in db["users"]:
                        if ub.id == y:
                            cont+=1
                            print(f"""{cont}. {ub.username}""")
                            lista_seguidos.append(y)
                            lista_username.append(ub.username.lower())
                            contw+=1
                            contb +=1
        if contw != 0: 
            unfollow2(db,username,lista_seguidos,lista_username)
            cargar(db) 
            
        if contb == 0:
            print("""
                                                    No tienes seguidos """)
            contw+=1
            break

                        
def unfollow2(db,username,lista_seguidos,lista_username):
    cont=0
    while cont==0:
        option= input("""
                                                Quiere dejar de seguir a alguien:
                                                1. Si
                                                2. No
➥ """)
        if option == "1":                

            option_no_seguir=int(input("""
                                                A que numero desea dejar de seguir
                                                0. Ninguno
➥ """))
            if option_no_seguir == 0:
                cont+=1
            elif option_no_seguir != 0:
                for u in db["users"]:
                    if username.lower() == u.username.lower():
                        u.unfollow(lista_seguidos[option_no_seguir-1])
                        print(f"""
                                                Dejo de seguir a {lista_username[option_no_seguir-1]}            
""")    
                        cont+=1
                        break
        elif option == "2":
            cont+=1
            break
    cargar(db)

# Ver mis post                            
#PROBARLO
def view_MIPost(db,username):
    
    contp = 0
    lista_posts_date = []
    
    for u in db["users"]:
        if isinstance(u,Student):
            for posts in db["post"]:
                if u.username.lower() == username.lower():
                    if u.id == posts.id_publisher:
                        print(f"""
{contp+1}.""")
                        posts.view_post()
                        mostrar_iteracciones(db,posts.date_p)
                        contp+=1
                        date=posts.date_p
                        lista_posts_date.append(date)

        elif isinstance(u,Professor):
            for posts in db["post"]:
                if u.username.lower() == username.lower():
                    if u.id == posts.id_publisher:
                        print(f"""
{contp+1}.""")
                        
                        posts.view_post()
                        mostrar_iteracciones(db,posts.date_p)
                        contp+=1
                        date=posts.date_p
                        lista_posts_date.append(date)
        
    if contp == 0:
        print("""
                                    No tienes publicaciones 
              """)
    if contp!=0:
        ver_mas_opciones(db,lista_posts_date)

def ver_mas_opciones(db,lista_posts_date):
    cont=0
    cont_del=0

    while cont == 0:
        option_posts = int(input("""
                                                A que posts desea ver opciones
                                                0. Ninguno 
➥ """))

        if option_posts == 0:
            cont+=1
            break

        elif option_posts != 0:
            options = input("""
                                                Elija una opcion valida:

                                                0. Atras 

                                                1. Likes
                                                2. Comentarios
                                                3. Eliminar post 
➥ """)
                    
            if options == "0":
                cont +=1
                break

            elif options == "1":
                for posts in db["post"]:
                    if lista_posts_date[option_posts-1] == posts.date_p:
                        for y,l in enumerate(posts.likes):
                            print(f"""
                                        Personas que le han dado like
                                        {y+1}. {l}""")
            elif options == "2":
                contcomen=0
                for posts in db["post"]:
                    if lista_posts_date[option_posts-1] == posts.date_p:
                        for comentario in posts.comentarios:
                            for k,v in comentario.items():
                                print(f"""
Comentarios:""")
                                contcomen+=1
                                print(f"""
                                        ->{contcomen}. {k}:{v[0]}  Date:{v[1]}""")

                user = int(input("""
                                            Cual comentarios deseas borrar:
                                            0. Ninguno
➥ """))
                if user == 0:
                    pass
                elif user != 0:
                    for posts in db["post"]:
                        if lista_posts_date[option_posts-1] == posts.date_p:
                            del posts.comentarios[user-1]

                            print("""
                                            Cometario borrado""")

            elif options == "3":
                delete = input("""
                                            Seguro quieres eliminar el post:
                                   
                                            1. SI
                                            2. No
➥""")
                if delete == "1":
                    for posts in db["post"]:
                        cont_del +=1
                        if lista_posts_date[option_posts-1] == posts.date_p:
                            
                            del db["post"][cont_del-1]
                    print("""               
                                            Posts eliminado
                            """)
                    break
                
                elif delete == "2":
                    cont+=1
                    break
    cargar(db)            
#=================================================== MODULO GESTION DE PERFIL ============================================== 
 

#INICIO DE SESION
def login(db,username):
    cont=0

    for u in db["users"]:
        if isinstance(u,Student):
            if u.username.lower() == username:
                print("-"*200 +f"""
========================================== [Sesion Iniciada del Estudiante - {u.username.lower()}] ==========================================""")
                cont+=1
                return True
            
        
        elif isinstance(u,Professor):
            if u.username.lower() == username:
                print("-"*200 +f"""
========================================== [Sesion Iniciada del Profesor - {u.username.lower()}] ==========================================""")
                cont+=1
                return True
             
                
    for a in db["admin"]:
        if username.lower() == a.username:
            key = input("""Introduzca la clave: """)
            if key == a.key:
                print("-"*200 +f"""
========================================== [Sesion Iniciada del Admin - {a.username}] ==========================================""")
                cont+=1
                return True
            else:
                print("""
                                                La clave no es correcta 💀
                      """)
                cont+=1
                return False

    if cont == 0:
        print("""
                                                No tiene una cuenta registrada ☹ """)
        return False 
             

# Validacion de inicio de sesion                            
def valid_login(db,username):

    for u in db["users"]:
        if isinstance(u,Student):
            if u.username.lower() == username:
                type = u.type.lower()
                return type
            
        elif isinstance(u,Professor):
            if u.username.lower() == username:
                type = u.type.lower()
                return type
                    
    for a in db["admin"]:
        if username.lower() == a.username:
            type = a.type
            return type

    
# Registra a las personas nuevas
def registrarse(db):
    cont=0

    
    
    indentificador = uuid.uuid4()

    for user in db["users"]:
        while user.id == id:
            indentificador = uuid.uuid4()


    

    firstName=input("Cual es su Nombre: ")
    lastName=input("Cual es su apellido: ")

    while cont == 0:
        username=input("Cual es su username: ")

        
        for u in db["users"]:
            for a in db["admin"]:
                if u.username.lower() == username.lower() or a.username.lower() == username.lower():
                    print("""
                                            Este username ya esta en uso intete de nuevo
    """)
                
                    username=input("Ingrese otro username: ")
                    cont+=1
                    break
                cont+=1



    while True:
        email=input("""Correo de la Unimet:  
➥ """)
        if "@correo.unimet.edu.ve" in email:
            break
            
        else:
            print("""
Obligatorio -> @correo.unimet.edu.ve""")
            
    while True:
        type=input("""
1. Profesor
2. Estudiante
➥ """)
        if type == "1":
            department=input("Cual departamento: ")
            following=[]
    
            db["users"].append(Professor(str(indentificador),firstName,lastName,email,username,"professor",department,following,[],[]))
            cargar(db)
            break

        elif type == "2":
            major=input("Que carre estudias: ")
            following=[]
            db["users"].append(Student(str(indentificador),firstName,lastName,email,username,"student",major,following,[],[]))
            cargar(db)
            break
            
        else:
            print("Elija una opcion valida")  
           
# Buscar perfiles
def buscar_usuario(db,inicio_username):
    
    while True:
        print(""" =========================================    [Buscador de perfiles]    ============================================ """)
        option=input("""
                     
                                                    0. Atras

                                                    1. Username
                                                    2. Departamento 
                                                    3. Carrera
➥ """)
        
        if option == "1":
            cont=0
            while cont == 0:
                username_buscar=input(""" 
                                                    Que username desea buscar: 
➥ """)



                for u in db["users"]:
                    if isinstance(u,Student):
                        if u.username.lower() == username_buscar.lower():
                            cont+=1
                            id_userbuscado = u.id
                            print(f"""
                                                    @{u.username}""")
                            option_ver=input("""                
                                                    Desea ver el perfil

                                                    1. Si
                                                    2. No
➥ """)
                            if option_ver == "1":
                                u.show_attr()
                                seguidos_mostrar_posts(db,inicio_username,username_buscar,id_userbuscado)
                                break
                            
                            
                            elif option_ver == "2":
                                break

                
                    elif isinstance(u,Professor):
                        if username_buscar.lower() == u.username.lower():
                            cont+=1
                            id_userbuscado = u.id
                            print(f"""
                                                    @{u.username}""")
                            option_ver=input("""                
                                                    Desea ver el perfil

                                                    1. Si
                                                    2. No
➥ """)
                            if option_ver == "1":
                                u.show_attr()
                                seguidos_mostrar_posts(db,inicio_username,username_buscar,id_userbuscado)
                                break
                            
                            
                            
                            elif option_ver == "2":
                                break

                if cont == 0:
                    print("""
                                                    Este Usuario No existe""")
                    break   
                                 
        
        elif option == "2":
                contd=0
                cont=0
                while contd == 0:
                    type=input("""
                                                    Que departamento desea buscar: 
➥ """)
                    lista_ids = []

                    lista_username=[]
                    cont=0
                    for u in db["users"]:
                        if isinstance(u,Professor):
                            if type == u.department:
                                cont+=1
                                print(f"""
                                                    {cont}. @{u.username}""")
                                lista_username.append(u.username)
                                lista_ids.append(u.id)
                                contd+=1
                    if contd == 0:
                        print("""
                                                    Esta Departamento No existe""")
                        contd+=1
                        break

                    if contd != 0:
                        buscar_perfiles2(db,inicio_username,lista_username)
                                                       

        elif option == "3":
            contm=0
            cont=0
            while contm == 0:
                type=input("""
                                                    Que carrera desea buscar: 
➥ """)
                lista_ids = []

                lista_username=[]
                for u in db["users"]:
                    if isinstance(u,Student):
                        if type.lower() == u.major.lower():
                            cont+=1
                            print(f"""
                                                    {cont}. @{u.username}""")
                            lista_username.append(u.username)
                            lista_ids.append(u.id)
                            contm+=1
            
         
                               
                if contm == 0:
                    print("""
                                                    Esta Carrera No existe""")
                    contm+=1
                    break

                if contm != 0:
                    buscar_perfiles2(db,inicio_username,lista_username)

        elif option == "0":
            break
# funcion buscar por departamento o Carrera
def buscar_perfiles2(db,inicio_username,lista_username):
    cont=0


    while cont == 0:
        option_ver=int(input("""
                                                    0.Ninguno
                                                    Que numero desea ver
➥ """))        
        if option_ver == 0:
            cont+=1
            break
        elif option_ver <= len(lista_username):
            for u in db["users"]:
                if lista_username[option_ver-1].lower() == u.username.lower():
                    usernamea_seguir = u.username.lower()
                    u.show_attr()
                    for i in db["users"]:
                        if i.username.lower() == inicio_username:
                            if lista_username[option_ver-1].lower() in i.following:
                                for h in db["users"]:
                                    if isinstance(h,Professor):
                                        for posts in db["post"]:
                                            if h.id == posts.id_publisher:
                                                posts.view_post()
                                                print("""
                                                    Sigues a este usuario""")
                                                cont+=1
                                    elif isinstance(h,Student):
                                        for posts in db["post"]:
                                            if h.id == posts.id_publisher:
                                                posts.view_post()
                                                print("""
                                                    Sigues a este usuario""")
                                                cont+=1
                        else:
                            print("No sigues a este usuario")
                            seguir(db,inicio_username,usernamea_seguir)
                            cont+=1
                            break
        elif option_ver > len(lista_username):
            print("""Elija una opcion valida""")


#Validacion de si lo sigue o no                                       
def seguidos_mostrar_posts(db,inicio_username,username_buscar,id_userbuscado):
    cont=0
    contp=0
    dates = []
    conts=0

    while cont == 0:
        for u in db["users"]:
            if isinstance(u,Professor):
                if inicio_username.lower() == u.username.lower():
                    if id_userbuscado in u.following:
                        conts+=1
                        for u in db["users"]:
                            if isinstance(u,Professor):
                                for posts in db["post"]:                        
                                    if id_userbuscado == posts.id_publisher:
                                        print(f"""{contp+1}.""")
                                        contp+=1
                                        posts.view_post()
                                        
                                        cont+=1
                                        date=posts.date_p
                                        dates.append(date)
                                        mostrar_iteracciones(db,date)
                                        print("="*60)
                                cont+=1
                                break

                                


                            elif isinstance(u,Student):
                                for posts in db["post"]:                        
                                    if id_userbuscado == posts.id_publisher:
                                        print(f"""{contp+1}.""")
                                        contp+=1
                                        posts.view_post()
                                        
                                        cont+=1
                                        date=posts.date_p
                                        dates.append(date)
                                        mostrar_iteracciones(db,date)
                                        print("="*60)
                                cont+=1
                                break
                                        
                                

            elif isinstance(u,Student):
                if inicio_username.lower() == u.username.lower():
                    if id_userbuscado in u.following:
                        conts+=1
                        for u in db["users"]:
                            if isinstance(u,Professor):
                                for posts in db["post"]:                        
                                    if id_userbuscado == posts.id_publisher:
                                        print(f"""{contp+1}.""")
                                        contp+=1
                                        posts.view_post()
                                        
                                        cont+=1
                                        date=posts.date_p
                                        dates.append(date)
                                        mostrar_iteracciones(db,date)
                                        print("="*60)

                                cont+=1
                                break
                                            

                            elif isinstance(u,Student):
                                for posts in db["post"]:                        
                                    if id_userbuscado == posts.id_publisher:
                                        print(f"""{contp+1}.""")
                                        contp+=1
                                        posts.view_post()
                                        
                                        cont+=1
                                        date=posts.date_p
                                        dates.append(date)
                                        mostrar_iteracciones(db,date)
                                        print("="*60)
                                cont+=1
                                break
                                       
                                


                                            

        if conts == 0:
            print("No sigues a este usuario")
            seguir(db,inicio_username,username_buscar)
            break

        if cont == 0:
            print("""
                                            No tiene ningun posts""")
            cont+=1
            break
            
        elif cont != 0:
            seguidos2_continuacion(db,inicio_username,dates)
            cont+=1
            break
            

# Validacion de interactuar o ver interacciones
def seguidos2_continuacion(db,inicio_username,dates):
    cont=0
    while cont==0:
        option_iteracciones = int(input("""
                                                    Que posts desea ver mas opciones 
                                                    0. Ninguno
➥ """))
        if option_iteracciones == 0:
            cont+=1
            break

        elif option_iteracciones <= len(dates):

            option_iteracciones_elegr = input("""
                                                    0. Atras
        
                                                    1. Ver interaciones del posts
                                                    2. Interactuar el posts
➥ """)   
            if option_iteracciones_elegr == "1":
                opciones_posts_interactuar(db,inicio_username,dates[option_iteracciones-1])
                cont+=1
                break

            elif option_iteracciones_elegr == "2":
                comentar_liker(db,inicio_username,dates[option_iteracciones-1])
                cont+=1
                break

            elif option_iteracciones_elegr == "0":
                cont+=1
                break
        elif option_iteracciones > len(dates):
            print("""ELija una option valida""")

#Cambiar informacion personal de la Cuenta
def change_information_account(db,username):

    for u in db["users"]:
        if isinstance(u,Student):
            if u.username.lower() == username.lower():
                u.show_attr()
                while True:
                    option_modificar=input("""
                                                        Que desea modificar:

                                                        0. Nada

                                                        1. Nombre
                                                        2. Apellido
                                                        3. Email
                                                        4. Username
                                                        5. Carrera
➥  """)
                    if option_modificar == "1":
                        firstname=input("Nombre nuevo: ")
                        u.change_info(firstname,u.lastname,u.email,u.username,u.major)

                    elif option_modificar == "2":
                        lastname=input("Apellido nuevo: ")
                        u.change_info(u.firstname,lastname,u.email,u.username,u.major)

                    elif option_modificar == "3":
                       
                        email=actualizar_correo()
                        u.change_info(u.firstname,u.lastname,email,u.username,u.major)
                               

                    elif option_modificar == "4":
                        username_c = actualizar_username(db)
                        if username_c != None:
                            u.change_info(u.firstname,u.lastname,u.email,username_c,u.major)
                            return True
                        else:
                            pass
                            

                    elif option_modificar == "5":
                        major = input("Carrera nueva: ")
                        u.change_info(u.firstname,u.lastname,u.email,u.username,major)
                    elif option_modificar == "0":
                        break
                cargar(db)

        elif isinstance(u,Professor):
            if u.username.lower() == username:
                u.show_attr()
                while True:
                    option_modificar=input("""
                                                        Que desea modificar:

                                                        0. Nada

                                                        1. Nombre
                                                        2. Apellido
                                                        3. Email
                                                        4. Username
                                                        5. Departamento
➥  """)
                    if option_modificar == "1":
                        firstname=input("Nombre nuevo: ")
                        u.change_info(firstname,u.lastname,u.email,u.username,u.department)

                    elif option_modificar == "2":
                        lastname=input("Apellido nuevo: ")
                        u.change_info(u.firstname,lastname,u.email,u.username,u.department)

                    elif option_modificar == "3":
                        email=actualizar_correo()
                        u.change_info(u.firstname,u.lastname,email,u.username,u.department)

                    elif option_modificar == "4":
                        username_c = actualizar_username(db)
                        if username_c != None:     
                            u.change_info(u.firstname,u.lastname,u.email,username_c,u.department)
                            return True
                        else:
                            pass

                    elif option_modificar == "5":
                        department = input("Departamento nuevo: ")
                        u.change_info(u.firstname,u.lastname,u.email,u.username,department)

                    elif option_modificar == "0":
                        break
                cargar(db)


        elif isinstance(u,Admin):
            if u.username.lower() == username:
                u.show_attr()
                while True:
                    option_modificar=input("""
                                                        Que desea modificar:

                                                        0. Nada

                                                        1. Nombre
                                                        2. Apellido
                                                        3. Email
                                                        4. Username
➥  """)
                    if option_modificar == "1":
                        firstname=input("Nombre nuevo: ")
                        u.change_info(firstname,u.lastname,u.email,u.username)

                    elif option_modificar == "2":
                        lastname=input("Apellido nuevo: ")
                        u.change_info(u.firstname,lastname,u.email,u.username)

                    elif option_modificar == "3":
                        
                            email=actualizar_correo()
                            u.change_info(u.firstname,u.lastname,email,u.username)
                            break

                    elif option_modificar == "4":
                        username_c = actualizar_username(db)
                        if username_c != None:
                            u.change_info(u.firstname,u.lastname,u.email,username_c)
                            return True
                        else:
                            pass

                    elif option_modificar == "5":
                        major = input("Carrera nueva: ")
                        u.change_info(u.firstname,u.lastname,u.email,u.username)
                    elif option_modificar == "0":
                        break
            cargar(db)

def actualizar_correo():
    while True:
        email = input (" Acutualizar Email: ")
        if "@correo.unimet.edu.ve" in email:
            return email
        else:
            print("correo no valido")
            
def actualizar_username(db):
    cont=0
    while True:
        username = input (" Nuevo username: ")
        for u in db["users"]:
            if u.username.lower() == username.lower():
                cont+=1
                    
        if cont == 0:
            option = input(""" 
                                Seguro te quieres cambiar el username
                                (Se va a cerrar sesion)

                                1. Si
                                2. No
➥ """)
            if option == "1":
               return username.lower()
            elif option == "2":
                return None
        else:
            print("username en uso")
            cont=0

#Borrar una cuenta
def borrar_datos(db,username):
    conts=0



    for u in db["users"]:
        conts+=1
        if username.lower() == u.username.lower():
            option=input("""SEGURO DESEA ELIMINAR SU CUENTA:
1. Si
2. No
➥ """)
            if option == "1":
                del db["users"][conts-1]
                cargar(db)
                return True
            elif option == "2":
                return False
                    

#Ver los comentarios y posts y lograr entrar a un perfil(SE PUEDE RECORTAR) PROBAR
def opciones_posts_interactuar(db,username,date):
     
     #Casi listo
    cont = 0
    perfiles_c = []
    while True:
        option = input("-"*160+f"""
                                                            Elija una option:

                                                            0. Atras

                                                            1. Ver Comentarios
                                                            2. Ver likes 
➥ """)
        if option == "1":
            cont1=0
            for posts in db["post"]:
                if date == posts.date_p:
                    for comentario in posts.comentarios:
                        for k,v in comentario.items():
                            print(f"""
                                                            Comentarios""")
                            cont +=1
                            print(f"""
                                                            {cont}->{k}:{v[0]}  Date:{v[1]}""")
                            perfiles_c.append(k.lower())
                            
                        while cont1==0:    
                            option_interactuar = int(input("""
                                                           
                                                            0. Ninguno
                                                            Que perfil desea entrar(numero)
➥ """))
                            if option_interactuar == 0:
                                cont1+=1
                                break

                            elif option_interactuar <= len(perfiles_c):
                                for u in db["users"]:
                                    if u.username.lower() == perfiles_c[option_interactuar-1]:
                                        cont+=1
                                        id_userbuscado = u.id
                                        print(f"""
                                                        @{u.username}""")
                                        option_ver=input("""
                                                        Desea ver el perfil
                                                        1. Si
                                                        2. No
➥ """)
                                        if option_ver == "1":
                                            u.show_attr()
                                            seguidos_mostrar_posts(db,username,perfiles_c[option_interactuar-1],id_userbuscado)
                                            cont1+=1
                                            break
                        
                        
                                        elif option_ver == "2":
                                            cont1+=1
                                            break

                            elif option_interactuar >= len(perfiles_c):
                                    print("""Elija una opcion valida""")
                        break
                                

        elif option == "2":
            perfiles_l = []
            cont2=0
            for posts in db["post"]:
                if date == posts.date_p:
                    for i,y in enumerate(posts.likes):

                        print(f""" Total:  {len(posts.likes)} ❤️
{i+1}. {y}""")
                    while cont2==0:    
                        option_interactuar = int(input("""
                                                            0. Ninguno
                                                            Que perfil desea entrar(numero)
➥ """))
                        if option_interactuar == 0:
                            cont2+=1
                            break
                        elif option_interactuar <= len(perfiles_l):
                            for u in db["users"]:
                                if u.username.lower() == perfiles_l[option_interactuar-1]:
                                    cont+=1
                                    id_userbuscado = u.id
                                    print(f"""
                                                        @{u.username}""")
                                    option_ver=input("""
                                                        Desea ver el perfil
                                                        1. Si
                                                        2. No
➥ """)
                                    if option_ver == "1":
                                        u.show_attr()
                                        seguidos_mostrar_posts(db,username,perfiles_l[option_interactuar-1],id_userbuscado)
                                        cont2+=1
                                        break
                    
                    
                                    elif option_ver == "2":
                                        cont2+=1
                                        break
                        elif option_interactuar >= len(perfiles_l):
                            print("""Elija una opcion valida""")
                    break
        elif option == "0":
            break

#=================================================== MODULO GESTION DE MULTIMEDIA ==============================================            


#Crear un post
def registrar_post(db,username):

    tags=[]
    multimedia={}

    option_type=input("""
                                                        1. Foto
                                                        2. Video
➥ """)
    if option_type == "1":
        type="photo"

    elif option_type == "2":
        type="video"

    caption=input("""
                                                        Descripcion:
➥ """)
    
    while True:
        option_tags=input("""
                                                        0. Solo esos:               
                                                        Que hashtags quieres (Escriba uno por uno):
➥  """)
        if option_tags == "0":
            break
        else:
            tags.append(option_tags.lower())

    option_multimedia=input("""
                                                        Escriba el url del video o photo que quiere publicar: 
➥ """)
    multimedia["type"]=type
    multimedia["url"]=option_multimedia

    for u in db["users"]:
        if isinstance(u,Student):
            if username.lower() == u.username.lower():
                id_publisher = u.id
                date = datetime.datetime.now()
        
        elif isinstance(u,Professor):
            if username.lower() == u.username.lower():
                id_publisher = u.id
                date = datetime.datetime.now()

    db["post"].append(Post(id_publisher,type,caption,str(date),tags,multimedia,[],[]))
    cargar(db)

    print("""
                                                        Se ha subido con exito
          """)

#Seguir a un Usuario
def seguir(db,inicio_username,username_buscar):
    cont=0
    contw=0
    while cont == 0:
        option_seguir=input("""
                                                    Desea seguir a este ususario (Podra ver mejor su perfil):
                        
                                                    1. Si
                                                    2. No
➥ """)
        if option_seguir == "1":
            for u in db["users"]:
                if isinstance(u,Professor):
                    if u.username.lower() == inicio_username.lower():
                        contw+=1
                        for u in db["users"]:
                            if isinstance(u,Student):
                                if u.username.lower() == username_buscar.lower():
                                    u.follow(inicio_username)
                                    cont+=1
                                    contw+=1
                                    cargar(db)
                                    break
                            elif isinstance(u,Professor):
                                if u.username.lower() == username_buscar.lower():
                                    u.follow(inicio_username)
                                    cont+=1
                                    contw+=1
                                    cargar(db)
                                    break
                elif isinstance(u,Student):
                    if u.username.lower() == inicio_username.lower():
                        contw+=1
                        for u in db["users"]:
                            if isinstance(u,Student):
                                if u.username.lower() == username_buscar.lower():
                                    id_user_buscar = u.id
                                    print(id_user_buscar)
                                    if seguir_Students(db,inicio_username,username_buscar,id_user_buscar) == True:
                                        cont+=1
                                        contw+=1
                                        break
                                    else:
                                        u.follow(inicio_username)
                                        cont+=1
                                        contw+=1
                                        cargar(db)
                                        break
                            elif isinstance(u,Professor):
                                if u.username.lower() == username_buscar.lower():
                                    u.follow(inicio_username)
                                    cont+=1
                                    contw+=1
                                    cargar(db)
                                    break
        

        elif option_seguir == "2":
            cont+=1
            break

def seguir_Students(db,inicio_username,username_buscar,id_user_buscar):
    

    for u in db["users"]:
        if isinstance(u,Student):
            if u.username.lower() == inicio_username.lower():
                major_p = u.major

    for u in db["users"]:
        if isinstance(u,Student):
            if u.username.lower() == username_buscar.lower():
                major_f = u.major
        elif isinstance(u,Professor):
            if u.username.lower() == username_buscar.lower():
                major_f = u.department

    
    if major_p == major_f:
        for u in db["users"]:
            if isinstance(u,Student):
                if u.username.lower() == inicio_username.lower():
                    u.follow_sameMajor(id_user_buscar,username_buscar)
                    cargar(db)
                    return True


#Aceptar o rechazar un requests            
def aceptar_requests(db,username):
    #ARREGLAR
    cont = 0
    print("""                                                     Requests:""")
    while cont == 0:
        for u in db["users"]:
            if username.lower() == u.username.lower():
                id_Inicio = u.id
                if len(u.requests) == 0:
                    print("""
                                                    No tienes requests""")
                    cont+=1
                    break
                elif len(u.requests) != 0:
                    for y,i in enumerate(u.requests):
                        print(f"""
                                                    {y+1}. @{i}""")
                    
                    aceptar_requests2(db,username,id_Inicio)
                    cont+=1
                    break

def aceptar_requests2(db,username,id_Inicio):
    cont=0
    while cont==0:
        option_request = input("""
                                                        0.Atras
                                           
                                                        1. Aceptar a todos
                                                        2. Rechazar a todos
                                                        3. Aceptar a uno solo
➥ """)
        if option_request == "1":
            for i in u.requests:
                for u in db["users"]:
                    if isinstance(u,Student):
                        if i.lower() == u.username.lower():
                            u.following.append(id_Inicio)
                            cargar(db)
                            #Limpiar la lista de requests
                            print(f"Aceptaste a todos")
                            cont+=1
                            for u in db["users"]:
                                if username.lower() == u.username.lower():
                                    u.vaciar_request()
                            break
                    elif isinstance(u,Professor):
                        if i.lower() == u.username.lower():
                            u.following.append(id_Inicio)

                            cargar(db)
                            #Limpiar la lista de requests
                            print(f"""
                                                        Aceptaste a todos""")
                            cont+=1
                            for u in db["users"]:
                                if username.lower() == u.username.lower():
                                    u.vaciar_request()
                            break


        elif option_request == "2":
            u.vaciar_request()
            cargar(db)
            print("""
                                                        No aceptaste a ninguno""")
            break

        elif option_request == "3":
            options = int(input("""
                                                        Que numero desea aceptar:
                                                        0. Nninguno
    ➥ """))

            if options == 0:

                cont+=1
                break
            elif options != 0:
                for u in db["users"]:
                    if username.lower()== u.username.lower():
                        username_requests = u.requests[options-1] 
                        print(f"""
                                                        Aceptaste a @{username_requests}
    """)
                        u.Remove_person_requests(username_requests)
                        for u in db["users"]:
                            if username_requests == u.username.lower():
                                u.Add_followings(id_Inicio)
                                cargar(db)

                            cont+=1
                            break

                            
        elif option_request == "0":
            cont+1
            break


#buscar posts Hashtag y user (TERMINAR FALTA SOLO USERS)
def buscar_posts_hashtag(db,inicio_username):
    cont=0
    conts=0
    contposts=0
    dates=[]
    print(""" =========================================    [Buscador de Posts]    ============================================ """)
    while cont == 0:
        print()
        hashtag = input("""
                                                    Escriba un hashtag: 
➥ """).lower()

        for posts in db["post"]:
            for hash in posts.tags:
                if hashtag.lower() == hash:
                    cont+=1
                    id_posts = posts.id_publisher
                    for u in db["users"]:
                        if inicio_username.lower() == u.username.lower():
                            if id_posts in u.following:
                                conts+=1
                                for posts in db["post"]:
                                    if id_posts == posts.id_publisher:
                                        if hashtag in posts.tags:
                                            date=posts.date_p
                                            dates.append(date)
                                            contposts+=1
                                            print(f"{contposts}.")
                                            posts.view_post()
                                            mostrar_iteracciones(db,date)
                                            print("="*60)
                            else:
                                for u in db["users"]:
                                    if id_posts == u.id:
                                        print(f"""
                                                    No sigues a @{u.username.lower()}
""")
                                        
                                        seguir(db,inicio_username,u.username.lower())
                                        cont+=1
                                        break

                    
                        
        if cont == 0:
            print("No se encuntra ese hashtag")

        elif contposts != 0:
            buscar_posts_hashtag2(db,inicio_username,dates)

def buscar_posts_hashtag2(db,inicio_username,dates):
    while True:
        option_iteracciones = int(input("""
                                                        Que posts desea interacturar: 
                                                        0. Ninguno
➥ """))

        if option_iteracciones == 0:
            break
        elif option_iteracciones != 0:
            option_iteracciones_elegr = input("""
                                                        0. Atras
                                                        1. Ver interaciones del posts
                                                        2. Interactuar el posts
➥ """)   
            if option_iteracciones_elegr == "1":
                opciones_posts_interactuar(db,inicio_username,dates[option_iteracciones-1])
                break
            
            elif option_iteracciones_elegr == "2":
                comentar_liker(db,inicio_username,dates[option_iteracciones-1])
                break
            
            elif option_iteracciones_elegr == "0":
                break

#Comentar o dar like
def comentar_liker(db,username,date):
    cont = 0
    while cont == 0:
        option = input("-"*60+f"""
                       
                                                    Elija una opcion:

                                                    0. Atras

                                                    1. Comentar
                                                    2. Dar ❤️
➥ """)
        if option == "1":
            for posts in db["post"]:
                
                if posts.date_p == date:
                    comentario = {}
                    comen = []

                    c = input("""
                                                    Que comentario desea agregar
➥ """)
                    datecomen = datetime.datetime.now()
                    comen.append(c)
                    comen.append(str(datecomen))

                    comentario[username]=comen

                    posts.comentar(comentario)
                    cargar(db)

                    posts.view_post()
                    mostrar_iteracciones(db,date)
                    

        elif option == "2":

            like(db,username,date)
            
            

        elif option == "0":
            cont+=1
                 

def like(db,username,date):
    cont=0
    
    for posts in db["post"]: 
        if posts.date_p == date:
            for i in posts.likes:
                if username == i:
                    username_r = username
                    cont+=1
                    posts.quitar_like(username_r)
                    print("""
                                            Has quitado el ❤️
                          """)
                    cargar(db)
                    posts.view_post()
                    mostrar_iteracciones(db,date)
                    cargar(db)

    if cont == 0:
        for posts in db["post"]:
            if posts.date_p == date:
                posts.like(username)
                print("""
                                            Le diste ❤️ 
                    """)
                cargar(db)
                posts.view_post()
                mostrar_iteracciones(db,date)
                cargar(db)
           

#Mostrar interacciones en posts 
def mostrar_iteracciones(db,date):
    cont=0

    while cont == 0:

        for posts in db["post"]:
            if posts.date_p == date:
                
                
                print(f"""
❤️  {len(posts.likes)}""")
                
                for comentario in posts.comentarios:
                    for k,v in comentario.items():
                        x = slice(0,10)
                        y = slice(11,19)
                        print(f"""
Comentarios:""")
                        print(f"""->{k}:{v[0]}  Date:{v[1][x]} a las {v[1][y]} """)
                
                cont+=1
                break
                        
                        
        if cont==0:
            print(f"""
❤️ "0"
Sin comentarios""")
            break
        cont+=1

#=================================================== MODULO ADMIN ==============================================            


#Buscador de perfiles de admin
def buscador_perfiles_admin(db):
    print(""" =========================================    Buscador de perfiles    ============================================ """)
    
    cont=0
    contposts=0
    while cont == 0:

        username_buscar=input("""
                                                Que username desea buscar:
➥ """) 
        for u in db["users"]:
            if isinstance(u,Student):
                if u.username.lower() == username_buscar.lower():
                    cont+=1
                    id_userbuscado = u.id
                    print(f"""                  
                                                @{u.username}""")
                    option_ver=input("""
                                                Desea ver el perfil
                                     
                                                1. Si
                                                2. No
➥ """)
                    if option_ver == "1":
                        u.show_attr()

                        print("Seguidos:")  
                        
                        for s in u.following:
                            for i in db["users"]:
                                if i.id == s:
                                    print(f"""
                                                -{i.username}""")

                        print("""
                                    Publicaciones:""")
                        
    

                        
                        for posts in db["post"]:                        
                            if id_userbuscado == posts.id_publisher:
                                print(f"{contposts+1}.")
                                posts.view_post()
                                for i in posts.tags:
                                    print(f"#{i}")
                                contposts+=1 
                                mostrar_iteracciones(db,posts.date_p)                       
                        break
                    
                    
                    elif option_ver == "2":
                        break

        
            elif isinstance(u,Professor):
                if username_buscar.lower() == u.username.lower():
                    cont+=1
                    id_userbuscado = u.id
                    print(f"""
                                                @{u.username}""")
                    option_ver=input("""
                                                Desea ver el perfil
                                                1. Si
                                                2. No
➥ """)
                    if option_ver == "1":
                        u.show_attr()

                        print("Seguidos:")  
                        
                        for s in u.following:
                            for i in db["users"]:
                                if i.id == s:
                                    print(f"-{i.username}")

                        print("""
                                    Publicaciones:""")
    

                        
                        for posts in db["post"]:                        
                            if id_userbuscado == posts.id_publisher:
                                print(f"{contposts+1}.")
                                posts.view_post()
                                contposts+=1
                                mostrar_iteracciones(db,posts.date_p)    

                    elif option_ver == "2":
                        break

        if cont == 0:
            print("""
                    Este Usuario No existe""")
            break   

#Buscador de posts Admin
def buscar_posts_hashtag_Admin(db):
    print(""" =========================================    Buscador de posts ADMIN    ============================================ """)
    while True:

        option = input("""
                                                        Filtro de busqueda: 
                                                        0. Atras

                                                        1. Hashtag
                                                        2. User
➥ """)
        if option == "1":
            hashtag(db)
            cargar(db)
            break


        elif option == "2":
           Posts_username(db)
           cargar(db)
           break

        elif option == "0":
            break

#Complemento de de buscar posts Admin
def hashtag(db):
     contpostsh=0
     datesh=[]
     cont=0
    
     while cont == 0:
        hashtag = input("""
Escriba un hashtag: 
➥ """).lower()

        for posts in db["post"]:
            for hash in posts.tags:
                if hashtag.lower() == hash:
                    contpostsh+=1
                    id_posts = posts.id_publisher
                    date=posts.date_p
                    datesh.append(date)
                    print(f"{contpostsh}.")
                    posts.view_post()
                    mostrar_iteracciones(db,date)
                    print("="*60)
                    cont+=1

        if cont == 0:
            print("""No se encuentra ese hashtag""")
            cont+=1
            break

        else:
            option_mas_opciones = int(input("""
0. Ninguno
Cual posts desea tener mas opciones: 
➥ """))
            if option_mas_opciones == 0:
                cont+=1
                break
            elif option_mas_opciones != 0:
                moderador_posts(db,datesh[option_mas_opciones-1])
                break

def Posts_username(db):
    contpostsu=0
    cont=0
    datesu=[]
    while cont == 0:
        user = input("""
                                        A que user le deseas ver los posts: 
➥ """)
        for u in db["users"]:
            if u.username.lower() == user.lower():
                for posts in db["post"]:
                    if u.id == posts.id_publisher:
                        contpostsu+=1
                        date = posts.date_p
                        datesu.append(date)
                        print(f"{contpostsu}.")
                        mostrar_iteracciones(db,date)
                        print("="*60)
                        cont+=1
                    
        if cont == 0:
            print("No existe ese username")
        
        else:
            option_mas_opciones = int(input("""
                                        0. Ninguno
                                        Cual posts desea tener mas opciones: 
➥ """))
            if option_mas_opciones == 0:
                break
            elif option_mas_opciones != 0:
                moderador_posts(db,datesu[option_mas_opciones-1])
                break


#Acciones de un admin con los posts
def moderador_posts(db,date):
    contp = 0
    
    while True:
        for posts in db["post"]:
            contp+=1
            if date == posts.date_p: 
                for u in db["users"]:
                    if posts.id_publisher == u.id:
                
                        user_person = u.username.lower()
                    
                        delete_posts_comentario(db,user_person,contp,date) 
                        cargar(db)
        break        

def delete_posts_comentario(db,user_person,contp,date):
    contcomen=0
    lista_comentarios = []
    strikes_u ={}
    cont=0
    while cont==0:
        option = input("""
                                            0. Atras

                                            1. Eliminar post 
                                            2. Eliminar Comentario ofensivo
➥ """)
        if option == "1":
            razonp = input("Razon porque le borra el posts:  ")
            del db["post"][contp-1] 
            cont+=1
            for u in db["users"]:
                if user_person == u.username.lower():
                    strikes_u["post"] = razonp
                    u.strikes.append(strikes_u)
            print(f"""
                                            Elimino un posts de {user_person}
""")
                    
            break

        elif option =="2":
            for posts in db["post"]:
                if posts.date_p == date:
                    for c, comen in enumerate(posts.comentarios):
                        contcomen+=1
                        for k,v in comen.items():
                            lista_comentarios.append(v[1])
                            print("="*60+f"""
{c+1}. User: {k} Comento: {v[0]} Fecha: {v[1]}""")
                            
                    option_comen = int(input("""
                                            Cual desea borrar
                                            0. Ninguno
➥"""))
                    if option_comen == 0:
                        cont+=1
                        break
                    elif option_comen !=0:
                    
                        razon_comen=input("Porque elimino el comentario: ")
                        del posts.comentarios[option_comen-1]
                        cont+=1
                        print("Comentario eliminado")
                        for u in db["users"]:
                            if user_person == u.username.lower():
                                strikes_u["comentario"] = razon_comen
                                u.strikes.append(strikes_u)
                        break


        elif option == "0":
            cont+=1
            break    
        if contcomen == 0:
            print("""
                                                No tiene comentarios
                  """)

def view_perfil_admin(db,username):
    
    for u in db["users"]:
        if isinstance(u,Student):
            if u.username.lower() == username.lower():
                u.show_attr()
        elif isinstance(u,Professor):
            if u.username.lower() == username.lower():
                u.show_attr()
        
def tumbar_cuenta(db,admin):
    cont=0
    cont2=0
    
    for u in db["users"]:
        cont+=1
        
        if len(u.strikes) >= 3:
            username=u.username.lower()
            for u in db["admin"]:
                if u.username.lower() == admin:
                    u.usuarios_eliminados.append(username)

            del db["users"][cont-1]

            print(f"""
                        La cuenta @{username} ha sido eliminado por exceder las infracciones
                                                """)
            cont2+=1
            cargar(db)
            

    if cont2==0:     
       print("Todavia nadie a pasado el limite de infracciones")     


#=================================================== MODULO ESTADISTICAS ==============================================
def gestion_Estadisticas(db):

#   4. Realizar gráficos con dichas estadísticas con las librerías de mathplotlib o
#Bokeh (Bono).

    contp=0
    
    while True:
        print("""
                                                [Indicadores de gestión (Estadísticas)]
          """)
        option_principal = input("""
                                                0. Atras

                                                1. Generar informes de publicaciones
                                                2. Generar informes de interacción con la siguiente información
                                                3. Generar informes de moderación con la siguiente información
➥ """)
        if option_principal == "1":
            while True:
                option_informes_posts = input("""
                                                0. Atras                                          

                                                1. Usuarios con mayor cantidad de publicaciones
                                                2. Carreras con mayor cantidad de publicaciones
➥ """)
                if option_informes_posts == "1":
                
                    ids_usuarios = []
                    ids_posts=[]
                    result = {}


                    for u in db["users"]:
                        ids_user = u.id
                        ids_posts.append(ids_user)
                        ids_usuarios.append(ids_user)
                    
                    
                    for posts in db["post"]:
                        count_posts = posts.id_publisher
                        ids_posts.append(count_posts)
    
                    for i in range(0,len(ids_usuarios)):
                    
                        result[ids_usuarios[i]]=ids_posts.count(ids_usuarios[i])

                    result_order = sorted(result.items(), key=operator.itemgetter(1), reverse=True)

    
                    for i in range(0,4):       
                        for user in db["users"]:
                            if user.id == result_order[i][0]:
                                print(f"""{i+1}. {user.username} con {result_order[i][1]-1}""")
                                

                elif option_informes_posts == "2":
                    ids_usuarios = []
    
                    ids_posts=[]
    
                    result = {}
    
                    for u in db["users"]:
                        if isinstance(u,Student):
                            ids_user = u.id
                            ids_posts.append(ids_user)
                            ids_usuarios.append(ids_user)
                    
                    
                    for posts in db["post"]:
                        count_posts = posts.id_publisher
                        ids_posts.append(count_posts)
    
                    for i in range(0,len(ids_usuarios)):
                    
                        result[ids_usuarios[i]]=ids_posts.count(ids_usuarios[i])

                    result_order = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    
                    for i in range(0,4):   
                        for u in db["users"]:
                            if isinstance(u,Student):
                                if u.id == result_order[i][0]:
                                    print(f"""{i+1}. {u.major} con {result_order[i][1]-1}""")
    
         
                elif option_informes_posts == "0":
                    break

        elif option_principal == "2":
            cont=0
            while True:
                option_informe_interaccion = input("""
                                                    0. Atras 

                                                    1. Post con la mayor cantidad de interacciones
                                                    2. Usuarios con la mayor cantidad de interacciones (dadas y enviadas)
➥ """)
                coments={}

                if option_informe_interaccion == "1":
                    for posts in db["post"]:
                        suma_interacciones=len(posts.comentarios)+len(posts.likes)
                        if suma_interacciones != 0:
                            coments[posts.date_p] = suma_interacciones
                            cont+=1


                    #comenatarios_rts = sorted(coments.items(), key=operator.itemgetter(1), reverse=True)

                    

                    for i in range(2):
                        for posts in db["post"]:
                            for c,y in coments.items():
                                if posts.date_p == c:
                                    print("""
                                                    == Post con mas interacciones == 
                                  """)
                                    posts.view_post()
                                    mostrar_iteracciones(db,posts.date_p)

                    if cont == 0:
                        print("""
                                                    Todavia no hay ninguna interaccion
                              """)

                #ARREGLARRRR
                elif option_informe_interaccion == "2":

                    contc= 0
                    comenatarios = {}
                    contl=0
                    co = 0 


                    for u in db["users"]:
                        for posts in db["post"]:
                            if u.id == posts.id_publisher:
                                suma_interacciones = len(posts.comentarios) + len(posts.likes)
                                if suma_interacciones != 0:
                                    comenatarios[u.id]=suma_interacciones
                    
                    for u in db["users"]:                
                        for posts in db["post"]:
                            for c in posts.comentarios:
                                for k,v in c.items():
                                    if k == u.username.lower():
                                        contc+=1

                                        comenatarios[u.id]=+contc
                            for l in posts.likes:
                                if l == u.username:
                                    contl+=1
                                    comenatarios[u.id]=+contl
                    print("""
                                                    Usuarios con mayores interaciones 
                          """)
                    
                    
                    for u in db["users"]:
                        for s,j in comenatarios.items():
                            if u.id == s:
                                co+=1
                                print(f"""{co}. @{u.username.lower()} = {j}""")
                                
                    

                elif option_informe_interaccion == "0":
                    break

           
        
        elif option_principal == "3":
            while True:
                option_moderador = input ("""
                                                    0. Atras  

                                                    1. Usuario con la mayor cantidad de post tumbados
                                                    2. Carreras con mayor comentarios inadecuados.
                                                    3. Usuarios eliminados por infracciones.
➥ """)
                if option_moderador == "1":
                    cont=0

                    for u in db["users"]:
                        if len(u.strikes) != 0:
                            for s in u.strikes:
                                for k, v in s.items():
                                    if k == "post":
                                        username = u.username.lower()
                                        print(f"""
                                                    -{username} con {len(u.strikes)} post tumbados
                                            """)
                                        cont+=1
                    if cont == 0:
                        print("""
                                                    No se ha tumado ningun post todavia 
                              """)



                elif option_moderador == "2":
                    cont=0

                    for u in db["users"]:
                        if isinstance(u,Student):
                            for s in u.strikes:
                                for k, v in s.items():
                                    if k == "comentario":
                                        major = u.major
                                        print(f"""-{major} con {len(u.strikes["comentario"])} comentarios inadecuados
                                            """)
                                        cont+=1
                    if cont == 0:
                        print("""
                                                    No ha comentado ningun estudiante todavia""")


                elif option_moderador == "3":
                    cont=0
                    for u in db["users"]:
                        if isinstance(u,Admin):
                            for i,c in enumerate(u.usuarios_eliminados):
                                print(f"""
                                                    Usuarios eliminados:
                                      
""")
                                print(f"{i}. {c}")
                                cont+=1
                    if cont == 0:
                        print("""
                                                    No hay usuarios elimador por infracciones todavia
                              """)
                            
                elif option_moderador == "0":
                    break
                        

        elif option_principal == "0":
            break






                                        
                                        







        
    

                

                                            