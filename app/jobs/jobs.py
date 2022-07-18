import logging
import os
import subprocess
import sys

logger = logging.getLogger(__name__)


def create_migration():
    try:
        alembic_dir = "./alembics/versions"
        current_files = sorted(os.listdir(alembic_dir), reverse=True)
        prefix = "_0001_"
        for filename in current_files:
            if filename[0] == "_" \
                    and filename[5] == "_" \
                    and filename[1:5].isnumeric() \
                    and os.path.splitext(filename)[1] == ".py":
                prefix = "_{0:04d}_".format(int(filename[1:5]) + 1)
                break
        if not sys.argv[1:]:
            message = "new migration"
        else:
            message = sys.argv[1:][0]

        subprocess.run([
            "alembic",
            "revision",
            "--autogenerate",
            "-m",
            f"'{message}'"
        ])

        for filename in os.listdir(alembic_dir):
            if filename not in current_files:
                if "__pycache__" not in filename:
                    os.rename(os.path.join(alembic_dir, filename),
                              os.path.join(alembic_dir, f"{prefix}{filename}"))
                    break
    except Exception as e:
        logger.error(e)

def upgrade_migration():
    try:
        if not sys.argv[1:]:
            revision = "head"
        else:
            revision = sys.argv[1:][0]
        subprocess.run([
            "alembic",
            "upgrade",
            revision
        ])
    except Exception as e:
        logger.error(e)


def downgrade_migration():
    try:
        if not sys.argv[1:]:
            revision = "base"
        else:
            revision = sys.argv[1:][0]
        subprocess.run([
            "alembic",
            "downgrade",
            revision
        ])
    except Exception as e:
        logger.error(e)