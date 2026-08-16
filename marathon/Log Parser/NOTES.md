The brief: Log File Analyser (command line)

Read a log file where each line looks roughly like: 2026-08-14 10:32:11 ERROR database connection failed
Parse each line into date, time, level, and message
Report: total lines, count per level (ERROR / WARN / INFO), and the 5 most common messages
Save the report as a JSON file
Fetch the current date-time from a public API and include it in the report as "generated_at"
Survive: file not found, a malformed line, and no internet
Make your own sample log file with 50-100 lines, including a few deliberately broken ones.

Coverage check — every requirement maps to a topic:

Parsing lines into fields → variables and data types
Separate parse / count / report functions → functions
Missing file, broken line, no internet → error handling
Reading the log, writing the report → file I/O
Fetching the timestamp, writing JSON → APIs and JSON
Done when: it runs on a good log, runs on a log with broken lines without crashing, runs with the network disconnected, and the counting logic sits in a function that takes a list and returns a dict — no printing inside it.

Do not: add a database, classes, or a web interface. Those come later. The constraint is part of the assignment.