
from funciones import *
import requests
import json

from usuario import Student, Professor,Admin
from post import Post




def create_object(db):

    cont=0

    url1 = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/08d4d2ce028692d71e9f8c32ea8c29ae24efe5b1/users.json"
    url2 = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/main/posts.json"
    
    archivos_users = None
    archivos_posts = None

    while True:
        x = input()
        if x == "1":
            with open("Metrogram_post.json","r") as file:
                archivos_posts = json.load(file)
            with open("Metrogram_users.json","r") as file:
                archivos_users = json.load(file)

            for i in archivos_users:
                if i["type"] == "professor":
                    db["users"].append(Professor(i['id'],i['firstName'],i['lastName'],i['email'],i['username'],i['type'],i['department'],i['following'],i["request"],i["strikes"]))   
                    
                elif i["type"] == "student":
                    db["users"].append(Student(i['id'],i['firstName'],i['lastName'],i['email'],i['username'],i['type'],i['major'],i['following'],i["request"],i["strikes"]))
                
                elif i["type"] == "admin":
                    db["admin"].append(Admin(i['id'],i['firstName'],i['lastName'],i['email'],i['username'],i['type'],i["key"],i["usuarios_eliminados"]))

            for i in archivos_posts:
                db["post"].append(Post(i['publisher'],i['type'],i['caption'],i['date'],i['tags'],i['multimedia'],i["likes"],i["comentarios"]))

            print("Cargando archivos")
            cont+=1
            break


        else:
            url1 = requests.get(url1)
            url2 = requests.get(url2)
            
            if url1.status_code == 200 and url2.status_code == 200:
                archivos_users = url1.json() 
                archivos_posts = url2.json()
                break

    if cont ==0:
        for i in archivos_users:
            if i["type"] == "professor":
                db["users"].append(Professor(i['id'],i['firstName'],i['lastName'],i['email'],i['username'],i['type'],i['department'],i['following'],[],[]))   
        #Creamos el objeto Student en el data_base
            if i["type"] == "student":
                db["users"].append(Student(i['id'],i['firstName'],i['lastName'],i['email'],i['username'],i['type'],i['major'],i['following'],[],[]))
            
        db["admin"].append(Admin("!@#21053101","Christian","Sanchez","christian.sanchez@correo.unimet.edu.ve","chris2i","admin","2105",[]))
        db["admin"].append(Admin("123@#$123","Antonio","Guerra","antonio.guerra@correo.unimet.edu.ve","AntonioGuerra","admin","3101",[]))

        


        for i in archivos_posts:
            db["post"].append(Post(i['publisher'],i['type'],i['caption'],i['date'],i['tags'],i['multimedia'],[],[]))
    
    
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


def main():
    db=data_base()

    create_object(db)

    cont=0

    while True:
        cont=0
        print("*"*50 + """ 📷 BIENVENIDO A METROGRAM 📷 """ +"*"*50)
        option=input(""" 

                                                    0. Salir

                                                    1. Iniciar Sesion
                                                    2. Registrarse                                                        
➥ """)
        
        if option == "1":
                
            while cont == 0:

                username=input("""
                                                    Porfavor introduzca su username: 
➥ """).lower()

                if login(db,username) == False:
                    cont+=1
                    break
                else:
                    if valid_login(db,username) == "admin":
                        while True:
                            print(f"""
                                                    === [Sesion iniciada: {username}] ===
""")

                            option_admin=input("""
                                                    0. Cerrar sesion

                                                    1. Mi perfil
                                                    2. Buscar perfiles
                                                    3. Buscar posts #
                                                    4. Indicadores de gestión (Estadísticas)
                                                    5. Tumbar cuentas
➥ """)
                            if option_admin == "1":

                                while True:
                                    print("""
                                                    === [Mi perfil] ===
                                          """)
                                    option_admin_perfil=input("""      
                                                    0.Atras

                                                    1. Mostrar Informacion de la cuenta
                                                    2. Cambiar informacion personal de la cuenta
                                                    3. Borrar cuenta
➥ """)

                                    if option_admin_perfil == "1":
                                        view_perfil_admin(db,username)
                                    elif option_admin_perfil == "3":
                                        change_information_account(db,username)
                                    elif option_admin_perfil == "4":

                                        if borrar_datos(db,username) == True:
                                            print("Su cuenta se ha eliminado exitosamente")
                                            break
                                
                                        else:
                                            pass

                                    elif option_admin_perfil== "0":
                                        break
                            elif option_admin == "2":
                                 buscador_perfiles_admin(db)

                            elif option_admin == "3":
                                buscar_posts_hashtag_Admin(db)

                            elif option_admin =="4":
                                gestion_Estadisticas(db)
                            
                            elif option_admin == "5":
                                tumbar_cuenta(db,username)
                                
                    
                            elif option_admin == "0":
                                print(f"""
                                                            Sesion cerrada de {username}""")
                                cont+=1
                                break
                            
                    elif valid_login(db,username) != "admin":
                        

                        while cont == 0:
                            print(f"""
                                                    === [Sesion iniciada: {username}] ===
""")

                            option_principal=input("""
                                                    0. Cerrar sesion
                                                   
                                                    1. Mi perfil
                                                    2. Crear un post
                                                    3. Mis posts
                                                    4. Buscar perfiles
                                                    5. Requests
                                                    6. Buscar posts #
➥ """)
            
                            if option_principal == "1":

                                while cont == 0:
                                    print("""
                                                    === [Mi perfil] ===
                                          """)
                                    option_perfil = input("""   
                                                    0.Atras
                                                          
                                                    1. Mostrar informacion de la cuenta
                                                    2. Seguidos
                                                    3. Cambiar informacion personal de la cuenta
                                                    4. Borrar cuenta

➥ """)
                                    if option_perfil == "1":
                                        view_MIPefil(db,username)

                                    elif option_perfil == "2":
                                        dejar_de_seguir(db,username)
                                    elif option_perfil == "3":
                                        if change_information_account(db,username) == True:
                                            cont+=1
                                    elif option_perfil == "4":
                                        if borrar_datos(db,username) == True:
                                            print("Su cuenta se ha eliminado exitosamente")
                                            cont+=1
                                            break
                                        
                                        else:
                                            print("gracias por no eliminar su cuenta")
                                            break
                                

                                    elif option_perfil == "0":
                                        break

                            elif option_principal == "2":
                                registrar_post(db,username)
                                
                            elif option_principal == "3":
                                view_MIPost(db,username)

                            elif option_principal == "4":
                                buscar_usuario(db,username)
                            
                            elif option_principal == "5":
                                aceptar_requests(db,username)
                            
                            elif option_principal == "6":
                                buscar_posts_hashtag(db,username)

                            elif option_principal == "7":
                                gestion_Estadisticas(db)



                    
                            elif option_principal == "0":
                                print(f"""
                                                    === [Sesion cerrada: {username}] ===
""")
                                cont+=1
                                break
                                


        elif option == "2":
            registrarse(db)
        elif option == "0":
            break

main()
