from abc import ABC, abstractmethod

from ex0.base import Creature


class TransformCapability(ABC):

    def __init__(self) -> None:
        self.is_transformed = False

    @abstractmethod
    def transform(self) -> str:
        ...

    @abstractmethod
    def revert(self) -> str:
        ...


class Shiftling(Creature, TransformCapability):

    def __init__(self, name: str, creature_type: str) -> None:
        super().__init__(name, creature_type)
        TransformCapability.__init__(self)

    def transform(self) -> str:
        if not self.is_transformed:
            self.is_transformed = True
            return f"{self.name} has transformed into its evolved form!"
        return f"{self.name} is already transformed."

    def revert(self) -> str:
        if self.is_transformed:
            self.is_transformed = False
            return f"{self.name} has reverted to its base form."
        return f"{self.name} is already in its base form."

    def attack(self) -> str:
        if self.is_transformed:
            return f"{self.name} attacks with a powerful energy blast!"
        return f"{self.name} attacks with a swift strike!"


class Morphagon(Creature, TransformCapability):

    def __init__(self, name: str, creature_type: str) -> None:
        super().__init__(name, creature_type)
        TransformCapability.__init__(self)

    def transform(self) -> str:
        if not self.is_transformed:
            self.is_transformed = True
            return f"{self.name} has transformed into its evolved form!"
        return f"{self.name} is already transformed."

    def revert(self) -> str:
        if self.is_transformed:
            self.is_transformed = False
            return f"{self.name} has reverted to its base form."
        return f"{self.name} is already in its base form."

    def attack(self) -> str:
        if self.is_transformed:
            return f"{self.name} attacks with a devastating firestorm!"
        return f"{self.name} attacks with a fiery slash!"
