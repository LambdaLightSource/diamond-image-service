import asyncio
import sys
from argparse import ArgumentParser

from thumbor_.server import main as server_main
from thumbor_.storage_manager import StorageManager


async def manage_storage(delete_old=False):
    manager = StorageManager()
    if delete_old:
        await manager.list_and_delete_old_objects()


def main():
    parser = ArgumentParser(description="Thumbor CLI for managing server and storage")
    parser.add_argument("--serve", action="store_true", help="Start the Thumbor server")
    parser.add_argument(
        "--delete-expired",
        action="store_true",
        help="Delete expired objects from the bucket",
    )

    args, unknown = parser.parse_known_args()

    if args.serve:
        sys.argv[1:] = unknown
        server_main()
    elif args.delete_expired:
        asyncio.run(manage_storage(delete_old=True))


if __name__ == "__main__":
    main()
