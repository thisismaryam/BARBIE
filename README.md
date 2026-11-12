# BARBIE v0 — hello and to-dos, plus chat

BARBIE is a tiny command-line assistant. Run `friday.py`, tell it your name, and it greets you once, then listens for commands in a loop:

- `add <task>` — append a task
- `list` — show numbered tasks
- `done <number>` — mark a task done
- `chat <message>` — send a message to a free LLM and print the answer (remembers earlier turns while running)
- `quit` — exit

Unknown commands get a polite, literal answer — BARBIE does exactly what you say.

## Install

```bash
git clone https://github.com/<you>/barbie.git
cd barbie
python -m pip install pytest requests# my barbie project 
