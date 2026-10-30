from abc import ABC, abstractmethod
from typing import Self

import pandas as pd


class ContextSource(ABC):
    @property
    @abstractmethod
    def required_columns(self) -> frozenset[str]:
        """Columns that must be present in any DataFrame passed to fetch() or join()."""
        ...

    def _validate(self, df: pd.DataFrame) -> None:
        missing = self.required_columns - set(df.columns)
        if missing:
            raise ValueError(
                f"{type(self).__name__} requires columns {sorted(self.required_columns)}. "
                f"Missing: {sorted(missing)}"
            )

    @abstractmethod
    def fetch(self, df: pd.DataFrame) -> Self:
        """Derive spatial extent from df and download the context data.

        Analogous to sklearn's fit — call this once to load context into state.
        Returns self to allow chaining with join().
        """
        ...

    @abstractmethod
    def join(self, df: pd.DataFrame) -> pd.DataFrame:
        """Join the fetched context data onto df and return the augmented result.

        Analogous to sklearn's transform — requires fetch() to have been called first.
        """
        ...

    def fetch_join(self, df: pd.DataFrame) -> pd.DataFrame:
        """Join the fetched context data onto df and return the augmented result."""
        self._validate(df)
        self.fetch(df)
        return self.join(df)
