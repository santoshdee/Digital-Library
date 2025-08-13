# Overview
The Distributed Digital Library System is a Python-based networked application designed to store and retrieve books based on language and genre.
It uses socket programming and multi-threading to handle multiple clients concurrently, with a central coordination server that dynamically routes requests to the appropriate backend servers.

# Features
* Language & Genre-Based Retrieval – Users can request books filtered by language and genre.

* Central Coordination Server – Handles routing logic between clients, language servers, and genre servers.

* Multi-Threaded Communication – Supports multiple simultaneous client requests.

* MySQL Database Integration – Stores book metadata for fast querying.

* In-Memory Caching (with TTL) – Reduces repeated DB calls, improving average book search speed.

* Easily add new language or genre servers via a config.json file without changing code.

* Custom Logger – Records real-time interactions and errors for debugging.
