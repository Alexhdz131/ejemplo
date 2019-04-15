import web
import config
import json


class Api_clientes:
    def get(self, id_evento):
        try:
            # http://localhost:8080/api_clientes?user_hash=12345&action=get
            if id_evento is None:
                result = config.model.get_all_clientes()
                clientes_json = []
                for row in result:
                    tmp = dict(row)
                    clientes_json.append(tmp)
                web.header('Content-Type', 'application/json')
                return json.dumps(clientes_json)
            else:
                # http://localhost:8080/api_clientes?user_hash=12345&action=get&id_cliente=1
                result = config.model.get_clientes(int(id_evento))
                clientes_json = []
                clientes_json.append(dict(result))
                web.header('Content-Type', 'application/json')
                return json.dumps(clientes_json)
        except Exception as e:
            print "GET Error {}".format(e.args)
            clientes_json = '[]'
            web.header('Content-Type', 'application/json')
            return json.dumps(clientes_json)

# http://localhost:8080/api_clientes?user_hash=12345&action=put&id_cliente=1&product=nuevo&description=nueva&stock=10&purchase_price=1&price_sale=3&product_image=0
    def put(self, titulo, description, fecha, hora, ubicacion ):
        try:
            config.model.insert_evento(titulo, description, fecha, hora, ubicacion)
            clientes_json = '[{200}]'
            web.header('Content-Type', 'application/json')
            return json.dumps(clientes_json)
        except Exception as e:
            print "PUT Error {}".format(e.args)
            return None

# http://localhost:8080/api_clientes?user_hash=12345&action=delete&id_cliente=1
    def delete(self, id_evento):
        try:
            config.model.delete_evento(id_evento)
            clientes_json = '[{200}]'
            web.header('Content-Type', 'application/json')
            return json.dumps(clientes_json)
        except Exception as e:
            print "DELETE Error {}".format(e.args)
            return None

# http://localhost:8080/api_clientes?user_hash=12345&action=update&id_cliente=1&product=nuevo&description=nueva&stock=10&purchase_price=1&price_sale=3&product_image=default.jpg
    def update(self, id_evento, titulo, description, fecha, hora, ubicacion):
        try:
            config.model.edit_evento(id_evento,titulo,description,fecha,hora,ubicacion)
            clientes_json = '[{200}]'
            web.header('Content-Type', 'application/json')
            return json.dumps(clientes_json)
        except Exception as e:
            print "GET Error {}".format(e.args)
            clientes_json = '[]'
            web.header('Content-Type', 'application/json')
            return json.dumps(clientes_json)

    def GET(self):
        user_data = web.input(
            user_hash=None,
            action=None,
            id_evento=None,
            titulo=None,
            description=None,
            fecha=None,
            hora=None,
            ubicacion=None,
        )
        try:
            user_hash = user_data.user_hash  # user validation
            action = user_data.action  # action GET, PUT, DELETE, UPDATE
            id_evento=user_data.id_evento

            titulo=user_data.titulo

            description=user_data.description

            fecha=user_data.fecha

            hora=user_data.hora

            ubicacion=user_data.ubicacion

            # user_hash
            if user_hash == '12345':
                if action is None:
                    raise web.seeother('/404')
                elif action == 'get':
                    return self.get(id_evento)
                elif action == 'put':
                    return self.put(titulo,description,fecha,hora,ubicacion)
                elif action == 'delete':
                    return self.delete(id_evento)
                elif action == 'update':
                    return self.update(id_evento,titulo,description,fecha,hora,ubicacion)
            else:
                raise web.seeother('/404')
        except Exception as e:
            print "WEBSERVICE Error {}".format(e.args)
            raise web.seeother('/404')
