#!/usr/bin/env python
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import set_title
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator
import re


if __name__ == "__main__":
    set_title("CPD Manager")

    answer = prompt(
        HTML("Would you like to <view>View</view> or <add>Add</add> to your CPD? "),
        completer=WordCompleter(["View", "Add"]),
        style=Style.from_dict(
            {"view": "#0000FF underline", "add": "#00FF00 underline",}
        ),
    )
    if answer.lower() == "view":
        pass

    elif answer.lower() == "add":
        prompt(
            HTML("<when>When</when> did you complete this learning (DD/MM/YYYY)? "),
            validator=Validator.from_callable(
                lambda x: re.search(r"\d{2}/\d{2}/\d{4}", x),
                error_message="Not a valid date (Must be in the form DD/MM/YYYY).",
                move_cursor_to_end=True,
            ),
        )

