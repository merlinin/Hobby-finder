"""
Flask application exposing a simple API to explore hobbies and their attributes.

This module defines a small web API that allows users to:

  - Retrieve all hobbies or search for hobbies by name via query parameter ``q``.
  - Filter hobbies by a specific attribute via query parameter ``attribute``.
  - Inspect each hobby's associated attributes and their scores.

The database is initialized on the first request and seeded with a few
sample entries if empty. Data persistence is handled via SQLite.

Run this app with ``python app.py`` and navigate to ``http://localhost:5000/hobbies``
to see the JSON output.
"""

from __future__ import annotations

from io import BytesIO

from flask import Flask, jsonify, render_template, request

from app.contracts import QualificationInput
from app.orchestration import AppOrchestrator
from models import db, seed_data

_ALLOWED_FREQUENCY = {"rarely", "occasionally", "regularly"}
_ALLOWED_IMPORTANCE = {"low", "medium", "high"}


def _parse_qualification_input(payload: object) -> tuple[QualificationInput | None, tuple[dict[str, str], int] | None]:
    if not isinstance(payload, dict) or not isinstance(payload.get("activity"), str):
        return None, ({"error": "Payload must contain string field 'activity'."}, 400)

    activity = payload["activity"].strip()
    if not activity:
        return None, ({"error": "Field 'activity' must not be empty."}, 400)

    for bool_field in ("currently_active", "previously_active", "intends_to_resume"):
        value = payload.get(bool_field)
        if value is not None and not isinstance(value, bool):
            return None, ({"error": f"Field '{bool_field}' must be a boolean when provided."}, 400)

    frequency = payload.get("frequency")
    if frequency is not None:
        if not isinstance(frequency, str) or frequency not in _ALLOWED_FREQUENCY:
            return None, ({"error": "Field 'frequency' must be one of: rarely, occasionally, regularly."}, 400)

    personal_importance = payload.get("personal_importance")
    if personal_importance is not None:
        if not isinstance(personal_importance, str) or personal_importance not in _ALLOWED_IMPORTANCE:
            return None, ({"error": "Field 'personal_importance' must be one of: low, medium, high."}, 400)

    return (
        QualificationInput(
            activity=activity,
            currently_active=payload.get("currently_active"),
            previously_active=payload.get("previously_active"),
            frequency=frequency,
            personal_importance=personal_importance,
            intends_to_resume=payload.get("intends_to_resume"),
        ),
        None,
    )


def create_app() -> Flask:
    """Factory to create and configure the Flask application instance."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hobbies.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_data()

    orchestrator = AppOrchestrator()

    @app.route("/hobbies", methods=["GET"])
    def get_hobbies():
        search_text = request.args.get("q", type=str) or ""
        attribute_filter = request.args.get("attribute", type=str)

        hobbies = orchestrator.list_hobbies(search_text=search_text)

        results = []
        for hobby in hobbies:
            hobby_data = {
                "id": hobby.id,
                "name": hobby.name,
                "category": hobby.category,
                "notes": hobby.notes,
                "attributes": [
                    {
                        "id": ha.attribute.id,
                        "name": ha.attribute.name,
                        "value": ha.value,
                    }
                    for ha in hobby.attributes
                ],
            }
            results.append(hobby_data)

        if attribute_filter:
            results = [
                hobby
                for hobby in results
                if any(attr["name"].lower() == attribute_filter.lower() for attr in hobby["attributes"])
            ]

        return jsonify(results)

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html", **orchestrator.get_index_context())

    @app.route("/wordcloud.png", methods=["GET"])
    def wordcloud_png():
        image = orchestrator.generate_wordcloud_image()
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return app.response_class(buffer.getvalue(), mimetype="image/png")

    @app.route("/attributes", methods=["GET"])
    def list_attributes():
        attrs = orchestrator.list_attributes()
        return jsonify([
            {
                "id": attr.id,
                "name": attr.name,
                "description": attr.description,
                "scale_type": attr.scale_type,
            }
            for attr in attrs
        ])

    @app.route("/qualify", methods=["POST"])
    def qualify_activity():
        parsed, error = _parse_qualification_input(request.get_json(silent=True))
        if error:
            return jsonify(error[0]), error[1]

        result = orchestrator.qualify_activity(parsed)
        return jsonify(result)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
