#!/usr/bin/env python
from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import set_title
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.sql import SqlLexer
import re
import tabulate
import mysql.connector
import csv

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
    ).strip()
    if answer.lower() == "view":
        answer = prompt(
            "Do you want to do a Query or view a Table or Export? (Query/Table/Export) ",
            completer=WordCompleter(
                ["Query", "Table", "Export", "query", "table", "export"]
            ),
        ).strip()
        if answer.lower() == "table":
            cursor.execute("SELECT * from report")
            print(
                tabulate.tabulate(cursor, headers=[i[0] for i in cursor.description],)
            )
            cursor.execute(" SELECT sum(hours_spent) from report;")
            print("\nTotal Hours Taken: ", cursor.fetchone()[0])
        elif answer.lower() == "query":
            cat_sql = prompt(
                "Do you want to do an SQL Query or Category Query? (SQL/Category) ",
                completer=WordCompleter(["SQL", "Category", "sql", "category"]),
            )
            if cat_sql.lower() == "category":
                cursor.execute("SELECT DISTINCT(category) from report;")
                categories = [cat[0] for cat in cursor.fetchall()]
                print(
                    tabulate.tabulate(
                        [[cat] for cat in categories], headers=["Category Name"]
                    )
                )
                category = prompt(
                    "\nWhich category do you want to view? ",
                    completer=WordCompleter(categories),
                    validator=Validator.from_callable(
                        lambda x: x in categories,
                        error_message="Not a valid category",
                        move_cursor_to_end=True,
                    ),
                ).strip()
                cursor.execute('SELECT * FROM report WHERE category="%s";' % category)
                print(
                    tabulate.tabulate(
                        cursor, headers=[i[0] for i in cursor.description],
                    )
                )
            elif cat_sql.lower() == "sql":
                cursor.execute(prompt("> ", lexer=PygmentsLexer(SqlLexer)))
                print(
                    tabulate.tabulate(
                        cursor, headers=[i[0] for i in cursor.description],
                    )
                )

        elif answer.lower() == "export":
            fmt = prompt(
                "What format do you want to use? (CSV) ",
                completer=WordCompleter(["CSV", "csv"]),
                validator=Validator.from_callable(
                    lambda x: x in ["CSV", "csv"],
                    error_message="Not a valid format",
                    move_cursor_to_end=True,
                ),
            )
            if fmt.lower() == "csv":
                print_formatted_text(
                    HTML(
                        "<ansired>WARNING: CSV'S DO NOT HAVE MULTI-LINE SUPPORT</ansired>"
                    )
                )
                cursor.execute("SELECT * FROM report")
                with open("export.csv", mode="w", newline="") as export_csv:
                    csv_writer = csv.writer(
                        export_csv,
                        delimiter=",",
                        quotechar='"',
                        quoting=csv.QUOTE_MINIMAL,
                    )
                    csv_writer.writerow([i[0] for i in cursor.description])
                    for row in cursor:
                        csv_writer.writerow(row)

                print_formatted_text(HTML("<green>Exported CSV Successfully</green>"))

    elif answer.lower() == "add":
        date = prompt(
            HTML("<when>When</when> did you complete this learning (DD/MM/YYYY)? "),
            validator=Validator.from_callable(
                lambda x: re.search(r"\d{2}/\d{2}/\d{4}", x),
                error_message="Not a valid date (Must be in the form DD/MM/YYYY).",
                move_cursor_to_end=True,
            ),
        ).strip()
        activity = prompt("Activity: ")
        brief_description = prompt(
            HTML(
                "Brief Description: (ESCAPE followed by ENTER to accept)\n <green>&#62;</green> "
            ),
            multiline=True,
            style=Style.from_dict({"green": "#00FF00 underline"}),
        ).strip()
        value_obtained = prompt(
            HTML(
                "Value Obtained: (ESCAPE followed by ENTER to accept)\n <green>&#62;</green> "
            ),
            multiline=True,
            style=Style.from_dict({"green": "#00FF00 underline"}),
        ).strip()
        hours_spent = prompt(
            HTML("<how>How</how> many hours did you spend (flt)? "),
            validator=Validator.from_callable(
                lambda x: re.search(r"\d+(?:\.)?", x),
                error_message="Not a valid number (Must be a float or integer).",
                move_cursor_to_end=True,
            ),
        ).strip()
        category = prompt(
            HTML("Category: <green>(OPTIONAL)</green> "),
            style=Style.from_dict({"green": "#00FF00 underline"}),
        ).strip()

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
