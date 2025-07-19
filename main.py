import asyncio
import json
from datetime import datetime
import argparse
import os
from pathlib import Path
from litellm import acompletion

async def main(llm_list: list[str]|None=None, llm_file: str|None=None, prompt_string: str|None=None, prompt_file: str|None=None, system_prompt: str|None=None, system_prompt_file: str|None=None):
    # Read system prompt from file if provided
    if system_prompt_file is not None:
        system_prompt_path = Path(system_prompt_file).expanduser()
        with open(system_prompt_path, "r") as f:
            system_prompt = f.read()

    # Set default system prompt if none provided
    if system_prompt is None:
        system_prompt = "You are a helpful assistant"

    if prompt_string is not None:
        prompt = prompt_string
    else:
        prompt_path = Path(prompt_file).expanduser()
        with open(prompt_path, "r") as f:
            prompt = f.read()

    if llm_file is not None:
        with open(llm_file, "r") as f:
            # ignore empty lines and comments
            llm_list = [line for line in f.read().splitlines() if line and not line.startswith('#')]

    if llm_list is None:
        print("No LLMs provided")
        exit(1)

    for llm in llm_list:
        if '/' not in llm:
            print(f"LLM {llm} is not a valid LLM - format is <provider>/model-name>")
            exit(1)

    results = []
    for llm in llm_list:
        response = await acompletion(
            model=llm,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        results.append({
            "model": llm,
            "response": str(response.choices[0].message.content)
        })

    now_string = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    results_file = f"results_{now_string}.json"
    with open(results_file, "w") as f:
        json.dump(results, f)

    for result in results:
        print(f"Model: {result['model']}")
        print(f"Response: {result['response']}")
        print("-" * 100)

    print(f"Results saved to {results_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    llm_group = parser.add_mutually_exclusive_group(required=True)
    llm_group.add_argument("--llm-list", type=str, required=True, help="List of LLMs to use, separated by commas (eg, 'openai/gpt-41,openrouter/llama4.0,anthropic/claude-4')")
    llm_group.add_argument("--llm-file", type=str, required=True, help="Path to file containing list of LLMs to use, separated by newlines (eg, 'openai/gpt-41\nopenrouter/meta/llama4.0\nanthropic/claude-4')")

    # Create mutually exclusive group for prompt arguments
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt-string", type=str, help="Prompt text as string")
    prompt_group.add_argument("--prompt-file", type=str, help="Path to file containing prompt text")

    # Create mutually exclusive group for system prompt arguments (not required, will use default)
    system_prompt_group = parser.add_mutually_exclusive_group(required=False)
    system_prompt_group.add_argument("--system-prompt", type=str, help="System prompt text as string")
    system_prompt_group.add_argument("--system-prompt-file", type=str, help="Path to file containing system prompt text")

    args = parser.parse_args()
    asyncio.run(main(args.llm_list, args.llm_file, args.prompt_string, args.prompt_file, args.system_prompt, args.system_prompt_file))
