def show_menu():
    """
    Muestra un menú interactivo para que el usuario elija el tipo de scan.
    """
    print("Seleccione el tipo de reconocimiento que desea realizar:")
    print("1. Internal Recon")
    print("2. External Recon")
    print("3. HTTP")
    print("4. Custom")
    print("5. Exit")

    # Solicitar al usuario que seleccione un perfil
    choice = input("Ingrese el número correspondiente a su elección: ")

    profiles = {
        '1': 'Internal Recon',
        '2': 'External Recon',
        '3': 'HTTP',
        '4': 'Custom',
        '5': 'Exit'
    }

    # Validar la opción y retornar el perfil seleccionado
    return profiles.get(choice, None)