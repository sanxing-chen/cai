# CAI

Trivial implementation of a ChatGPT interface in shell, mainly for personal use or as a reference for other implementations.

**The use of clipboard is only supported in macOS.**

# Usage

Basic usage is with the `chatgpt.py` script. You can run it in interactive mode (multiple rounds of conversation), or in oneshot mode (one round of conversation).
```bash
$ python chatgpt.py --mode interactive # interactive mode, use "!help" for help
$ python chatgpt.py --mode oneshot --type chat --prompt "Who are you? What are you doing here?"
$ python chatgpt.py --mode oneshot --type search --prompt "Best resorts in the world"
```

If you use macOS with vscode, the simpler `run.sh` script is recommended for oneshot interaction.
Results will be copied to clipboard and shown in vscode automatically.
In one-shot mode, only `ctx_chat` considers the previous context, which is suitable for follow-up questions.
```bash
$ ./run.sh chat "Who are you? What are you doing here?"
$ ./run.sh search "Best resorts in the world"
$ ./run.sh ctx_chat "Talk about one of them in detail." # follow up with the previous context

# copy "I don't konw waht I am talking about" to clipboard, then
$ ./run.sh revise
```

It keeps a local copy of all the conversations in a sqlite3 database.

You can view bill in hour, day, week, month, and all time.
    
```bash
$ python chatgpt.py --mode bill
```

You can export the database to csv files with chat history in hour, day, week, month, and all time.

```bash
$ python chatgpt.py --mode export
```

# Requirements

Only tested on macOS, with
- Python 3.8
- sqlite3
- openai

# Alfred Demo
With a simple Alfred Workflow (Keyword -> Run Script) set up, you can do this

https://user-images.githubusercontent.com/18565449/222528490-68269587-ee49-45a9-97bd-2256e60c169f.mov
