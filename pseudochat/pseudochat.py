"""
PseudoChat entry point.

Everything chat-specific lives in pseudochat.yaml (state,
tools, criterias, settings) and pseudochat_tools.py (the
handlers).

The loop has no exit tool: it ends when the user types
exit/quit (or Ctrl+C / EOF) in get_user_input, or at
settings.max_iterations.
"""

from pathlib import Path

from pseudoagent import load_config, run

CONFIG_PATH = Path(__file__).with_name("pseudochat.yaml")


if __name__ == "__main__":

    run(load_config(CONFIG_PATH))
