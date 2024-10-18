from sys import stderr

from click import group
from click import version_option
from loguru import logger

from pd.config.config import config
from pd.conv.conv import conv
from pd.down.down import down
from pd.aws.aws import aws
from pd.edit.edit import edit
from pd.env.env import env
from pd.init.init import init
from pd.nginx.nginx import nginx
from pd.web.web import web
from pd.gen.gen import gen
from pd.version import __version__


@group()
@version_option(__version__, '-v', '--version', help='Show the version and exit')
def cli():
    pass


cli.add_command(config)
cli.add_command(conv)
cli.add_command(down)
cli.add_command(aws)
cli.add_command(edit)
cli.add_command(env)
cli.add_command(gen)
cli.add_command(init)
cli.add_command(nginx)
cli.add_command(web)


def main():
    logger.remove(0)
    logger.add(stderr, level="DEBUG")
    cli()


if __name__ == "__main__":
    main()
