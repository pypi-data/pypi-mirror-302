
# Policy Validator

Policy Validator is a Python package that leverages OpenAI's GPT models to validate text against predefined content policies. It ensures that user input conforms to specific rules, making it useful for content moderation, compliance checks, and safety regulations.

## Key Features
- **OpenAI GPT Integration**: Uses OpenAI models to validate text based on content moderation policies.
- **Retry Mechanism**: Ensures reliable API calls with built-in retry functionality.
- **Logging**: Offers comprehensive logging to track and debug policy validation processes.
- **Flexible Policy Input**: Policies can be supplied either as tuples directly or loaded from a file.
- **Customizable**: Adjust model parameters such as max tokens, temperature, and the specific OpenAI's model used.

## Installation

To install the Policy Validator package, use `pip`:

```bash
pip install policy_validator
```

## Usage

The `PolicyValidator` class allows you to pass policies either as a tuple or via a file.

### Example 1: Passing Policies as a Tuple

In this example, policies are defined directly as a tuple in Python:

```python
from policy_validator import PolicyValidator

# Define policies directly as a tuple
policies = (
    "No abusive language.",
    "No personal information sharing.",
    "No inappropriate content."
)

api_key = "your_openai_api_key"
validator = PolicyValidator(api_key=api_key, model="gpt-4o-mini", max_tokens=100, temperature=0.3, policies=policies)

# Validate user input
result = validator.validate("Who is John Doe?")
print(result)
```

### Example 2: Passing Policies via a File

You can also load policies from a file. First, create a `policies.txt` file with the following content:

```plaintext
Policy 1: No abusive language.
Policy 2: No personal information sharing.
Policy 3: No inappropriate content.
```

Now load the policies from this file:

```python
from policy_validator import PolicyValidator

api_key = "your_openai_api_key"
validator = PolicyValidator(api_key=api_key, model="gpt-4o-mini", max_tokens=100, temperature=0.3, policies_file="policies.txt")

# Validate user input
result = validator.validate("Who is Ashkan Rafiee?")
print(result)
```

## Important: Securely Managing API Keys

It's recommended to **avoid hardcoding your API key** in your code as shown in the above examples. Instead, use a more secure method, such as:

- **Environment variables**: Store the API key in an environment variable and access it via `os.getenv()`.
  
  ```python
  import os
  api_key = os.getenv("OPENAI_API_KEY")
  ```

- **Secret management systems**: Use secure secret management tools such as AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault to securely store and access the API key in a managed way.


For any issues, feel free to submit a bug report or open a discussion.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
