from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def display_station(station: SpaceStation) -> None:
    """Print a station's key stats in a human-readable block."""
    status = "Operational" if station.is_operational else "Offline"
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Status: {status}")


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)

    # last_maintenance is declared as datetime. Pydantic also accepts an ISO
    # string here and coerces it (see the printed type below), but we pass a
    # real datetime so static type checking stays happy.
    maintenance_stamp = datetime.fromisoformat("2024-01-15T10:30:00")
    valid_station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=maintenance_stamp,
    )
    print("Valid station created:")
    display_station(valid_station)
    stamp_type = type(valid_station.last_maintenance).__name__
    print(f"last_maintenance type: {stamp_type}")

    print("=" * 40)

    # An invalid station: crew_size is above the allowed maximum of 20.
    # Building it raises ValidationError; we catch it so execution continues.
    try:
        SpaceStation(
            station_id="BAD",
            name="Overcrowded Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=50.0,
            last_maintenance=datetime.fromisoformat("2024-02-01T08:00:00"),
        )
    except ValidationError as error:
        print("Expected validation error:")
        print(error)


if __name__ == "__main__":
    main()
