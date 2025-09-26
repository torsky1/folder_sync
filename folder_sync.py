import sys
import os
import time
import logging
import shutil


# --------------------Logging--------------------
def set_up_logger(log_path: str):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_path, encoding="utf-8"),
        ],
    )
    return logging.getLogger("folder_sync")


# --------------------Helpers--------------------
def create_file_or_update(src_path: str, rep_path: str, logger: logging.Logger) -> None:
    os.makedirs(os.path.dirname(rep_path), exist_ok=True)
    shutil.copy2(src_path, rep_path)
    logger.info(f"File was copied/updated: {rep_path}")


def remove_folder(path: str, logger: logging.Logger) -> None:
    if not os.path.exists(path):
        return
    if os.path.isfile(path):
        os.remove(path)
        logger.info(f"File was removed: {path}")
        return
    try:
        for name in sorted(os.listdir(path)):
            child = os.path.join(path, name)
            if os.path.isdir(child) and not os.path.islink(child):
                remove_folder(child, logger)
            else:
                os.remove(child)
                logger.info(f"File was removed: {child}")
        os.rmdir(path)
        logger.info(f"Directory was removed: {path}")
    except FileNotFoundError:
        pass


# --------------------Core--------------------
def copy_folder(source_path: str, replica_path: str, logger: logging.Logger) -> None:
    for name in sorted(os.listdir(source_path)):
        src = os.path.join(source_path, name)
        rep = os.path.join(replica_path, name)

        if os.path.isdir(src) and not os.path.islink(src):
            os.makedirs(rep, exist_ok=True)
            copy_folder(src, rep, logger)

        elif os.path.isfile(src) and not os.path.islink(src):
            rep_is_file = os.path.isfile(rep) and not os.path.islink(rep)
            if not rep_is_file:
                create_file_or_update(src, rep, logger)
            else:
                src_st = os.stat(src)
                rep_st = os.stat(rep)

                if (src_st.st_size != rep_st.st_size) or (
                    src_st.st_mtime != rep_st.st_mtime
                ):
                    create_file_or_update(src, rep, logger)


def delete(source_path: str, replica_path: str, logger: logging.Logger) -> None:
    if not os.path.exists(replica_path):
        return

    for name in sorted(os.listdir(replica_path)):
        src = os.path.join(source_path, name)
        rep = os.path.join(replica_path, name)

        if not os.path.exists(src):
            if os.path.isdir(rep) and not os.path.islink(rep):
                remove_folder(rep, logger)
            else:
                try:
                    os.remove(rep)
                    logger.info(f"File was removed: {rep}")
                except FileNotFoundError:
                    pass
        else:
            if os.path.isdir(src) and os.path.isdir(rep) and not os.path.islink(rep):
                delete(src, rep, logger)
            elif os.path.isdir(rep) != os.path.isdir(src):
                if os.path.isdir(rep) and not os.path.islink(rep):
                    remove_folder(rep, logger)
                else:
                    try:
                        os.remove(rep)
                        logger.info(f"File was removed cause - type mismatch: {rep}")
                    except FileNotFoundError:
                        pass


# --------------------Scheduler--------------------
def schedule(
    source_path: str,
    replica_path: str,
    sync_interval: int,
    sync_amount: int,
    logger: logging.Logger,
):
    for i in range(sync_amount):
        logger.info(f"*SYNC START* - {i + 1}/{sync_amount}")
        try:
            copy_folder(source_path, replica_path, logger)
            delete(source_path, replica_path, logger)
        except Exception as e:
            logger.error(f"Sync error: {e}")
        logger.info(f"*SYNC DONE* - {i + 1}/{sync_amount}")

        if i < sync_amount - 1:
            try:
                time.sleep(sync_interval)
            except Exception as e:
                logger.error(f"Sleep error: {e}")


# --------------------Entry--------------------
def main():
    if len(sys.argv) != 6:
        print(
            "Expected arguments: <source_folder_path> <replica_folder_path> <interval_between_sync> <amount_of_sync> <log_path>"
        )
        return
    source_path = sys.argv[1]
    replica_path = sys.argv[2]
    try:
        sync_interval = int(sys.argv[3])
        sync_amount = int(sys.argv[4])
    except ValueError:
        print("Sync interval and sync amount must be integers")
        return

    log_path = sys.argv[5]

    if not os.path.exists(source_path) or not os.path.isdir(source_path):
        print(f"Source must be an existing directory: {source_path}")
        return

    if sync_interval < 0:
        print("interval between synchronizations must be >= 0")
        return

    if sync_amount < 1:
        print("Amount of synchronizations must be >= 1")
        return

    logger = set_up_logger(log_path)

    schedule(source_path, replica_path, sync_interval, sync_amount, logger)


if __name__ == "__main__":
    main()
