<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# General Instructions
- This project is a Python application that interacts with Postgres and uses a chat client.
- The codebase is structured with adapters for different functionalities, such as Postgres and chat clients.
- The code is organized in a modular way, with each adapter handling specific tasks related to its functionality.

## General Guidelines
- Always ask for clarification if the request is not clear or there are multiple routes to consider.
- When providing code for updates to the codebase, return only the modified lines and where they should be placed.

## Generation Guidelines
- Never present generated, inferred, speculated or deduced content as fact.
- Label unverified content at the start of a sentence using `[Inference] [Speculation] [Unverified]`.

## Style and Conventions
- Always include type hints for function parameters and return types.
- All files should have a logger instance.
- The code includes logging for debugging and information purposes.
- Use descriptive variable and function names.
- Do not add function docstrings which do not provide additional information beyond the function name and it's parameters.
- New functions should always start with a try catch with a logger.error in the catch block and the exception to be re-raised. 