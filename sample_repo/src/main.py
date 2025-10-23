# Sample Python Project for Codebase Genius Testing

"""
A simple data processing application that demonstrates
various programming concepts for documentation generation testing.
"""

import os
import json
from typing import List, Dict, Any
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    """
    Abstract base class for data processors.

    This class defines the interface that all data processors
    must implement to ensure consistent behavior across
    different processing strategies.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the data processor.

        Args:
            config: Configuration dictionary with processing parameters
        """
        self.config = config
        self.processed_count = 0

    @abstractmethod
    def validate_data(self, data: Any) -> bool:
        """
        Validate input data before processing.

        Args:
            data: The data to validate

        Returns:
            True if data is valid, False otherwise
        """
        pass

    @abstractmethod
    def process_data(self, data: Any) -> Any:
        """
        Process the validated data.

        Args:
            data: The data to process

        Returns:
            Processed data
        """
        pass

    def save_results(self, results: Any, output_path: str) -> None:
        """
        Save processing results to a file.

        Args:
            results: The results to save
            output_path: Path where to save the results
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"Results saved to {output_path}")


class JSONProcessor(DataProcessor):
    """
    Concrete implementation for processing JSON data.

    This processor handles JSON files, validates their structure,
    and transforms them according to specified rules.
    """

    def validate_data(self, data: Any) -> bool:
        """
        Validate that data is a valid JSON structure.

        Args:
            data: Data to validate

        Returns:
            True if data is a dictionary or list, False otherwise
        """
        return isinstance(data, (dict, list))

    def process_data(self, data: Any) -> Dict[str, Any]:
        """
        Process JSON data by adding metadata and structure.

        Args:
            data: JSON data to process

        Returns:
            Enhanced data with metadata
        """
        if isinstance(data, dict):
            processed = {
                "original_data": data,
                "metadata": {
                    "processed_at": self._get_timestamp(),
                    "processor_type": "JSONProcessor",
                    "config": self.config
                },
                "statistics": self._calculate_stats(data)
            }
        else:  # list
            processed = {
                "original_data": data,
                "metadata": {
                    "processed_at": self._get_timestamp(),
                    "processor_type": "JSONProcessor",
                    "config": self.config
                },
                "statistics": {
                    "item_count": len(data),
                    "total_items": len(data)
                }
            }

        self.processed_count += 1
        return processed

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

    def _calculate_stats(self, data: dict) -> Dict[str, Any]:
        """Calculate basic statistics for dictionary data."""
        return {
            "key_count": len(data),
            "total_keys": len(data),
            "max_depth": self._calculate_depth(data)
        }

    def _calculate_depth(self, data: dict, depth: int = 0) -> int:
        """Calculate maximum depth of nested dictionary."""
        if not isinstance(data, dict) or not data:
            return depth

        return max(self._calculate_depth(value, depth + 1)
                  for value in data.values())


def main():
    """
    Main entry point for the data processing application.

    This function demonstrates how to use the DataProcessor
    classes to process JSON data from files or other sources.
    """
    # Configuration
    config = {
        "input_format": "json",
        "output_format": "enhanced_json",
        "validation_rules": {
            "require_keys": ["id", "name"],
            "max_size": 1000
        }
    }

    # Sample data
    sample_data = {
        "id": 1,
        "name": "Sample Record",
        "details": {
            "category": "example",
            "tags": ["sample", "test"],
            "nested": {
                "deep": "value"
            }
        }
    }

    # Create processor
    processor = JSONProcessor(config)

    # Validate and process data
    if processor.validate_data(sample_data):
        results = processor.process_data(sample_data)

        # Save results
        processor.save_results(results, "output/processed_data.json")

        print(f"Successfully processed {processor.processed_count} records")
    else:
        print("Data validation failed")


def run_tests():
    """Run unit tests for the data processor."""
    print("Running tests...")

    # Test data
    test_data = {
        "id": 1,
        "name": "Test",
        "value": 42
    }

    config = {"test": True}
    processor = JSONProcessor(config)

    # Test validation
    assert processor.validate_data(test_data) == True
    assert processor.validate_data("invalid") == False

    # Test processing
    result = processor.process_data(test_data)
    assert "metadata" in result
    assert "statistics" in result
    assert result["metadata"]["processor_type"] == "JSONProcessor"

    print("All tests passed!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_tests()
    else:
        main()
