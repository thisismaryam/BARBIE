import os
import json

# ---------- logic (importable, testable, no stdin) ----------


def add_task(tasks, task):
    tasks.append(task)
    return f"Added: {task}"


def list_tasks(tasks):
    if not tasks:
        return "(no tasks)"
    return "\n".join(f"{i+1}. {t}" for i, t in enumerate(tasks))


def done_task(tasks, n_str):
    try:
        n = int(n_str)
    except ValueError:
        return f"Sorry, '{n_str}' is not a number."
    if not (1 <= n <= len(tasks)):
        return f"Sorry, there's no task numbered{n}."
    t = tasks[n-1]
    tasks[n-1] = f"{t} (done)"
    return f"Done: {t}"


def chat(history, message, client=None):
    history.append({"role": "user", "content": message})
    if client is None:
        try:
            import requests
        except ImportError:
            return "Chat unavailable (requests not installed)."
        key = os.environ.get("GROQ_API_KEY")
        if not key:
            return "GROQ_API_KEY is not set. See README."
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={"model": "llama-3.1-8b-instant",
                      "messages": history},
                timeout=20,
            )
            r.raise_for_status()
            answer = r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Chat failed: {e}"
    else:
        answer = client(history)
    history.append({"role": "assistant", "content": answer})
    return answer


def handle(tasks, history, line, client=None):
    parts = line.strip().split(maxsplit=1)
    if not parts:
        return ""
    cmd, rest = parts[0], (parts[1] if len(parts) > 1 else "")
    if cmd == "add":
        return add_task(tasks, rest)
    if cmd == "list":
        return list_tasks(tasks)
    if cmd == "done":
        return done_task(tasks, rest)
    if cmd == "chat":
        return chat(history, rest, client=client)
    if cmd == "quit":
        return None  # signal exit
    return f"Sorry, I don't know '{cmd}'. I can do: add, list, done, chat, quit."

# ---------- tests (run: python -m pytest friday.py) ----------


def test_add_list_done_unknown():
    tasks = []
    assert "Added" in add_task(tasks, "buy milk")
    assert "buy milk" in list_tasks(tasks)
    assert "Done" in done_task(tasks, "1")
    assert "done" in tasks[0]
    assert "Sorry" in done_task(tasks, "99")
    assert "Sorry" in handle(tasks, [], "frobnicate")
    assert "Sorry" in done_task(tasks, "x")


def test_chat_fake_model_remembers():
    history = []

    def fake(msgs):
        # turn 3 references turn 1's content — proves history is passed
        return f"saw {len(msgs)} msgs, first user: {msgs[0]['content']}"
    chat(history, "my name is Ada", client=fake)
    chat(history, "what's 2+2?", client=fake)
    third = chat(history, "what's my name?", client=fake)
    assert "Ada" in third
    assert third.count("user") or "my name is Ada" in third

# ---------- CLI ----------


def main():
    name = input("What's your name? ").strip() or "friend"
    print(f"Hello, {name}! Commands: add, list, done, chat, quit.")
    tasks, history = [], []
    while True:
        try:
            line = input("> ")
        except EOFError:
            print(f"Goodbye, {name}.")
            return
        out = handle(tasks, history, line)
        if out is None:
            print(f"Goodbye, {name}.")
            return
        if out:
            print(out)


if __name__ == "__main__":
    main()
