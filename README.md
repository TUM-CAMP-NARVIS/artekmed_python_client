tcnart_py

A minimal Python 3.10 reimplementation of selected parts of the `tcnart` Rust crate (core, schema, serialization, and a sync network wrapper) using:
- Eclipse Zenoh (python) for networking (synchronous API)
- pycdr2 for CDR serialization framing

Notes
- This package focuses on structure compatibility and provides stubs for CDR (de)serialization using pycdr2. Full IDL-backed decoding of complex messages may require additional type descriptors.
- All methods are synchronous by design.
