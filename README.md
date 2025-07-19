# prompt_evaluator

A command-line tool to run a single prompt (or system + user prompts) across multiple Large Language Models (LLMs) and collect their responses. Built on `litellm`, it serializes outputs into a timestamped JSON file and prints them to the console.

---

## Repository

```bash
git clone https://github.com/ohnotnow/prompt_evaluator.git
cd prompt_evaluator
```

---

## Requirements

- git (for cloning)
- Python 3.8+
- [uv tool](https://docs.astral.sh/uv/) (for dependency management and execution)

---

## Installation

All platforms (MacOS, Ubuntu, Windows)

```bash
# From the repo root
uv sync
```

> This will read your project’s dependency configuration and install them into a local virtual environment.
> Visit https://docs.astral.sh/uv/ for full uv documentation.

---

## Usage

The entrypoint is `main.py`. You must specify either `--llm-list` or `--llm-file`, and either `--prompt-string` or `--prompt-file`. System prompts are optional.

```bash
uv run main.py -- \
  --llm-list "openai/gpt-4,anthropic/claude-3" \
  --prompt-file "./prompts/my_prompt.txt" \
  --system-prompt "You are a helpful assistant."
```

The backslash (`\`) ensures flags are passed to `main.py` rather than to `uv`.

### Flags

Required LLM selection (exactly one):

  • `--llm-list`
    Comma-separated list of LLM identifiers (e.g. `openai/gpt-4,openrouter/llama4.0`)
  • `--llm-file`
    Path to a newline-separated file of LLM identifiers (comments and blank lines are ignored)

Required prompt selection (exactly one):

  • `--prompt-string`
    Prompt text directly on the CLI
  • `--prompt-file`
    Path to a file containing the user prompt

Optional system prompt (mutually exclusive):

  • `--system-prompt`
    System prompt text directly on the CLI
  • `--system-prompt-file`
    Path to a file containing the system prompt

### Example with files

```bash
# llms.txt:
# openai/gpt-4
# anthropic/claude-3

# prompt.txt:
# Write a poem about autumn.

uv run main.py -- \
  --llm-file "./llms.txt" \
  --prompt-file "./prompt.txt" \
  --system-prompt-file "./system.txt"
```

---

## Output

- Prints each model’s name and response to stdout, separated by lines.
- Writes `results_<YYYY_MM_DD_HH_MM_SS>.json` in the working directory, containing an array of:
  ```json
  [
    {
      "model": "openai/gpt-4",
      "response": "..."
    },
    ...
  ]
  ```

## Example llm file
The code uses [litellm](https://docs.litellm.ai/docs/) under the hood - so the format of the model names follows their convention.

```
openai/o4-mini
openai/gpt-4.1
# you can comment out lines
anthropic/claude-sonnet-4
openrouter/google/gemini-2.5-flash
```

---

## Development

If you prefer a standard venv and pip workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install litellm
pip install -r requirements.txt  # if you maintain one
python main.py --help
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/xyz`)
3. Commit your changes
4. Open a pull request

---

## License

This project is licensed under the MIT License.
