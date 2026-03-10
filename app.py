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

from flask import Flask, request, jsonify, render_template

from app.orchestration import AppOrchestrator
from models import db, Hobby, Attribute, HobbyAttribute, seed_data


def create_app() -> Flask:
    """Factory to create and configure the Flask application instance."""
    app = Flask(__name__)
    # Configure the database URI. SQLite database stored locally.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hobbies.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Create tables and seed data during app initialization.
    with app.app_context():
        db.create_all()
        seed_data()

    orchestrator = AppOrchestrator()

    @app.route("/hobbies", methods=["GET"])
    def get_hobbies():
        """Return a list of hobbies, optionally filtered by search or attribute.

        Query parameters:
        ``q`` - free‑text search for hobby names.
        ``attribute`` - name of an attribute to filter by (must match
        an existing attribute name).
        """
        search_text = request.args.get("q", type=str) or ""
        attribute_filter = request.args.get("attribute", type=str)

        # Build base query
        query = Hobby.query
        if search_text:
            # Case‑insensitive search on hobby name
            query = query.filter(Hobby.name.ilike(f"%{search_text}%"))
        hobbies = query.all()

        # Assemble result structure
        results = []
        for hobby in hobbies:
            # Convert each hobby to a dictionary including its attributes
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

        # If an attribute filter is given, filter results to only include
        # hobbies that have at least one attribute matching the filter.
        if attribute_filter:
            results = [
                hobby
                for hobby in results
                if any(attr["name"].lower() == attribute_filter.lower() for attr in hobby["attributes"])
            ]

        return jsonify(results)

    @app.route("/", methods=["GET"])
    def index():
        """Render a simple landing page for end users."""
        return render_template("index.html", **orchestrator.get_index_context())

    @app.route("/wordcloud.png", methods=["GET"])
    def wordcloud_png():
        """Generate and return the hobby definitions word cloud as PNG."""
        image = orchestrator.generate_wordcloud_image()
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return app.response_class(buffer.getvalue(), mimetype="image/png")

    @app.route("/attributes", methods=["GET"])
    def list_attributes():
        """Return a list of all defined attributes with descriptions."""
        attrs = Attribute.query.order_by(Attribute.name).all()
        return jsonify([
            {
                "id": attr.id,
                "name": attr.name,
                "description": attr.description,
                "scale_type": attr.scale_type,
            }
            for attr in attrs
        ])

    return app


if __name__ == "__main__":
    # Only run the server if this script is executed directly.
    app = create_app()
    # Run the development server with debug mode enabled for hot reloading.
    app.run(debug=True)
