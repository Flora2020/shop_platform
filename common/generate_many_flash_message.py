from typing import List
from flask import flash


def generate_many_flash_message(messages: List[str], category: str) -> None:
    for msg in messages:
        flash(msg, category)
