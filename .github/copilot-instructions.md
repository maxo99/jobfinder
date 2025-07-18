<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# General Instructions
- This project is a Python application that interacts with Elasticsearch and uses a chat client.
- The codebase is structured with adapters for different functionalities, such as Elasticsearch and chat clients.
- The code is organized in a modular way, with each adapter handling specific tasks related to its functionality.
- The project uses environment variables for configuration, such as host and port for Elasticsearch and model for the chat client.

## Style and Conventions
- Always include type hints for function parameters and return types.
- All files should have a logger instance.
- The code includes logging for debugging and information purposes.
- Use descriptive variable and function names.
- Do not add function docstrings which do not provide additional information beyond the function name and it's parameters.
- New functions should always start with a try catch with a logger.error in the catch block and the exception to be re-raised. 