from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def check_contact(self) -> "AlienContact":
        # Business rules that depend on more than one field at once.
        # Each raise short-circuits, so only the first broken rule is reported.
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')
        is_physical = self.contact_type == ContactType.PHYSICAL
        if is_physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        is_telepathic = self.contact_type == ContactType.TELEPATHIC
        if is_telepathic and self.witness_count < 3:
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        strong_signal = self.signal_strength > 7.0
        if strong_signal and self.message_received is None:
            raise ValueError("Strong signals should include received messages")
        return self


def display_contact(contact: AlienContact) -> None:
    """Print an alien contact report in a human-readable block."""
    message = contact.message_received or "(none)"
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: {message!r}")


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 38)

    # A valid report: radio contact, strong signal so it carries a message,
    # ID starts with "AC", enough witnesses for its (non-telepathic) type.
    valid_contact = AlienContact(
        contact_id="AC-2024-001",
        timestamp=datetime.fromisoformat("2024-03-10T21:45:00"),
        location="Area 51, Nevada",
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
    )
    print("Valid contact report:")
    display_contact(valid_contact)

    print("=" * 38)

    # An invalid report: telepathic contact with only 2 witnesses.
    # Every other field is valid so the model_validator is what rejects it.
    try:
        AlienContact(
            contact_id="AC-2024-002",
            timestamp=datetime.fromisoformat("2024-03-11T02:15:00"),
            location="Roswell, New Mexico",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=4.0,
            duration_minutes=10,
            witness_count=2,
        )
    except ValidationError as error:
        print("Expected validation error:")
        print(error)


if __name__ == "__main__":
    main()
