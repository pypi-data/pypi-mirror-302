import os
import shutil
import click, pathlib

@click.group()
def main():
    pass

@main.command()
@click.argument('destination', type=click.Path())
def init(destination):
    """Initialize boilerplate files for custom implementation."""
    source_dir = pathlib.Path(__file__).parent / 'boilerplate'

    configFilePath = source_dir / 'config.json'
    implementationDirPath = source_dir / 'implementation'


    destinationDir = pathlib.Path(os.getcwd())

    if not os.path.exists(str(destinationDir)):
        os.makedirs(str(destinationDir), exist_ok=True)

    
    shutil.copy(str(configFilePath), str(destinationDir / 'config.json'))
    shutil.copytree(implementationDirPath, os.path.join(os.getcwd(), 'implementation'))
    print(f"Boilerplate created at {destination}/implementation")

if __name__ == '__main__':
    main()
