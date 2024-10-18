import click
from autotasker.managers.docker_manager import DockerManager
from InquirerPy import prompt, inquirer


@click.group()
@click.version_option(version="0.1.1", message=f"autotasker 0.1.1")
def cli():
    """Comando principal de la CLI."""
    pass

import time

@cli.command()
def crear_dockerfile():
    # Muestra el mensaje inicial
    click.echo("Dockerfile: Creating...", nl=False)

    # Simulamos el proceso (puedes reemplazar esto con cualquier operación que estés haciendo)
    time.sleep(3)  # Aquí es donde se ejecutaría tu proceso real (por ejemplo, crear el Dockerfile)

    # Borramos la línea anterior con un retorno de carro (\r) y escribimos el mensaje "Created" en verde
    click.echo("\rDockerfile: " + click.style("Created", fg="green"))
@cli.command()
def select_language():
    """Muestra un menú para seleccionar un lenguaje."""

    # Definimos las opciones del menú
    languages = [
        {"name": "Python", "value": "python"},
        {"name": "JavaScript", "value": "javascript"},
        {"name": "TypeScript", "value": "typescript"},
        {"name": "Rust", "value": "rust"},
        {"name": "Go", "value": "go"},
        {"name": "Salir", "value": "exit"}
    ]

    # Pregunta interactiva usando flechas
    questions = [
        {
            "type": "list",
            "message": "Select an option:",
            "choices": languages,
            "default": "python",
        }
    ]

    # Muestra el menú y obtiene la opción seleccionada
    selected_language = prompt(questions)

    # Dependiendo de la selección, mostramos un mensaje
    language = selected_language.get("Select an option")

    if language == "exit":
        click.echo("Saliendo...")
    else:
        primera_clave = next(iter(selected_language))
        primer_valor = selected_language[0]

        click.echo(f"Primera clave: {primera_clave}, Primer valor: {primer_valor}")


@cli.command()
@click.argument('path')
@click.option('--only-image', is_flag=True, default=False,
              help='Creates only the image, without starting the container.')
def docker(path, only_image):
    """Crea un contenedor de docker"""

    click.echo(click.style(" Select the programming language:", bold=True, fg='cyan'))
    languages = [
        {"name": "Django", "value": "django"},
        {"name": "Vite", "value": "vite"},
        {"name": "React (Vanilla)", "value": "react"},
    ]

    questions = [
        {
            "type": "list",
            "message": "Seleccione un lenguaje:",
            "choices": languages,
            "default": "python",
        }
    ]

    selected_language = prompt(questions)

    selected_lang = selected_language[0]
    image_name = inquirer.text(message="Enter the name of the Docker image:").execute()
    container_name = inquirer.text(message="Enter the name of the Docker container:").execute()
    port = inquirer.text(message="Enter the port number:").execute()

    dockermanager = DockerManager(path, selected_lang, image_name, port, container_name)

    # Create the Dockerfile
    dockermanager.create_dockerfile()

    # Create the Image
    dockermanager.create_image()

    # Creaate Container
    if not only_image:
        dockermanager.create_container()


# Hay que añadir contexto en la database


@cli.group()
def database():
    """Comandos para gestionar bases de datos."""


@database.command()
def importar_info():
    """Importar datos a una base de datos"""
    click.echo("datos importados")


@database.command()
def copias_seguridad():
    """Crea copias de seguridad"""
    click.echo("copia creada")


if __name__ == '__main__':
    cli()
