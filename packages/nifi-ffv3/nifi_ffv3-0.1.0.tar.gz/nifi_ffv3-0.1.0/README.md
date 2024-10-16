## Description

nifi_ffv3 is a Python library for packaging and unpacking data in the `application/flowfile-v3` format, commonly used in Apache NiFi.

## Features

* Packages data into a byte stream compatible with `flowfile-v3`.
* Allows adding custom attributes to the flowfile.
* Handles large file sizes.

## Installation

```bash
pip install nifi_ffv3
```

## Usage

```python
import io
from nifi_ffv3 import package_flowfile

# Data to be packaged
data = b"Hello, world!"
input_stream = io.BytesIO(data)

# Create an output byte stream
output_stream = io.BytesIO()

# Define custom attributes (optional)
attributes = {"filename": "example.txt", "author": "John Doe"}

# Package the data in flowfile-v3 format
package_flowfile(input_stream, output_stream, attributes=attributes)

# Access the packaged flowfile
flowfile_data = output_stream.getvalue()
```

## Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

Apache-2.0 license
