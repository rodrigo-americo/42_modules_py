from enum import Enum
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    # All fields here reuse ex0-style Field constraints: length ranges for
    # strings, ge/le ranges for integers, an Enum for rank, a bool default.
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_mission(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')
        leaders = [
            m for m in self.crew
            if m.rank in (Rank.COMMANDER, Rank.CAPTAIN)
        ]
        if not leaders:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )
        if self.duration_days > 365:
            experienced = sum(
                1 for member in self.crew if member.years_experience >= 5
            )
            percentage = experienced / len(self.crew)
            if percentage < 0.5:
                raise ValueError(
                    "Long missions need at least 50% experienced crew"
                )
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self


def display_mission(mission: SpaceMission) -> None:
    """Print a mission and its crew roster in a human-readable block."""
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        rank_label = member.rank.value
        line = f"- {member.name} ({rank_label}) - {member.specialization}"
        print(line)


def build_crew() -> List[CrewMember]:
    """A small valid roster reused by the demo below."""
    return [
        CrewMember(
            member_id="CM001",
            name="Sarah Connor",
            rank=Rank.COMMANDER,
            age=45,
            specialization="Mission Command",
            years_experience=20,
        ),
        CrewMember(
            member_id="CM002",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=38,
            specialization="Navigation",
            years_experience=10,
        ),
        CrewMember(
            member_id="CM003",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=33,
            specialization="Engineering",
            years_experience=8,
        ),
    ]


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)

    valid_mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime.fromisoformat("2024-06-01T12:00:00"),
        duration_days=900,
        crew=build_crew(),
        budget_millions=2500.0,
    )
    print("Valid mission created:")
    display_mission(valid_mission)

    print("=" * 41)

    # An invalid mission: a crew with no Commander or Captain.
    # Every CrewMember is valid on its own, so the mission-level
    # model_validator is what rejects it.
    junior_crew = [
        CrewMember(
            member_id="CM010",
            name="Bob Lee",
            rank=Rank.LIEUTENANT,
            age=30,
            specialization="Navigation",
            years_experience=6,
        ),
    ]
    try:
        SpaceMission(
            mission_id="M2024_MOON",
            mission_name="Lunar Survey",
            destination="Moon",
            launch_date=datetime.fromisoformat("2024-09-01T09:00:00"),
            duration_days=120,
            crew=junior_crew,
            budget_millions=800.0,
        )
    except ValidationError as error:
        print("Expected validation error:")
        print(error)


if __name__ == "__main__":
    main()
