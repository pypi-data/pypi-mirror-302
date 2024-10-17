import os
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)
class ExplainableActionCheckAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_action_check(self, conversation):
        """
        Check if the conversation contains an actionable request for the current project.

        Args:
            conversation (list): The conversation history.

        Returns:
            dict: Action check result in JSON format.
        """

        tree = self.repo.print_tree()
    
        messages = [
            {
                "role": "system",
                "content": (
                    "Analyze the conversation and project structure carefully. Determine if there's a direct, actionable request for the current project. Respond in this exact JSON format:\n\n"
                    "{\n"
                    '    "action": "One sentence describing the direct action for the project and in which specific file, if applicable.",\n'
                    '    "status": "1 if 100% sure it\'s actionable in the current project, 2 otherwise"\n'
                    "}\n\n"
                    "Only return status 1 if you are absolutely certain the action is directly applicable to the current project structure. Otherwise, return status 2."
                )
            },
            {
                "role": "user",
                "content": f"Conversation:\n{conversation}\n\nDetailed project structure:\n{tree}"
            }
        ]
        
        try:
            logger.debug("\n #### The `ExplainableActionCheckAgent` is initiating:\n A request to the AI for action check")
            response = await self.ai.prompt(messages, self.max_tokens, 0, 0)
            logger.debug("\n #### The `ExplainableActionCheckAgent` has successfully:\n Received the AI response for action check")
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            logger.debug("\n #### The `ExplainableActionCheckAgent` is attempting:\n To repair a JSON decoding error in the AI response")
            good_json_string = repair_json(response.choices[0].message.content)
            action_check_json = json.loads(good_json_string)
            return action_check_json
        except Exception as e:
            logger.error(f" #### The `ExplainableActionCheckAgent` encountered an error:\n While performing the action check\n Error: {e}")
            return {
                "action": "",
                "status": "2"
            }

    async def perform_action_check(self, conversation):
        """
        Perform an action check based on the conversation.

        Args:
            conversation (list): The conversation history.

        Returns:
            dict: Action check result.
        """
        logger.debug("\n #### The `ExplainableActionCheckAgent` is beginning:\n The action check process")
        action_check = await self.get_action_check(conversation)
        logger.debug("\n #### The `ExplainableActionCheckAgent` has finished:\n The action check process")
        return action_check
