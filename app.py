import json
import re
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

DATA = Path(app.root_path) / "data"

LABELS = {
    "first_name": "Імʼя",
    "last_name": "Прізвище",
    "age": "Вік",
    "email": "Email",
    "location": "Локація",
    "table": "Номер столику",
}

LIMITS = {
    "first_name": 20,
    "last_name": 40,
    "age": 3,
    "email": 254,
    "location": 20,
    "table": 2,
}

LOCATIONS = ("Uman", "Cherkasy", "Zolotonocha", "Smila")

TABLES = ("1", "2", "3", "4")


@app.template_filter("datetime_utc")
def datetime_utc(value):
    return value.replace("T", " ").replace("+00:00", "")


def validate(values):
    errors = {}

    for field in LABELS:
        value = values.get(field, "")
        if not value:
            errors[field] = "Поле є обовʼязковим."
        elif len(value) > LIMITS[field]:
            errors[field] = f"Дозволено не більше {LIMITS[field]} символів."
        elif any(char in value for char in "\r\n"):
            errors[field] = "Введіть значення одним рядком."

    if "email" not in errors:
        if re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", values["email"]) is None:
            errors["email"] = "Перевірте формат електронної адреси."

    if "age" not in errors:
        if re.fullmatch(r"[0-9]+", values["age"]) is None:
            errors["age"] = "Використовуйте лише цифри."
        elif not 1 <= int(values["age"]) <= 120:
            errors["age"] = "Допустимий вік: від 1 до 120."

    if "location" not in errors and values["location"] not in LOCATIONS:
        errors["location"] = "Виберіть локацію зі списку."

    if "table" not in errors and values["table"] not in TABLES:
        errors["table"] = "Виберіть номер столику зі списку."

    return errors


def save_submission(values):
    DATA.mkdir(parents=True, exist_ok=True)

    created = datetime.now(timezone.utc)
    stamp = created.strftime("%Y-%m-%d_%H-%M-%S_%f")
    filename = f"reservation_{stamp}_{uuid4().hex}.json"

    record = {"created_at": created.isoformat(timespec="seconds"), **values}

    with (DATA / filename).open("x", encoding="utf-8") as output:
        json.dump(record, output, ensure_ascii=False, indent=2)

    return filename


def load_submissions():
    if not DATA.is_dir():
        return []

    records = []
    for path in DATA.glob("*.json"):
        try:
            with path.open(encoding="utf-8") as source:
                record = json.load(source)
        except (OSError, json.JSONDecodeError):
            app.logger.warning("Пропущено пошкоджений файл: %s", path.name)
            continue

        records.append(record)

    records.sort(key=lambda record: record.get("created_at", ""), reverse=True)
    return records


@app.route("/", methods=["GET", "POST"])
def index():
    values = {field: "" for field in LABELS}
    errors = {}

    if request.method == "POST":
        values = {field: request.form.get(field, "").strip() for field in LABELS}
        errors = validate(values)

        if not errors:
            try:
                save_submission(values)
            except OSError:
                app.logger.exception("Не вдалося зберегти відправлення")
                errors["_storage"] = "Не вдалося зберегти дані. Спробуйте пізніше."
            else:
                return redirect(url_for("preorders"), code=303)

        return render_template("index.html", values=values, errors=errors), 422

    return render_template("index.html", values=values, errors=errors), 200


@app.get("/preorders")
def preorders():
    return render_template(
        "preorders.html",
        records=load_submissions(),
        labels=LABELS,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
