# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright (c) 2026 Adityam Ghosh
# SPDX-License-Identifier: MIT
#

from pydantic import BaseModel, HttpUrl


class AddUrlRequest(BaseModel):
    url: HttpUrl
