from app.authentication.domain.controllers.introspect_controller import IntrospectController
from app.authentication.domain.controllers.login_controller import LoginController
from app.authentication.domain.controllers.logout_controller import LogoutController
from app.authentication.domain.controllers.register_controller import RegisterController

# Singletons
_register_controller = None
_login_controller = None
_logout_controller = None
_introspect_controller = None


def get_register_controller():
    global _register_controller
    if _register_controller is None:
        _register_controller = RegisterController()
    return _register_controller


def get_login_controller():
    global _login_controller
    if _login_controller is None:
        _login_controller = LoginController()
    return _login_controller


def get_logout_controller():
    global _logout_controller
    if _logout_controller is None:
        _logout_controller = LogoutController(login_controller=get_login_controller())
    return _logout_controller


def get_introspect_controller():
    global _introspect_controller
    if _introspect_controller is None:
        _introspect_controller = IntrospectController(login_controller=get_login_controller())
    return _introspect_controller
