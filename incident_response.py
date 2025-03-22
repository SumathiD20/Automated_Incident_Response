import openai

# Load your API key
API_KEY = "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"

def generate_response(system_name, error_message):
    prompt = f"""
    This is an incident response AI. Analyze the following error message and provide troubleshooting steps.
    
    System Name: {system_name}
    Error Message: {error_message}
    
    Provide a detailed incident response plan.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI incident responder."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

# Example usage
if __name__ == "__main__":
    system_name = input("Enter system name: ")
    error_message = input("Paste the error message: ")
    
    response = generate_response(system_name, error_message)
    print("\nIncident Response Plan:\n", response)
