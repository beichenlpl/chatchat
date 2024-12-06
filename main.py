import sys
from cli import chat_in_cli
from api import start_api

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        chat_in_cli()
    elif len(sys.argv) > 1 and sys.argv[1] == "api":
        start_api()
    else:
        chat_in_cli()