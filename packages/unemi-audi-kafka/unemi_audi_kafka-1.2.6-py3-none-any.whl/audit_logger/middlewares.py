import threading
from django.utils.deprecation import MiddlewareMixin

# Variables de thread-local para almacenar la request y sus atributos
_thread_locals = threading.local()

def get_current_request():
    """
    Devuelve la request almacenada en el middleware.
    """
    return getattr(_thread_locals, 'request', None)

def set_current_request(request):
    """
        Modifica la request almacenada en el middleware.
    """
    return setattr(_thread_locals, 'request', request)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AuditUserMiddleware(MiddlewareMixin):
    """
    Middleware combinado para capturar el usuario, la request, la URL, la IP y el dispositivo (user-agent).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_request(request)

        response = self.get_response(request)
        return response

    @staticmethod
    def get_current_user():
        """
        Devuelve el usuario actual de la solicitud.
        """
        request = get_current_request()
        user_id = getattr(request, 'user_id', None)
        if user_id:
            return user_id
        user = getattr(request, 'user', None)
        if user:
            user_id = getattr(user, 'id', None)
            return user_id
        return None

    @staticmethod
    def get_previous_user():
        """
        Devuelve el usuario anterior almacenado en la sesión.
        """
        request = get_current_request()
        if request:
            previous_user = request.session.get('user_anterior', None)
            if previous_user:
                # Si es un objeto User, devuelve su id
                if hasattr(previous_user, 'id'):
                    return previous_user.id
                # Si es un ID (entero), lo devuelve tal cual
                elif isinstance(previous_user, int):
                    return previous_user
        return None

    @staticmethod
    def get_current_ip():
        """
        Devuelve la IP del cliente.
        """
        request = get_current_request()
        decoded_token = getattr(request, 'decoded_token', None)
        if decoded_token:
            datasession = decoded_token['dataUserSession']
            if datasession:
                ip = datasession['ip'] if datasession['ip'] else None
                return ip
            return None
        ip = request.session.get('capippriva', None)
        if ip:
            return ip
        remote_ip = get_client_ip(request)
        return remote_ip if remote_ip else None

    @staticmethod
    def get_user_agent():
        """
        Devuelve el User-Agent del cliente.
        """
        request = get_current_request()
        if request:
            return request.META.get('HTTP_USER_AGENT')
        return None

    @staticmethod
    def get_current_url():
        """
        Devuelve la URL completa de la solicitud actual.
        """
        request = get_current_request()
        if request:
            return request.path
        return None