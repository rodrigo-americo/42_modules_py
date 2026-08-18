from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):

    name: str = "Data Processor"

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

    @property
    def total_ingested(self) -> int:
        return self._total_ingested

    @property
    def remaining(self) -> int:
        return len(self._data)


class NumericProcessor(DataProcessor):

    name = "Numeric Processor"

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

    name = "Text Processor"

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

    name = "Log Processor"

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


class DataStream:

    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            processed = False
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    processed = True
                    break
            if not processed:
                print(
                    "DataStream error - Can't process element in "
                    f"stream: {element}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            print(
                f"{proc.name}: total {proc.total_ingested} items "
                f"processed, remaining {proc.remaining} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Stream ===\n")

    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Numeric Processor")
    numeric = NumericProcessor()
    stream.register_processor(numeric)

    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nRegistering other data processors")
    text = TextProcessor()
    log = LogProcessor()
    stream.register_processor(text)
    stream.register_processor(log)

    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print(
        "\nConsume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
    )
    for _ in range(3):
        numeric.output()
    for _ in range(2):
        text.output()
    log.output()
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
