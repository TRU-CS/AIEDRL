from pprint import pprint
from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

class MyAgent:
    def __init__(self, system_message: str):
        self.system_message = system_message
        self.agent = self._agent_constructor()
        self.reset_conversation()
    
    def reset_conversation(self):
        # Initialize conversation history with the system message
        self.conversation_history = [SystemMessage(content=self.system_message)]

    def invoke(self, message:HumanMessage) -> AIMessage:
        self.conversation_history.append(message)
        try:
            response = self.agent.invoke({"messages": self.conversation_history})
            self.conversation_history = response["messages"]  # Update conversation history with the agent's response
        except Exception as e:
            # error invoking agent. Log the error and raise an exception
            raise Exception(f"Error invoking agent: {e}")
        
        return self._get_final_message(response)

    def invoke_pprint(self, message:HumanMessage) -> AIMessage:
        out = self.invoke(message=message)
        pprint(out.content)
        return out

    # Deprecated?? See below. 
    # def _get_final_message(self, response: dict) -> AIMessage:
    #     """
    #     Extract the final user-facing AI response from a LangChain-style run output.
    #     Safely skips tool-call placeholders and returns the last meaningful AIMessage.
    #     """
    #     print("types:", [type(message)  for message in response["messages"]])
    #     messages = response.get("messages", [])

    #     for msg in reversed(messages):
    #         if isinstance(msg, AIMessage) and msg.content:
    #             return msg

    #     raise ValueError("No final AIMessage with content found in response.")

    def _get_final_message(self, response: dict) -> AIMessage: # Edit: Makes easier to detect errors in case the output is not as expected. 
        """
        Extract the final user-facing AI response from a LangChain-style run output.
        Safely skips tool-call placeholders and returns the last meaningful AIMessage.
        """
        
        last_respose_message = response["messages"][-1]
        if isinstance(last_respose_message, AIMessage) and last_respose_message.content:
            return last_respose_message
        raise ValueError("No final AIMessage with content found in response. Last message:", type(last_respose_message), last_respose_message)


    def _agent_constructor(self):
        # For simplicity, we return agent with a fixed agent configuration
        model = ChatOpenAI(
            model="gpt-4.1-nano",
            temperature=0.0, # 0.1
            max_tokens=1000,
            timeout=30
            # ... (other params)
        )
        agent_tutor = create_agent(model , tools=None)
        return agent_tutor

    
## TUTORS

class Tutor(MyAgent):
    def __init__(self, system_message: str):
        super().__init__(system_message)

class TutorCodeChecking(Tutor):
    """
    TODO: Finish tool to Check Code.
    """
    def __init__(self, system_message: str):
        super().__init__(system_message)

    def _agent_constructor(self):
        # For simplicity, we return agent with a fixed agent configuration
        model = ChatOpenAI(
            model="gpt-4.1-nano",
            temperature=0.0, # 0.1
            max_tokens=1000,
            timeout=30
            # ... (other params)
        )
        agent_tutor = create_agent(model , tools=[self.check_code])
        return agent_tutor

    def check_code(self, code: str) -> str:
        """
        TODO: Implement code checking logic using the agent. 
        Function takes python code from the agent, checks it for correctness, and returns output.
        """
        pass

## STUDENTS

class Student(MyAgent):
    def __init__(self, system_message: str):
        super().__init__(system_message)

    def invoke(self, message: AIMessage) -> HumanMessage:
        """
        Student receives an AIMessage from the Tutor and responds with a HumanMessage.
        This simulates a student reacting to the tutor's guidance.
        """
        ai_response = super(Student, self).invoke(HumanMessage(content=message.content))
        return HumanMessage(content=ai_response.content)

    def invoke_pprint(self, message:AIMessage) -> HumanMessage:
        out = self.invoke(message=message)
        pprint(out.content)
        return out