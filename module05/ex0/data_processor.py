from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):

    def __init__(self) -> None:
        self._data: list[str] = []
        self._total_ingested: int = 0
        self._next_rank_out: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        ...

    def output(self) -> tuple[int, str]:
        if not self._data:
            raise IndexError("No data available to output")
        item = self._data.pop(0)
        rank = self._next_rank_out
        self._next_rank_out += 1
        return (rank, item)


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        if isinstance(data, list):
            return all(
                isinstance(item, (int, float)) and not isinstance(item, bool)
                for item in data
            )
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise TypeError("Improper numeric data")
        if isinstance(data, list):
            self._data.extend(str(item) for item in data)
            self._total_ingested += len(data)
        else:
            self._data.append(str(data))
            self._total_ingested += 1


class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise TypeError("Improper text data")
        if isinstance(data, list):
            self._data.extend(data)
            self._total_ingested += len(data)
        else:
            self._data.append(data)
            self._total_ingested += 1


class LogProcessor(DataProcessor):

    _LOG_KEYS = {"log_level", "log_message"}

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return self._is_valid_log(data)
        if isinstance(data, list):
            return all(
                isinstance(item, dict) and self._is_valid_log(item)
                for item in data
            )
        return False

    def ingest(
        self,
        data: dict[str, str] | list[dict[str, str]],
    ) -> None:
        if not self.validate(data):
            raise TypeError("Improper log data")
        if isinstance(data, list):
            self._data.extend(self._format_log(item) for item in data)
            self._total_ingested += len(data)
        else:
            self._data.append(self._format_log(data))
            self._total_ingested += 1

    def _is_valid_log(self, data: dict[Any, Any]) -> bool:
        if set(data.keys()) != self._LOG_KEYS:
            return False
        return all(isinstance(value, str) for value in data.values())

    def _format_log(self, data: dict[str, str]) -> str:
        return f"{data['log_level']}: {data['log_message']}"


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    numeric = NumericProcessor()
    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(f"Trying to validate input 'Hello': {numeric.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        numeric.ingest("foo")  # type: ignore[arg-type]
    except TypeError as exc:
        print(f"Got exception: {exc}")
    numeric_batch: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {numeric_batch}")
    numeric.ingest(numeric_batch)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")

    print("\nTesting Text Processor...")
    text = TextProcessor()
    print(f"Trying to validate input '42': {text.validate(42)}")
    text_batch = ["Hello", "Nexus", "World"]
    print(f"Processing data: {text_batch}")
    text.ingest(text_batch)
    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")

    print("\nTesting Log Processor...")
    log = LogProcessor()
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")
    log_batch = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"Processing data: {log_batch}")
    log.ingest(log_batch)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
