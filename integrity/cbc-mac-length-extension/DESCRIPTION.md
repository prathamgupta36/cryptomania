## CBC-MAC Length Extension

This challenge demonstrates how CBC-MAC becomes forgeable when variable-length messages are accepted without binding the length into the MAC computation. You are given two valid message-tag pairs under the same key.

Construct a new message and a valid tag for it by chaining the known MAC state into an extended message.
