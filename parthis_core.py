import os
import google.generativeai as genai

class ParthisAgent:
    def __init__(self, agent_name: str = "Parthis", primary_model: str = "gemini-1.5-flash"):
        """
        Parthis Core Agent Engine initializing the name, fallback hierarchy, 
        and system instruction prompt.
        """
        self.agent_name = agent_name
        self.primary_model = primary_model
        
        # API 404 Crash Prevention Fallback Priority Matrix
        self.fallback_chain = [
            self.primary_model,
            "gemini-1.5-pro",
            "gemini-pro"
        ]
        
        self.system_prompt = (
            f"You are {self.agent_name}, an autonomous, resilient, and mobile-native AI assistant. "
            "You run with high error recovery, vector memory context, and modular task execution."
        )

    def process_request(self, prompt: str) -> str:
        """
        Executes user queries with resilient error-handling. 
        Iterates through the model fallback chain if any 404/API errors occur.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "Configuration Error: GEMINI_API_KEY is not set in environment."

        genai.configure(api_key=api_key)

        last_error = None
        # Dynamic Model Fallback Loop
        for model_name in self.fallback_chain:
            try:
                model_instance = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=self.system_prompt
                )
                response = model_instance.generate_content(prompt)
                return response.text
            except Exception as e:
                last_error = e
                print(f"[{self.agent_name}] Warning: Model '{model_name}' failed ({e}). Attempting next fallback...")
                continue
                
        return f"Critical Failure: All fallback model endpoints failed to execute. Last error: {last_error}"

if __name__ == "__main__":
    # Quick Standalone Test Execution
    agent = ParthisAgent()
    print(f"[{agent.agent_name} Core Engine Ready]")
