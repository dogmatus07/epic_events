import os
from dotenv import load_dotenv
import sentry_sdk


def init_sentry():
    load_dotenv()
    sentry_dsn  = os.getenv("SENTRY_DSN")

    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            traces_sample_rate=1.0,
            send_default_pii= True
        )
