# kson: Nobly-Flavoured JSON

> a.k.a. kingSON

KSON is a custom data format similar to JSON but uses the crown emoji as the key-value delimiter.

This Python library provides functions to parse and serialize KSON data, following the design of Python's built-in `json` module.

**IMPORTANT: This Library is a joke project. It's published for archive.**
**You should not include this in your projects.**

## Features

- [x] Parse KSON strings and files into Python objects
- [x] Serialize Python objects into KSON strings and files

## Installation

Install the KSON Library using pip:

```bash
pip install kson-irs
```

## Usage

### Parsing KSON Data from String Object

```python
import kson

kson_data = '''
{
    "name" 👑 "John Doe",
    "age" 👑 114,
    "isPresident" 👑 false,
    "skills" 👑 ["Rust", "Syndication", "KSON"]
}
'''

data = kson.loads(kson_data)
print(data)

```

Such output should be observed:

```python
{'name': 'John Doe', 'age': 114, 'isPresident': False, 'skills': ['Rust', 'Syndication', 'KSON']}
```

### Serializing Python objects to KSON

```python
import kson

obj = {
    "company": "IRregular Syndicate",
    "employees": [
        {
            "id": 1,
            "name": "John Doe",
            "position": "President(Good Job!)",
            "skills": ["KSON"]
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "position": "Duchess",
            "skills": ["Syndication", "Python"]
        }
    ],
    "isHiring": True
}

kson_text = kson.dumps(obj, indent=4)
print(kson_text)
```

Such expected output shall be observed:
```text
{
    "company" 👑 "IRregular Syndicate",
    "employees" 👑 [
        {
            "id" 👑 1,
            "name" 👑 "John Doe",
            "position" 👑 "President(Good Job!)",
            "skills" 👑 [
                "KSON"
            ]
        },
        {
            "id" 👑 2,
            "name" 👑 "Jane Smith",
            "position" 👑 "Duchess",
            "skills" 👑 [
                "Syndication",
                "Python"
            ]
        }
    ],
    "isHiring" 👑 true
}

```

### Reading KSON from a File

```python
import kson

with open('data.kson', 'r', encoding = 'utf-8') as file:
    data = kson.load(file)

print(data)
```

### Writing KSON to a File

```python
import kson

data = {
    "title": "IRoSha City",
    "population": 727,
    "coordinates": {
        "latitude": 34.0522,
        "longitude": -118.2437
    },
    "when": "you",
    "see": "it",
}

with open('city.kson', 'w', encoding='utf-8') as file:
    kson.dump(data, file, indent = 2)
```

## Exception Handling
The library raises `KSONDecodeError` and `KSONEncodeError` exceptions for decoding and encoding errors, respectively.

```python
import kson

try:
    # Missing Proof of Nobility and Supreme Power!
    data = kson.loads('{"key" "value"}')
except kson.KSONDecodeError as e:
    print(f"Decoding failed: {e}")
```

## License
This project is licensed under the MIT License.

## Acknowledgments

We wish to acknowledge that references to monarchies or any form of autocratic governance may be inappropriate or unsettling in certain contexts.

The KSON format's association with the crown is a stylistic choice and is not an endorsement of any specific political system or ideology.
