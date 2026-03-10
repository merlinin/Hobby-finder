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
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict) or not isinstance(payload.get("activity"), str):
            return jsonify({"error": "Payload must contain string field 'activity'."}), 400

        activity = payload["activity"].strip()
        if not activity:
            return jsonify({"error": "Field 'activity' must not be empty."}), 400

        result = orchestrator.qualify_activity(QualificationInput(activity=activity))
        return jsonify(result)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
