import re
import aiofiles
import os
import unicodedata
from typing import List, Tuple
import logging
import difflib

class FileContentManager:
    def __init__(self, repo):
        self.repo = repo
        # Configure the logger to write to the specified log file
        log_file_path = os.path.join(self.repo.get_repo_path(), 'log1.txt')
        # Ensure the directory exists
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        logging.basicConfig(
            filename=log_file_path,
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s:%(message)s'
        )
        self.logger = logging.getLogger(__name__)

    async def read_file(self, file_path: str) -> str:
        """Read the content of the file asynchronously with UTF-8 encoding."""
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
                content = await file.read()
            self.logger.debug(f"Successfully read the file: '{file_path}'")
            return content
        except FileNotFoundError:
            self.logger.error(f"File '{file_path}' not found. Returning an empty string.")
            return ""
        except Exception as e:
            self.logger.error(f"Error while reading file '{file_path}'. Error details: '{e}'")
            return ""

    async def write_file(self, file_path: str, content: str):
        """Write content to the file asynchronously with UTF-8 encoding."""
        try:
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
                self.logger.debug(f"Created a new directory: '{directory}' for the file: '{file_path}'")
            
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as file:
                await file.write(content)
            
            if not os.path.exists(file_path):
                self.logger.debug(f"Successfully created a new file: '{file_path}'")
            else:
                self.logger.debug(f"Successfully updated the file: '{file_path}'")
        except Exception as e:
            self.logger.error(f"Error while writing to file '{file_path}'. Error details: '{e}'")

    @staticmethod
    def parse_search_replace_blocks(response: str) -> List[Tuple[str, str]]:
        """
        Parses a response string for single or multiple SEARCH/REPLACE blocks,
        returning search and replace content as tuples.
        """
        # Regular expression pattern to capture multiple SEARCH/REPLACE blocks
        pattern = r'<<<<<<< SEARCH\n(.*?)=======\n(.*?)>>>>>>> REPLACE'
        # Find all matches in the response
        matches = re.findall(pattern, response, re.DOTALL)
        # Raise an error if no blocks are found
        if not matches:
            raise ValueError("No valid SEARCH/REPLACE blocks found in the input.")
        blocks = []
        for search, replace in matches:
            # Remove leading/trailing whitespace and normalize line endings
            search = search.strip().replace('\r\n', '\n')
            replace = replace.strip().replace('\r\n', '\n')
            # Append the search and replace blocks as a tuple
            blocks.append((search, replace))
        return blocks

    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text by standardizing encodings and whitespace."""
        # Normalize Unicode characters
        text = unicodedata.normalize('NFC', text)
        # Replace multiple whitespace characters with a single space
        text = re.sub(r'\s+', ' ', text)
        # Strip leading and trailing whitespace
        text = text.strip()
        return text

    async def apply_changes(self, file_path: str, blocks: List[Tuple[str, str]]) -> str:
        """Apply the changes from SEARCH/REPLACE blocks to the file content."""
        content = await self.read_file(file_path)

        for idx, (search, replace) in enumerate(blocks, 1):
            if search:
                # Normalize both the search block and the file content
                normalized_search = self.normalize_text(search)
                normalized_content = self.normalize_text(content)

                # Use difflib to find the closest match
                matcher = difflib.SequenceMatcher(None, normalized_content, normalized_search)
                match_ratio = matcher.ratio()
                self.logger.debug(f"Block {idx}: Similarity ratio is {match_ratio:.2f}")

                if match_ratio >= 0.8:  # You can adjust the threshold as needed
                    # Find the matching blocks
                    match = matcher.find_longest_match(0, len(normalized_content), 0, len(normalized_search))
                    if match.size > 0:
                        # Map the match back to the original content
                        start = content.find(search)
                        if start != -1:
                            end = start + len(search)
                            # Replace the matched text in the original content
                            content = content[:start] + replace + content[end:]
                            self.logger.info(
                                f"Block {idx}: Successfully replaced content in file: '{file_path}'\n"
                                f"Search Block:\n{search}\n"
                                f"Replace Block:\n{replace}\n"
                            )
                        else:
                            self.logger.error(
                                f"Block {idx}: Exact match not found after difflib matching in file: '{file_path}'\n"
                                f"Search Block:\n{search}\n"
                            )
                    else:
                        self.logger.error(
                            f"Block {idx}: No matching blocks found using difflib in file: '{file_path}'\n"
                            f"Search Block:\n{search}\n"
                        )
                else:
                    self.logger.error(
                        f"Block {idx}: Similarity ratio below threshold in file: '{file_path}'\n"
                        f"Similarity Ratio: {match_ratio:.2f}\n"
                        f"Search Block:\n{search}\n"
                    )
            else:
                # Handle new code additions
                content += f"\n{replace}"
                self.logger.info(
                    f"Block {idx}: Successfully added new content to file: '{file_path}'\n"
                    f"Added Block:\n{replace}\n"
                )

        return content

    async def process_coding_agent_response(self, file_path: str, coding_agent_response: str):
        """Process the coding agent response and automatically apply changes to the file."""
        try:
            blocks = self.parse_search_replace_blocks(coding_agent_response)
            if not blocks:
                self.logger.error(
                    f"No valid SEARCH/REPLACE blocks found in the coding agent response for file: '{file_path}'"
                )
                return

            new_content = await self.apply_changes(file_path, blocks)
            await self.write_file(file_path, new_content)
            self.logger.debug(f"Automatically applied changes to file: '{file_path}'")
        except Exception as e:
            self.logger.error(
                f"Encountered an error while processing the coding agent response for file '{file_path}'. "
                f"Error details: '{e}'"
            )

    async def handle_coding_agent_response(self, file_path: str, coding_agent_response: str):
        """Main method to handle coding agent responses and automatically manage code changes for a single file."""
        self.logger.debug("Processing coding agent response...")
        await self.process_coding_agent_response(file_path, coding_agent_response)
