# CAI

Trivial implementation of a ChatGPT interface in shell, mainly for personal use or as a reference for other implementations.

**The use of clipboard is only supported in macOS.**

# Usage

```bash
$ ./run.sh chat "Who are you? What are you doing here?"
$ ./run.sh search "Best resorts in the world"
# only in macOS, copy "I don't konw waht I am talking about" to clipboard
$ ./run.sh revise
```

# Requirements

Only tested on macOS, with
- Python 3.8
- sqlite3
- openai
