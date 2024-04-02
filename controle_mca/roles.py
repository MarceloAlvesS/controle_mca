from rolepermissions.roles import AbstractUserRole

class Contabil(AbstractUserRole):
    available_permissions = {
    }

class Administrador(AbstractUserRole):
    available_permissions = {
        'ver_si_proprio': True,
        'ver_funcionarios': True,
        'ver_area_administrativa': True
    }