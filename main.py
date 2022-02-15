#!/usr/bin/env python
from email import header
from more_itertools import first
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import set_title
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator
import re
import tabulate
import mysql.connector

if __name__ == "__main__":
    set_title("CPD Manager")

    # Setup MySQL
    user = prompt("User: ")
    passwd = prompt("Password: ", is_password=True)

    cnx = mysql.connector.connect(
        user=user, password=passwd, host="127.0.0.1", database="cpd"
    )
    cursor = cnx.cursor()

    # Main
    answer = prompt(
        HTML("Would you like to <view>View</view> or <add>Add</add> to your CPD? "),
        completer=WordCompleter(["View", "Add", "view", "add"]),
        style=Style.from_dict(
            {"view": "#0000FF underline", "add": "#00FF00 underline",}
        ),
    )
    if answer.lower() == "view":
        answer = prompt(
            "Do you want to do a Query or view a Table? (Query/Table) ",
            completer=WordCompleter(["Query", "Table", "query", "table"]),
        )
        if answer.lower() == "table":
            cursor.execute("SELECT * from report")
            print(
                tabulate.tabulate(
                    cursor,
                    headers=[
                        "id",
                        "date",
                        "activity",
                        "brief_description",
                        "values_obtained",
                        "hours_spent",
                        "category",
                    ],
                )
            )
            cursor.execute(" SELECT sum(hours_spent) from report;")
            print("Total Hours Taken: ", cursor.fetchone()[0])
        elif answer.lower() == "query":
            cat_sql = prompt(
                "Do you want to do an SQL Query or Category Query? (SQL/Category) ",
                completer=WordCompleter(["SQL", "Category", "sql", "category"]),
            )
            if cat_sql.lower() == "category":
                cursor.execute("SELECT DISTINCT(category) from report;")
                cat_sql = prompt(
                    "Which category do you want to view? ",
                    completer=WordCompleter([cat for cat in cursor.fetchall()[0]]),
                )

    elif answer.lower() == "add":
        date = prompt(
            HTML("<when>When</when> did you complete this learning (DD/MM/YYYY)? "),
            validator=Validator.from_callable(
                lambda x: re.search(r"\d{2}/\d{2}/\d{4}", x),
                error_message="Not a valid date (Must be in the form DD/MM/YYYY).",
                move_cursor_to_end=True,
            ),
        )
        activity = prompt("Activity: ")
        brief_description = prompt(
            HTML(
                "Brief Description: (ESCAPE followed by ENTER to accept)\n <green>&#62;</green> "
            ),
            multiline=True,
            style=Style.from_dict({"green": "#00FF00 underline"}),
        )
        value_obtained = prompt(
            HTML(
                "Value Obtained: (ESCAPE followed by ENTER to accept)\n <green>&#62;</green> "
            ),
            multiline=True,
            style=Style.from_dict({"green": "#00FF00 underline"}),
        )
        hours_spent = prompt(
            HTML("<how>How</how> many hours did you spend (flt)? "),
            validator=Validator.from_callable(
                lambda x: re.search(r"\d+(?:\.)?", x),
                error_message="Not a valid number (Must be a float or integer).",
                move_cursor_to_end=True,
            ),
        )
        category = prompt(
            HTML("Category: <green>(OPTIONAL)</green> "),
            style=Style.from_dict({"green": "#00FF00 underline"}),
        )

        add_entry = (
            "INSERT INTO report "
            "(date, activity, brief_description, values_obtained, hours_spent, category) "
            "VALUES (%(date)s, %(activity)s, %(brief_description)s, %(value_obtained)s, %(hours_spent)s, %(category)s)"
        )
        data = {
            "date": date[-4:] + "-" + date[3:-5] + "-" + date[:2],
            "activity": activity,
            "brief_description": brief_description,
            "value_obtained": value_obtained,
            "hours_spent": hours_spent,
            "category": category,
        }
        cursor.execute(add_entry, data)
        cnx.commit()

    cursor.close()
    cnx.close()
