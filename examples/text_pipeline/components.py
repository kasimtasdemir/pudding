"""Simple text processing components for demonstration."""

# examples/text_pipeline/components.py
from typing import Optional

from pydantic import BaseModel, Field

from pudding.core import BaseComponent, registry


# Schemas
class TextInput(BaseModel):
    """Input for text loader."""

    text: str = Field(..., description="Raw text to process")
    source: Optional[str] = Field(None, description="Source identifier")


class CleanedText(BaseModel):
    """Output from text cleaner."""

    text: str = Field(..., description="Cleaned text")
    source: Optional[str] = None
    changes_made: list[str] = Field(default_factory=list)


class WordStats(BaseModel):
    """Output from word counter."""

    total_words: int
    unique_words: int
    average_word_length: float
    most_common_words: list[tuple[str, int]]
    source: Optional[str] = None


# Components
class TextLoader(BaseComponent[TextInput, TextInput]):
    """Loads and validates text input."""

    def __init__(self):
        super().__init__(
            name="text_loader",
            version="1.0.0",
            input_schema=TextInput,
            output_schema=TextInput,
        )
        registry.register(self.name, self.version, "TextInput", "TextInput")

    async def process(self, input_data: TextInput) -> TextInput:
        """Simply pass through the text after validation."""
        return input_data


class TextCleaner(BaseComponent[TextInput, CleanedText]):
    """Cleans text by removing extra whitespace and normalizing."""

    def __init__(self):
        super().__init__(
            name="text_cleaner",
            version="1.0.0",
            input_schema=TextInput,
            output_schema=CleanedText,
        )
        registry.register(self.name, self.version, "TextInput", "CleanedText")

    async def process(self, input_data: TextInput) -> CleanedText:
        """Clean the text."""
        original = input_data.text
        changes = []

        # Remove extra whitespace
        cleaned = " ".join(original.split())
        if cleaned != original:
            changes.append("removed_extra_whitespace")

        # Convert to lowercase for consistency
        cleaned = cleaned.lower()
        if cleaned != original.lower():
            changes.append("converted_to_lowercase")

        # Remove special characters (keep only letters, numbers, spaces)
        import re

        cleaned = re.sub(r"[^a-z0-9\s]", "", cleaned)
        if len(cleaned) != len(original):
            changes.append("removed_special_characters")

        return CleanedText(text=cleaned, source=input_data.source, changes_made=changes)


class WordCounter(BaseComponent[CleanedText, WordStats]):
    """Counts words and generates statistics."""

    def __init__(self):
        super().__init__(
            name="word_counter",
            version="1.0.0",
            input_schema=CleanedText,
            output_schema=WordStats,
        )
        registry.register(self.name, self.version, "CleanedText", "WordStats")

    async def process(self, input_data: CleanedText) -> WordStats:
        """Generate word statistics."""
        words = input_data.text.split()

        # Count frequencies
        from collections import Counter

        word_counts = Counter(words)

        # Calculate stats
        total_words = len(words)
        unique_words = len(word_counts)
        avg_length = (
            sum(len(word) for word in words) / total_words if total_words > 0 else 0
        )

        return WordStats(
            total_words=total_words,
            unique_words=unique_words,
            average_word_length=round(avg_length, 2),
            most_common_words=word_counts.most_common(5),
            source=input_data.source,
        )
