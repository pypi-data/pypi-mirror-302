# Autotasker
AutoTasker is a console application designed to simplify and automate repetitive tasks without the need for programming skills.
## Docker
#### Create containers and images with a single command

The `autotasker` command allows you to create Docker containers and images with just one simple command.

#### Usage:
```bash
autotasker [OPTIONS] PATH
```

#### Parameters: 
- **PATH:** The path to the Docker project or directory you want to build

  - Example:
    ```bash 
    autotasker ./my-docker-project
    ``` 

#### Options: 
- ```--only-image```: Use this option to only create the Docker image without creating a container.

  - Example:
    ```bash 
    autotasker --only-image ./my-docker-project
    ``` 
#### Suported Frameworks
This tool supports projects built with:
- Django
- React
- Vite