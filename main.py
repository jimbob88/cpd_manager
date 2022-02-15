#!/usr/bin/env python
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import set_title
from prompt_toolkit.completion import WordCompleter

style = Style.from_dict(
    {   
        "view": "#0000FF underline",
        "add": "#00FF00 underline",
    }
)

if __name__ == "__main__":
    set_title("CPD Manager")
    view_add = WordCompleter(['View', 'Add'])
    answer = prompt (
        HTML(
            "Would you like to <view>View</view> or <add>Add</add> to your CPD? "
        ),
        completer=view_add,
        style=style
    )
    if answer.lower() == "view":
        pass
    elif answer.lower() == "Add":
        pass
