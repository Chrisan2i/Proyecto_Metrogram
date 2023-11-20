class Post:
    def __init__(self,id_publisher,type,caption,date_p,tags,multimedia,likes,comentarios):
        self.id_publisher=id_publisher
        self.type=type
        self.caption=caption
        self.date_p=date_p
        self.tags=tags
        self.multimedia = multimedia
        self.likes=likes
        self.comentarios = comentarios

    def view_post(self):
        hashtags = ""
        for tag in self.tags:
            if len(hashtags) == 0:
                hashtags += f"#{tag}"
            else:
                hashtags += f" #{tag}"
        x = slice(0, 10)
        y = slice(11,19)
        print("-"*60 + f"""
Tipo: {self.type}
Descripcion: {self.caption}
Publicado: {self.date_p[x]} a las {self.date_p[y]}
tags: {hashtags}""")

        
    def comentar(self,comentario):
        self.comentarios.append(comentario)
    
    def quitar_comentario(self,comentario):
        self.comentarios.remove(comentario)

    def like(self,username):
        self.likes.append(username)

    def quitar_like(self,username):
        self.likes.remove(username)
    

        


