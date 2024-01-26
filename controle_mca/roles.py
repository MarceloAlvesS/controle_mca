from rolepermissions.roles import AbstractUserRole

class Funcionario(AbstractUserRole):
    available_permissions = {

    }

class Adimistrador(AbstractUserRole):
    available_permissions = {
        'ver_funcionarios': True,
    }