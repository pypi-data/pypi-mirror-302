import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class TaskPlannerPro:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        """
        Initialize the TaskPlanner with necessary configurations.

        Args:
            directory_path (str): Path to the project directory.
            api_key (str): API key for authentication.
            endpoint (str): API endpoint URL.
            deployment_id (str): Deployment ID for the AI model.
            max_tokens (int): Maximum number of tokens for AI responses.
        """
        self.max_tokens = 4096
        self.repo = repo
        self.ai = AIGateway()

    async def get_task_plan(self, instruction, file_list, original_prompt_language):
        """
        Get a development plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for task planning.
            file_list (list): List of available files.
            original_prompt_language (str): The language of the original prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `TaskPlanner` is initiating the process to generate a task plan")
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a principal engineer specializing in Pyramid architecture. Generate an ordered list of task groups for implementing a system based on the user's instruction and provided file list.\n\n"
                    "Guidelines:\n"
                    "1. Only include files from the provided `file_list`.\n"
                    "2. Each group should contain tasks that are completely independent and can be worked on concurrently without any context from each other.\n"
                    "3. Strictly enforce separation of concerns. Files that need context from others (e.g., main files, style files, script files) must never be in the same group.\n"
                    "4. Order groups following Pyramid architecture principles, ensuring each group provides necessary context for subsequent groups.\n"
                    "5. Provide `file_name` (full path) and `techStack` for each task.\n"
                    "6. Omit configuration, dependencies, and non-essential files.\n"
                    "7. Exclude all image files except `.svg` and all audio asset files.\n"
                    "8. For each tech stack or file type, create a separate group for a 'lead' file that others can mimic. The lead file should be the main file that is most important and contains much context for other files in the same group to follow. For example, in the UI layer, the lead file could be `main.html`, which defines the overall structure, while other HTML files mimic its structure. In the logic layer, `main_controller.py` could serve as the lead file that other controllers follow for consistency.\n"
                    "9. Apply the 'lead file' principle to all tech stacks, including SVG icons.\n"
                    "10. All style-related files (CSS, SCSS, etc.) must be in the penultimate group.\n"
                    "11. All SVG files must be strictly grouped together in the last group, without exception.\n"
                    "12. Critically analyze dependencies between files. If file A depends on file B, ensure B is implemented before A, even if it means separating them into different groups.\n"
                    "13. The order of tasks and groups is crucial. Always prioritize providing necessary context for subsequent tasks.\n"
                    "14. Each file should appear only once in the entire plan. Ensure correct ordering to avoid repetition.\n"
                    "Response Format:\n"
                    "{\n"
                    '    "groups": [\n'
                    '        {\n'
                    '            "group_name": "",\n'
                    '            "tasks": [\n'
                    '                {\n'
                    '                    "file_name": "/full/path/to/file.py",\n'
                    '                    "techStack": "python"\n'
                    '                }\n'
                    '            ]\n'
                    '        },\n'
                    '        {\n'
                    '            "group_name": "",\n'
                    '            "tasks": [\n'
                    '                {\n'
                    '                    "file_name": "/full/path/to/file.html",\n'
                    '                    "techStack": "html"\n'
                    '                }\n'
                    '            ]\n'
                    '        }\n'
                    '    ]\n'
                    "}\n\n"
                    f"Current working project is {self.repo.get_repo_path()}\n\n"
                    "Return only valid JSON without additional text or formatting."
                )
            },
            {
                "role": "user",
                "content": f"Create a grouped task list and an ordered list of groups following Pyramid architecture. Only select files from this list:\n{file_list}\n\nStrictly group only tasks that are completely independent and can be executed without any knowledge of other files' configurations or contents. Enforce a strong separation between files that need context from others (e.g., main files, style files, script files) - these must always be in separate groups. Additionally, strengthen the lead-follow principle by ensuring each group has a clearly defined lead file that other files within the group follow. For example, in the UI layer, designate a main HTML file (e.g., `main.html`) as the lead, which outlines the overall structure, while other HTML files mimic its structure for consistency. In the logic layer, use a primary controller file (e.g., `main_controller.py`) as the lead, guiding the structure and conventions for other controllers.\n\nOrder the groups to ensure each group, when completed, provides necessary context for the next group's execution, adhering strictly to Pyramid architecture principles. For website-related tasks, always order groups as HTML first, then JavaScript, then CSS, with SVG files as the very last group. For other tech stacks, apply similar principles (e.g., database schema files before API route files in a backend system). Never group files of different tech stacks together. Within each group, order tasks based on their internal dependencies, if any. Include `file_name` (full path) and `techStack` for each task in JSON format. Ensure correct paths. For each tech stack or file type, create a separate group for a 'lead' file that others can mimic. The lead file should be the main file that is most important and contains much context for other files in the same group to follow and take advantage of. Apply this 'lead file' principle to all tech stacks, including SVG icons. All style-related files (CSS, SCSS, etc.) must be in the penultimate group, and SVG icons must always be in the very last group. Critically analyze dependencies between files and ensure that if file A depends on file B, B is always implemented before A, even if it requires separating them into different groups. The order of tasks and groups is of utmost importance to provide the necessary context for subsequent tasks. Each file should be included only once in the entire plan, ensuring correct ordering to avoid repetition. Original instruction: {instruction}\n\n"
            }
        ]

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### The `TaskPlanner` has successfully generated the task plan")
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### The `TaskPlanner` has repaired and processed the JSON response")
            return plan_json
        except Exception as e:
            logger.error(f" #### The `TaskPlanner` encountered an error while generating the task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction, file_lists, original_prompt_language):
        """
        Get development plans based on the user's instruction.

        Args:
            instruction (str): The user's instruction for task planning.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `TaskPlanner` is generating task plans")
        plan = await self.get_task_plan(instruction, file_lists, original_prompt_language)
        logger.debug("\n #### The `TaskPlanner` has completed generating the task plans")
        return plan