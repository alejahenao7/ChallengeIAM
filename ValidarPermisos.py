def ConfirmarPermiso(permissions): #permissions es el parámetro de entrada de la API de google Drive
    for permission in permissions:
        if permission['id'] == 'anyoneWithLink':
            print(f"Id: {permission['id']}")
            print(f"Type: {permission['type']}")
            print(f"Kind: {permission['kind']}")
            return "Publico"
    return "Privado"
