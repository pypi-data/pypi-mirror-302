import click
from autotasker.managers.docker_manager import DockerManager



@click.group()
def cli():
    """Comando principal de la CLI."""
    pass


@cli.command()
@click.argument('path')
@click.option('--only-image', is_flag=True, default=False, help='Creates only the image, without starting the container.')
def docker(path, only_image):
    """Crea un contenedor de docker"""

    click.echo(click.style(" Select the programming language:", bold=True, fg='cyan'))
    languages = ['Django', 'Vite', 'React']

    for i, lang in enumerate(languages, start=1):
        click.echo(click.style(f'  {i}. {lang}', fg='yellow'))
    lang_choice = click.prompt(click.style("", fg='green'), type=int)
    if lang_choice < 1 or lang_choice > len(languages):
        click.echo(click.style(" Error: Invalid choice. Please try again.", fg='red'))
        return

    selected_lang = languages[lang_choice - 1]
    image_name = click.prompt(click.style(' Enter the name of the Docker image:', fg='green'))
    container_name = click.prompt(click.style(' Enter the name of the Docker container:', fg='green'))
    port = click.prompt(click.style(' Enter the port number:', fg='green'), type=int)

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
