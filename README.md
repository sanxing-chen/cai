# CAI

Trivial implementation of a ChatGPT interface in shell, mainly for personal use or as a reference for other implementations.

**The use of clipboard is only supported in macOS.**

# Usage

Basic usage is with the `chatgpt.py` script. You can run it in interactive mode (multiple rounds of conversation), or in oneshot mode (one round of conversation w/ or w/o history).
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

You can export the database to csv/markdown files with chat history in hour, day, week, month, and all time.

```bash
$ python chatgpt.py --mode export
```

# Setup and Requirements

Only tested on macOS
1. `pip install openai`
2. Correct `OPENAI_API_KEY` environment variable set, get it from [here](https://platform.openai.com/account/api-keys). You should have a paid account to use the API.

## Extra Setup for Alfred Workflow

Download the [Workflow](https://github.com/sanxing-chen/cai/raw/main/cai.alfredworkflow) and import it to Alfred.

1. Make sure you can run `run.sh` from the terminal
2. Set `OPENAI_API_KEY` and `CAI_PATH` (path to the repo) in Alfred Workflow (Alfred does **not** load environment variables from `.bashrc` or `.zshrc`)
3. Replace the `python` (and `code`) command in `run.sh` with the absolute path to your python executable, e.g. `/usr/local/bin/python3.8`, obtained by `which python` in the terminal

The `run.sh` script directly open the markdown file in vscode, you can use command + shift + v to open the built-in preview.
I find it more convenient to set the built-in preview as default editor for "*.md" files in vscode.

# Alfred Demo
With a simple Alfred [Workflow](https://github.com/sanxing-chen/cai/raw/main/cai.alfredworkflow) (Keyword -> Run Script) set up, you can do this

https://user-images.githubusercontent.com/18565449/222794526-6a3e07e7-c680-4859-a9c7-0cb765c5a894.mov

https://user-images.githubusercontent.com/18565449/222528490-68269587-ee49-45a9-97bd-2256e60c169f.mov
