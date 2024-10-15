import openai
from tenacity import retry, wait_exponential, stop_after_attempt
from .logging_setup import logger

class PolicyValidator:
    def __init__(self, api_key: str, model: str, max_tokens: int, temperature: float, policies: tuple = None, policy_file: str = None):
        """
        Initializes the policy validator with OpenAI and policies configuration.
        Accepts policies as a tuple or reads from a file and converts them to a tuple.
        
        :param api_key: OpenAI API key
        :param model: GPT model to use
        :param max_tokens: Maximum tokens for GPT response
        :param temperature: Temperature for GPT response variability
        :param policies: A tuple of policies (optional)
        :param policy_file: A file containing policies (optional)
        """
        self.gpt_client = self._init_openai_client(api_key)
        
        if policies:
            self.policies = policies
        elif policy_file:
            self.policies = self._load_policies(policy_file)  # Policies will be loaded as a tuple
        else:
            raise ValueError("Either `policies` or `policy_file` must be provided.")

        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def _init_openai_client(self, api_key: str):
        """Initializes the OpenAI client."""
        openai.api_key = api_key
        return openai

    def _load_policies(self, policy_file: str):
        """Loads the content moderation policies from a file."""
        try:
            with open(policy_file, 'r') as f:
                return tuple(f.read().splitlines())  # Return policies as a tuple
        except FileNotFoundError:
            logger.error(f"Policy file {policy_file} not found.")
            raise
        except Exception as e:
            logger.error(f"Error reading policy file: {e}")
            raise

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    def _call_gpt(self, messages):
        """Calls the OpenAI GPT API with retry mechanism."""
        logger.info("Attempting to call GPT API")
        try:
            response = self.gpt_client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            logger.info("GPT API call successful")
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error while calling OpenAI API: {e}")
            raise

    def _validate_with_gpt(self, text: str, text_type: str):
        """Validates a given text using OpenAI GPT against predefined policies."""
        policies_content = "\n".join(self.policies)  # Join policies into a single string
        validation_messages = [
            {"role": "system", "content": "You are an AI assistant tasked with content moderation."},
            {"role": "user", "content": f"Policies: {policies_content}"},
            {"role": "user", "content": f"Text: {text}"},
            {"role": "user", "content": "Does this text comply with the policies? Answer 'yes' or 'no'."}
        ]
        return self._call_gpt(validation_messages)

    def validate(self, user_input: str):
        """Validates a single input."""
        input_validation = self._validate_with_gpt(user_input, "input")
        if "no" in input_validation.lower():
            logger.warning(f"Input validation failed: {input_validation}")
            return False
        elif "yes" in input_validation.lower():
            logger.info(f"Input validation passed: {input_validation}")
            return True
        else:
            logger.error(f"Input validation Unknown: {input_validation}")
            raise ValueError(f"Unexpected validation result: {input_validation}")
