# CodeScribe

CodeScribe is a Python Package that allows you to convert GitHub repositories into formatted text, including a directory structure and file contents.

## Installation

You can install the package using pip:

```
pip install codescribe
```

## Usage

Here's a simple example of how to use the package:

```python
from codescribe import codescribe

repo_url = 'https://github.com/username/repo'
access_token = 'your_github_access_token'  # optional

formatted_text = codescribe(repo_url, access_token)
print(formatted_text)
```

## Features

- Fetches repository contents from GitHub
- Generated a directory structure
- Formats file contents with proper seperation
- Supports private respositories with access token

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
