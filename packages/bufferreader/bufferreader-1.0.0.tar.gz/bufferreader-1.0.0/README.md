# BufferReader

`BufferReader` is a Python class designed for efficient navigation and reading of a multi-line text buffer. This tool provides the ability to move a pointer through the buffer, read specified ranges of characters, and manage pointer movement without raising exceptions. Instead, it returns status flags (`True`/`False`) for pointer movement operations, allowing seamless error handling.

## Features

-   **Pointer-Based Navigation**: Move a pointer through a text buffer, both forward and backward.
-   **Range-Based Reading**: Read specific ranges of characters between positions, capturing multi-line content.
-   **No Exceptions for Pointer Movement**: Returns `True` or `False` based on success, avoiding pointer movement errors.
-   **Custom Step Sizes**: Control forward and backward step sizes for movement operations.
-   **Stateful Stream**: The `stream` attribute stores the current set of characters read from the buffer.

## Installation

Clone the repository:

```bash
git clone https://github.com/vladimirjo/bufferreader.git
```

Navigate to the directory:
cd bufferreader

Since this is a standalone Python class, no additional dependencies are required.

## Usage

Below is a simple example demonstrating how to use `BufferReader`:

```python
from bufferreader import BufferReader

buffer = "Hello\nWorld\nThis is BufferReader!"
reader = BufferReader(buffer)

# Read the first 5 characters
reader.read(0, 4)
print(reader.stream)  # Output: Hello

# Move to the next character
reader.next()
print(reader.stream)  # Output: \n (newline character)

# Move back to the previous character
reader.before()
print(reader.stream)  # Output: o

# Set the pointer to a specific position (line 1, character 0)
reader.set_pointer(1, 0)
print(reader.stream)  # Output: W (from "World")
```

## API Reference

### Class: `BufferReader`

The `BufferReader` class handles reading and pointer navigation within a text buffer.

#### Attributes:

-   `stream (str)`: Stores the current character(s) from the last read operation.
-   `line_pointer (int)`: The current line index in the buffer (starts at 0).
-   `char_pointer (int)`: The current character index within the current line.
-   `steps_forward (int)`: Tracks how many characters to move forward.
-   `steps_back (int)`: Tracks how many characters to move backward.

#### Methods:

-   **`move(steps: int) -> bool`**
    Moves the pointer forward or backward by the specified number of steps.

-   **`read(start: int = 0, end: int = 0) -> bool`**
    Reads the buffer between the specified start and end positions. Updates the `stream` with the result.

-   **`next() -> bool`**
    Moves the pointer forward by the last read operation's length.

-   **`before() -> bool`**
    Moves the pointer backward by the last read operation's length.

-   **`reset() -> None`**
    Resets the stream to the character at the current pointer position and resets step sizes.

-   **`set_pointer(line_pointer: int, char_pointer: int) -> bool`**
    Moves the pointer to a specific line and character position. Returns `False` if the indices are out of bounds.

## Contributing

Contributions are welcome! If you have suggestions for improvements, feel free to open an issue or submit a pull request.

### Steps to Contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any inquiries or issues, feel free to reach out:

-   GitHub: [@vladimirjo](https://github.com/vladimirjo)
