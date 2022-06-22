from datetime import datetime, timezone
from uuid import uuid4


uuid = lambda: uuid4()
now = lambda: datetime.now(timezone.utc)

