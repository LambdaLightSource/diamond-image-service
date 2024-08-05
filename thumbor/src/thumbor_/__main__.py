import argparse
import asyncio

from thumbor.src.thumbor_.server import main as server_main
from thumbor.src.thumbor_.storage_manager import StorageManager


async def manage_storage(delete_old=False):
    manager = StorageManager()
    if delete_old:
        await manager.list_and_delete_old_objects()


def main():
    parser = argparse.ArgumentParser(
        description="Thumbor CLI for managing server and storage"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    server_parser = subparsers.add_parser("server", help="Start the Thumbor server")
    server_parser.add_argument("--serve", action="store_true", help="Start the server")

    storage_parser = subparsers.add_parser(
        "storage", help="Delete expired objects from the bucket"
    )
    storage_parser.add_argument(
        "--delete-expired",
        action="store_true",
        help="Delete expired objects from the bucket",
    )

    args = parser.parse_args()

    if args.command == "server" and args.serve:
        server_main()
    elif args.command == "storage" and args.delete_expired:
        asyncio.run(manage_storage(delete_old=True))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
