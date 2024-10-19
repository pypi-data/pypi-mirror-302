import os
import requests
import yaml
import logging
from groq import Groq

# Configure logging
logging.basicConfig(level=logging.INFO)

class OpenAPIGroqDataGenerator:
    def __init__(self, groq_api_key):
        self.groq_client = Groq(api_key=groq_api_key)

    def fetch_openapi_schema(self, swagger_url):
        """
        Fetch the OpenAPI/Swagger schema from the provided URL.
        Supports both JSON and YAML formats.
        """
        try:
            logging.info(f"Fetching OpenAPI schema from: {swagger_url}")
            response = requests.get(swagger_url)
            logging.debug(f"Response Status Code: {response.status_code}")
            logging.debug(f"Response Content: {response.text}")

            if response.status_code == 200:
                try:
                    return response.json()
                except ValueError:
                    logging.info("Failed to parse as JSON, trying YAML...")
                    return yaml.safe_load(response.text)
            else:
                raise Exception(f"Error fetching OpenAPI schema: {response.status_code}")
        except Exception as e:
            logging.error(f"Failed to fetch schema: {str(e)}")
            return {"error": f"Failed to fetch schema: {str(e)}"}

    def create_sample_data_prompt(self, endpoint, parameters):
        """
        Create a prompt for the Groq LLaMA3 model based on the API endpoint and parameters.
        """
        prompt = f"""
        Generate realistic sample data for the following API endpoint:
        
        Endpoint: {endpoint}
        Parameters: {parameters}
        Provide the most realistic JSON response that could be returned by this API.
        """
        logging.debug(f"Created prompt: {prompt}")
        return prompt

    def generate_realistic_data_using_groq(self, prompt):
        """
        Generate realistic data using the Groq LLaMA3 model.
        """
        try:
            logging.info(f"Generating data for prompt: {prompt}")
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192"
            )
            return response.choices[0].message.content
            # # Placeholder for now
            # return "Generated Sample Data (placeholder)"
        except Exception as e:
            logging.error(f"Failed to generate data: {str(e)}")
            return {"error": f"Failed to generate data: {str(e)}"}

    def generate_example_apis(self, swagger_schema):
        """
        Generate example API responses using Groq LLaMA3 for each endpoint in the OpenAPI schema.
        """
        example_apis = {}

        for path, methods in swagger_schema['paths'].items():
            for method, details in methods.items():
                if isinstance(details, dict):
                    parameters = details.get('parameters', [])
                    prompt = self.create_sample_data_prompt(path, parameters)
                    sample_data = self.generate_realistic_data_using_groq(prompt)

                    # Store the generated sample data
                    example_apis[path] = {
                        "method": method.upper(),
                        "sample_data": sample_data
                    }
                    logging.debug(f"Generated sample data for {path}: {sample_data}")
                else:
                    logging.warning(f"Expected details to be a dictionary, but got {type(details)} for path {path} and method {method}")
        
        return example_apis

    def get_generated_data(self, swagger_url):
        """
        Fetch the Swagger schema and generate realistic API data using Groq.
        """
        swagger_schema = self.fetch_openapi_schema(swagger_url)
        if 'error' in swagger_schema:
            return swagger_schema

        return self.generate_example_apis(swagger_schema)
