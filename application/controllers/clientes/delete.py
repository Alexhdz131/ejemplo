import config
import hashlib
import app

class Delete:
    
    def __init__(self):
        pass

    def GET(self, id_evento, **k):
        if app.session.loggedin is True: # validate if the user is logged
            # session_username = app.session.username
            session_privilege = app.session.privilege # get the session_privilege
            if session_privilege == 0: # admin user
                return self.GET_DELETE(id_evento) # call GET_DELETE function
            elif session_privilege == 1: # guess user
                raise config.web.seeother('/guess') # render guess.html
        else: # the user dont have logged
            raise config.web.seeother('/login') # render login.html

    def POST(self, id_evento, **k):
        if app.session.loggedin is True: # validate if the user is logged
            # session_username = app.session.username
            session_privilege = app.session.privilege
            if session_privilege == 0: # admin user
                return self.POST_DELETE(id_evento) # call POST_DELETE function
            elif session_privilege == 1: # guess user
                raise config.web.seeother('/guess') # render guess.html
        else: # the user dont have logged
            raise config.web.seeother('/login') # render login.html

   
    @staticmethod
    def GET_DELETE(id_evento, **k):
        message = None # Error message
        id_evento = config.check_secure_val(str(id_evento)) # HMAC id_cliente validate
        result = config.model.get_clientes(int(id_evento)) # search  id_cliente
        result.id_evento = config.make_secure_val(str(result.id_evento)) # apply HMAC for id_cliente
        return config.render.delete(result, message) # render delete.html with user data

    
    @staticmethod
    def POST_DELETE(id_evento, **k):
        form = config.web.input() # get form data
        form['id_evento'] = config.check_secure_val(str(form['id_evento'])) # HMAC id_cliente validate
        result = config.model.delete_clientes(form['id_evento']) # get clientes data
        if result is None: # delete error
            message = "El registro no se puede borrar" # Error messate
            id_evento = config.check_secure_val(str(id_evento))  # HMAC user validate
            id_evento = config.check_secure_val(str(id_evento))  # HMAC user validate
            result = config.model.get_clientes(int(id_evento)) # get id_cliente data
            result.id_evento = config.make_secure_val(str(result.id_evento)) # apply HMAC to id_cliente
            return config.render.delete(result, message) # render delete.html again
        else:
            raise config.web.seeother('/clientes') # render clientes delete.html 
