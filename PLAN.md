The problem, in one sentence
BARBIE is a tiny command-line assistant ("friday.py") that greets me once, remembers my to-dos in a running list, and can chat with me through a free LLM API with conversation memory — but right now none of that exists, so the problem is: nothing on my machine yet lets me add/list/complete tasks and chat with a model from one polite, literal CLI.

Who BARBIE is for
Me. Single user, my laptop, my terminal. No web UI, no auth, no multi-user concerns. If it works for me, it's done.

Three things BARBIE must do this week
#	What it must do	"Done" looks like (checkable by someone else)
1	Greet and track to-dos in a loop — friday.py asks my name once, greets me, then loops on add <task> / list / done <number> / quit, using a list + if/elif + while. Unknown commands get a polite, literal reply.	python friday.py runs interactively; then python -m pytest tests/test_todo.py passes, covering add, list, done, and unknown command. Checker: clone repo, follow README, run both commands.
2	Chat with a free model, with memory — chat <message> sends the message + prior turns to a free model via its API, prints the reply, keeps history in a list of messages, reads the key from an env var, and prints a clear error (no traceback) on request failure.	tests/test_chat.py passes using a fake model (no network); a 3-turn manual chat where turn 3 references something said in turn 1 (shown in README/NOTES); grep of repo history for the key pattern returns nothing.
3	Ship with tests running on GitHub Actions — .github/workflows/tests.yml in the repo, running on every push, daily, and on manual dispatch; also greps every commit for API keys.	Actions tab shows a green run on the latest commit; repo is public; git log -p | grep -i "sk-" (and similar) returns nothing. Checker: open Actions tab, look at the latest run + the secret-scan step.# my plan 
