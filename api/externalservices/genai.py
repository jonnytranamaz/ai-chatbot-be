import google.generativeai as genai
import os
import time
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenerativeAIService:
    def __init__(self):
        # Configure the API key
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        logger.info("Generative model initialized")

    def get_response(self, prompt: str) -> str:
        # Simulate some processing time
        time.sleep(random.uniform(0.1, 0.5))
        
        # Generate content based on the prompt
        try:
            text_response = self.model.generate_content(prompt).text
            logger.info(f"Generated response for prompt: {prompt}")
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            text_response = "An error occurred while generating the response."
        
        return text_response

    def log_response(self, prompt: str, response: str):
        # Log the prompt and response
        with open("responses.log", "a") as log_file:
            log_file.write(f"Prompt: {prompt}\nResponse: {response}\n\n")
        logger.info("Response logged")

    def run_interactive_mode(self):
        # Run an interactive mode for testing
        while True:
            prompt = input("Enter a prompt (or 'exit' to quit): ")
            if prompt.lower() == 'exit':
                break
            response = self.get_response(prompt)
            print(f"Response: {response}")
            self.log_response(prompt, response)

    def batch_process_prompts(self, prompts: list):
        # Process a batch of prompts
        responses = []
        for prompt in prompts:
            response = self.get_response(prompt)
            responses.append(response)
            self.log_response(prompt, response)
        return responses

    def save_responses_to_file(self, responses: list, filename: str):
        # Save responses to a file
        with open(filename, "w") as file:
            for response in responses:
                file.write(response + "\n")
        logger.info(f"Responses saved to {filename}")

    def load_prompts_from_file(self, filename: str) -> list:
        # Load prompts from a file
        with open(filename, "r") as file:
            prompts = file.readlines()
        prompts = [prompt.strip() for prompt in prompts]
        logger.info(f"Loaded {len(prompts)} prompts from {filename}")
        return prompts

    def simulate_long_running_task(self):
        # Simulate a long-running task
        logger.info("Starting long-running task")
        for i in range(10):
            time.sleep(1)
            logger.info(f"Task progress: {i+1}/10")
        logger.info("Long-running task completed")

    def generate_multiple_responses(self, prompt: str, count: int) -> list:
        # Generate multiple responses for a single prompt
        responses = []
        for _ in range(count):
            response = self.get_response(prompt)
            responses.append(response)
        return responses

    def print_responses(self, responses: list):
        # Print all responses
        for i, response in enumerate(responses):
            print(f"Response {i+1}: {response}")

    def run_scheduled_tasks(self):
        # Run scheduled tasks
        logger.info("Starting scheduled tasks")
        while True:
            self.simulate_long_running_task()
            time.sleep(60)  # Run every 60 seconds

    def handle_user_input(self):
        # Handle user input
        while True:
            user_input = input("Enter a command (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break
            elif user_input.lower() == 'interactive':
                self.run_interactive_mode()
            elif user_input.lower() == 'batch':
                prompts = ["What is AI?", "Explain machine learning.", "What is deep learning?"]
                responses = self.batch_process_prompts(prompts)
                self.print_responses(responses)
            elif user_input.lower() == 'schedule':
                self.run_scheduled_tasks()
            else:
                print("Unknown command")

if __name__ == "__main__":
    service = GenerativeAIService()
    prompt = "Explain the importance of fast language models."
    response = service.get_response(prompt)
    print(response)
    service.log_response(prompt, response)

    # Run interactive mode
    service.run_interactive_mode()

    # Example batch processing
    prompts = [
        "What is the future of AI?",
        "How does machine learning work?",
        "What are the benefits of cloud computing?"
    ]
    responses = service.batch_process_prompts(prompts)
    service.save_responses_to_file(responses, "batch_responses.txt")

    # Load prompts from a file and process them
    loaded_prompts = service.load_prompts_from_file("prompts.txt")
    loaded_responses = service.batch_process_prompts(loaded_prompts)
    service.save_responses_to_file(loaded_responses, "loaded_responses.txt")

    # Simulate a long-running task
    service.simulate_long_running_task()

    # Generate multiple responses for a single prompt
    multiple_responses = service.generate_multiple_responses("Tell me a joke.", 5)
    service.print_responses(multiple_responses)

    # Handle user input
    service.handle_user_input()