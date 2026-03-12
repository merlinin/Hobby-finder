"""
Database models and seed function for the hobby attribution app.

This module defines three SQLAlchemy models:
  - `Hobby`: represents a leisure activity the user might consider a hobby.
  - `Attribute`: represents a property or dimension by which hobbies can be
    evaluated (e.g. "freiwillig", "Freizeit", "körperlich").
  - `HobbyAttribute`: association table linking hobbies to attributes with
    a numeric score. Higher values indicate stronger relevance of the
    attribute to the hobby.

The `seed_data` function populates the database with a small set of
attributes and sample hobbies derived from the user's brainstorming. The
values assigned in this function are examples and should be adjusted as
needed.
"""

from flask_sqlalchemy import SQLAlchemy

# Create a SQLAlchemy instance but bind it to a Flask app in app.py
db: SQLAlchemy = SQLAlchemy()


class Hobby(db.Model):
    """Model representing a leisure activity or hobby candidate."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255))
    notes = db.Column(db.Text)
    # Use relationship to the association table
    attributes = db.relationship('HobbyAttribute', back_populates='hobby', cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Hobby {self.name}>"


class Attribute(db.Model):
    """Model representing an attribute or dimension relevant to hobbies."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text)
    scale_type = db.Column(db.String(50))  # e.g., 'boolean' or 'scale'
    hobbies = db.relationship('HobbyAttribute', back_populates='attribute', cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Attribute {self.name}>"


class HobbyAttribute(db.Model):
    """Association table linking hobbies to attributes.

    Each entry stores a numeric value representing the strength or degree
    to which a hobby exhibits a given attribute. The scale is arbitrary but
    commonly ranged from 0 (not relevant) to 3 (strongly relevant).
    """

    id = db.Column(db.Integer, primary_key=True)
    hobby_id = db.Column(db.Integer, db.ForeignKey('hobby.id'))
    attribute_id = db.Column(db.Integer, db.ForeignKey('attribute.id'))
    value = db.Column(db.Integer, default=0)

    hobby = db.relationship('Hobby', back_populates='attributes')
    attribute = db.relationship('Attribute', back_populates='hobbies')

    def __repr__(self) -> str:
        return f"<HobbyAttribute hobby={self.hobby_id} attribute={self.attribute_id} value={self.value}>"


def seed_data() -> None:
    """Populate the database with a small set of attributes and sample hobbies.

    This function is idempotent: it checks whether the database already
    contains attributes and hobbies to avoid duplicating entries. You can
    modify or extend this function to suit your own list of hobbies and
    attribute definitions.
    """
    # Only seed if there are no attributes defined
    if not Attribute.query.first():
        # Core attributes derived from common definitions of "Hobby" and
        # extended by user-specific dimensions. Each attribute has a
        # description and indicates whether it is a simple boolean or a
        # graded scale.
        core_attributes = [
            Attribute(
                name="freiwillig",
                description="Die Tätigkeit wird freiwillig ausgeführt, ohne Zwang.",
                scale_type="boolean",
            ),
            Attribute(
                name="Freizeit",
                description="Die Tätigkeit findet hauptsächlich in der Freizeit statt, nicht beruflich.",
                scale_type="boolean",
            ),
            Attribute(
                name="regelmäßig",
                description="Wie regelmäßig die Tätigkeit ausgeübt wird (0–3).",
                scale_type="scale",
            ),
            Attribute(
                name="körperlich",
                description="Grad der körperlichen Aktivität (0–3).",
                scale_type="scale",
            ),
            Attribute(
                name="drinnen",
                description="Wie stark die Tätigkeit indoor stattfindet (0–3).",
                scale_type="scale",
            ),
            Attribute(
                name="kreativ",
                description="Grad der Kreativität, die bei der Tätigkeit gefordert ist (0–3).",
                scale_type="scale",
            ),
        ]
        for attr in core_attributes:
            db.session.add(attr)
        db.session.commit()

    # Ensure sample hobbies exist (idempotent insert by name)
    sample_hobbies = [
        Hobby(name="Klettern", category="Sport", notes="Bouldern und Felsklettern"),
        Hobby(name="3D-Druck", category="Technik", notes="Additive Fertigung"),
        Hobby(name="DJ / Synth", category="Musik", notes="Elektronische Musik und Sampling"),
        Hobby(name="Autos reparieren", category="Technik", notes="Auto reparieren und Tuning"),
        Hobby(name="Programmieren", category="Technik", notes="Softwareentwicklung"),
        Hobby(name="Reiten", category="Sport", notes="Umgang mit Pferden und Ausritte"),
        Hobby(name="Fotografie", category="Kreativ", notes="Fotos aufnehmen und bearbeiten"),
        Hobby(name="Gitarre spielen", category="Musik", notes="Instrument üben und Songs spielen"),
        Hobby(name="Kochen", category="Kreativ", notes="Gerichte planen und zubereiten"),
        Hobby(name="Zeichnen", category="Kreativ", notes="Skizzen, Illustration und Kunst"),
        Hobby(name="Musik machen", category="Musik", notes="Aktives Musizieren mit Instrument oder Stimme"),
        Hobby(name="Modellbau", category="Technik", notes="Modelle bauen und verfeinern"),
        Hobby(name="Gärtnern", category="Natur", notes="Pflanzen pflegen und Garten gestalten"),
        Hobby(name="Radfahren", category="Sport", notes="Freizeitfahrten, Touren und Training"),
        Hobby(name="Schwimmen", category="Sport", notes="Bahnenschwimmen, Technik und Ausdauer"),
        Hobby(name="Yoga", category="Bewegung", notes="Asana-Praxis, Mobilität und Entspannung"),
        Hobby(name="Wandern", category="Outdoor", notes="Tagestouren und Naturerlebnisse"),
        Hobby(name="Malen", category="Kreativ", notes="Aquarell, Acryl und freies Malen"),
        Hobby(name="Klavier spielen", category="Musik", notes="Klavier üben und Stücke spielen"),
        Hobby(name="Elektronik basteln", category="Technik", notes="Löten, Schaltungen und Maker-Projekte"),
        Hobby(name="Briefmarken sammeln", category="Sammeln", notes="Sammeln und Ordnen philatelistischer Stücke"),
        Hobby(name="Vogelbeobachtung", category="Natur", notes="Arten beobachten und dokumentieren"),
    ]
    existing_hobbies = {h.name for h in Hobby.query.all()}
    for hobby in sample_hobbies:
        if hobby.name not in existing_hobbies:
            db.session.add(hobby)
    db.session.commit()

    # Helper to assign attribute values
    def assign(hobby_name: str, attr_name: str, value: int) -> None:
        hobby = Hobby.query.filter_by(name=hobby_name).first()
        attr = Attribute.query.filter_by(name=attr_name).first()
        if hobby and attr:
            existing = HobbyAttribute.query.filter_by(hobby_id=hobby.id, attribute_id=attr.id).first()
            if existing is None:
                db.session.add(HobbyAttribute(hobby_id=hobby.id, attribute_id=attr.id, value=value))

    # Attribute assignments for each hobby. These numbers are example
    # values and can be adjusted based on personal perception.
    assignments = {
        "Klettern": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 1,
            "körperlich": 3,
            "drinnen": 2,
            "kreativ": 1,
        },
        "3D-Druck": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 1,
            "drinnen": 3,
            "kreativ": 2,
        },
        "DJ / Synth": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 1,
            "drinnen": 3,
            "kreativ": 3,
        },
        "Autos reparieren": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 2,
            "drinnen": 2,
            "kreativ": 2,
        },
        "Programmieren": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 3,
            "körperlich": 1,
            "drinnen": 3,
            "kreativ": 3,
        },
        "Reiten": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 3,
            "drinnen": 1,
            "kreativ": 1,
        },
        "Fotografie": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 1,
            "drinnen": 2,
            "kreativ": 3,
        },
        "Gitarre spielen": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 1,
            "drinnen": 3,
            "kreativ": 3,
        },
        "Kochen": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 3,
            "körperlich": 1,
            "drinnen": 3,
            "kreativ": 2,
        },
        "Zeichnen": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 1,
            "drinnen": 3,
            "kreativ": 3,
        },
        "Musik machen": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 1,
            "drinnen": 3,
            "kreativ": 3,
        },
        "Modellbau": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 1,
            "drinnen": 3,
            "kreativ": 3,
        },
        "Gärtnern": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 2,
            "drinnen": 1,
            "kreativ": 2,
        },
        "Radfahren": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 3,
            "drinnen": 1,
            "kreativ": 1,
        },
        "Schwimmen": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 3,
            "drinnen": 2,
            "kreativ": 1,
        },
        "Yoga": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 2,
            "drinnen": 3,
            "kreativ": 1,
        },
        "Wandern": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 2,
            "drinnen": 0,
            "kreativ": 1,
        },
        "Malen": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 1,
            "drinnen": 3,
            "kreativ": 3,
        },
        "Klavier spielen": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 1,
            "drinnen": 3,
            "kreativ": 3,
        },
        "Elektronik basteln": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 1,
            "drinnen": 3,
            "kreativ": 3,
        },
        "Briefmarken sammeln": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 1,
            "drinnen": 3,
            "kreativ": 1,
        },
        "Vogelbeobachtung": {
            "freiwillig": 3,
            "Freizeit": 3,
            "regelmäßig": 2,
            "körperlich": 1,
            "drinnen": 0,
            "kreativ": 2,
        },
    }
    for hobby_name, attrs in assignments.items():
        for attr_name, value in attrs.items():
            assign(hobby_name, attr_name, value)
    db.session.commit()
