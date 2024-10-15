__all__ = ["id_uint"]

from typing import Annotated

id_uint = Annotated[int, "id为大于0的整数"]