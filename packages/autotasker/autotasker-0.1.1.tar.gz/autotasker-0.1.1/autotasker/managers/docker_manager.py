import click
import subprocess
from autotasker.utils.dockerfile_templates import get_dockerfile_template
import os


class DockerManager:
    """
        A class to manage Docker container creation and management.

        Attributes:
            image (str): The name of the Docker image.
            container (str): The name of the Docker container.
            port (int): The port on which the container will run.
            dockerfile_path (str): The directory where the Dockerfile will be created.
            language (str): The programming language used for the Docker container.
    """

    def __init__(self, dockerfile_path: str, language: str, image: str, port: int = 8000, container: str = None):
        """
        Initializes the DockerManager with an image name, an optional container name, and a port.

        Args:
            dockerfile_path (str): The directory where the Dockerfile will be created.
            image (str): The name of the Docker image to be used.
            container (str, optional): The name for the Docker container. Defaults to "default_container".
            port (int, optional): The port on which the container will run. Defaults to 8000.
            language (str): The programming language for the Docker container
        """
        self.dockerfile_path = os.path.normpath(dockerfile_path)
        self.image = image
        self.port = port
        self.container = container
        self.language = language

    def create_dockerfile(self):
        """This function is used to create the Dockerfile based on the provided data."""
        click.echo("   • Dockerfile: creating...", nl=False)
        if not os.path.exists(self.dockerfile_path):
            click.echo(click.style(f'Error: The file "{self.dockerfile_path}" does not exist.', fg='red'))
            raise click.Abort()

        template = get_dockerfile_template(self.language, self.port)

        full_dockerfile_path = os.path.join(self.dockerfile_path, "dockerfile")
        with open(full_dockerfile_path, "w") as f:
            f.write(template)

        click.echo("\r   • Dockerfile: " + click.style("created    ", fg="green"))

    def create_image(self):
        """This function will create the Docker image using the provided data."""
        click.echo("   • Docker Image: creating...", nl=False)
        try:
            command = ["docker", "build", "-t", self.image, self.dockerfile_path]

            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                click.echo("\r   • Docker Image: " + click.style("created    ", fg="green"))
            else:
                click.echo(click.style(f'\nError: {result.stderr}', fg='red'))
                raise click.Abort()
        except Exception as e:
            raise click.Abort()

    def create_container(self):
        """This function will create the container from the previous image."""
        click.echo("   • Docker Container: creating...", nl=False)
        try:
            command = ["docker", "run", "-d", "-p", f"{self.port}:{self.port}", "--name", self.container,
                       self.image]

            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                click.echo("\r   • Docker Container: " + click.style("created    ", fg="green"))
            else:
                click.echo(click.style(f'\nError: {result.stderr}', fg='red'))
                raise click.Abort()
        except Exception as e:
            remove_image = ["docker", "rm", self.container]
            remove_container = ["docker", "image", "rm", self.image]
            click.echo(click.style("Deleting container and image...", fg='red'),nl=False)
            result = subprocess.run(remove_container, capture_output=True, text=True)
            result = subprocess.run(remove_image, capture_output=True, text=True)
            click.echo("\rDeleted                " + click.style("created", fg="red"))
            raise click.Abort()
