from datetime import datetime
from random import randint

from faker import Faker

from app.redis import get_client
from app.schema import Log, StreamObject
from app.settings import env

fake = Faker()
key_prefix = "log"


def mangle_key(key: str) -> str:
    return f"{key_prefix}:{key}"


async def generate_log(service: str, count: int | None = None):
    aredis = get_client()
    await aredis.initialize()
    if not count:
        limit = randint(10, 20)
    else:
        limit = count

    KEY = mangle_key(service)
    # add key to set to know which keys to trim
    await aredis.sadd("logs", KEY)
    for _ in range(limit):
        await aredis.xadd(
            KEY,
            Log(
                message=fake.text().strip(),
                datetime=datetime.now().isoformat(),
                service=service,
            ).dict(),
            maxlen=env.stream_max_length,
        )
    await aredis.close()


async def retrieve_log(
    service: str,
    last_id: str,
    count: int
) -> tuple[list[StreamObject], str]:
    aredis = get_client()
    await aredis.initialize()

    # check if key exists
    KEY = mangle_key(service)
    key_exists = await aredis.exists(KEY)
    if not key_exists:
        return ([], None)

    # get logs from newest to oldest but only return the last {count} logs
    logs = await aredis.xrange(KEY, min=last_id, count=count)
    if not logs:
        return ([], None)
    logs = [
        StreamObject(
            id_=log[0],
            log=Log(**log[1]),
        )
        for log in logs
    ]
    await aredis.close()
    return (logs, logs[-1].id_)


async def retrieve_log_as_string(
    service: str,
    last_id: str,
    count: int
) -> tuple[str, str]:
    logs, last_id = await retrieve_log(service, last_id, count)
    logs = [
        f"{log.log.datetime} - {log.log.service} - {log.log.message}"
        for log in logs
    ]
    return ("\n".join(logs), last_id)
