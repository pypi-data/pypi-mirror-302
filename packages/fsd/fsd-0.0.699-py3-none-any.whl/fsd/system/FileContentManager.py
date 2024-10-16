import re
import aiofiles
import os
import mimetypes
from typing import List, Tuple
from fsd.log.logger_config import get_logger
import PyPDF2
import docx
import chardet
import openpyxl
logger = get_logger(__name__)

class FileContentManager:
    @staticmethod
    async def read_file(file_path: str) -> str:
        """
        Read and return the content of any type of file asynchronously, including special files like PDFs,
        DOCs, XLSX, and all code file types.

        Args:
            file_path (str): Full path to the file.

        Returns:
            str: Content of the file or empty string if file doesn't exist or can't be read.
        """
        if not os.path.exists(file_path):
            logger.error(f"File does not exist: {file_path}")
            return ""

        mime_type, _ = mimetypes.guess_type(file_path)

        try:
            # Handle PDF files
            if mime_type == 'application/pdf':
                async with aiofiles.open(file_path, 'rb') as file:
                    content = await file.read()
                pdf_reader = PyPDF2.PdfReader(content)
                text_content = []
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                return '\n'.join(text_content)

            # Handle DOC and DOCX files
            elif mime_type in [
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            ]:
                async with aiofiles.open(file_path, 'rb') as file:
                    content = await file.read()
                doc = docx.Document(content)
                return '\n'.join(paragraph.text for paragraph in doc.paragraphs)

            # Handle XLSX (Excel) files
            elif mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                async with aiofiles.open(file_path, 'rb') as file:
                    content = await file.read()
                workbook = openpyxl.load_workbook(content, data_only=True)
                sheet = workbook.active  # Read the first sheet
                data = []
                for row in sheet.iter_rows(values_only=True):
                    data.append('\t'.join([str(cell) if cell is not None else "" for cell in row]))
                return '\n'.join(data)

            # Handle text and code files
            else:
                # Attempt to read as UTF-8 first
                try:
                    async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
                        return await file.read()
                except UnicodeDecodeError:
                    # If UTF-8 fails, detect encoding
                    async with aiofiles.open(file_path, 'rb') as file:
                        raw_data = await file.read()
                    detected = chardet.detect(raw_data)
                    encoding = detected['encoding'] if detected['encoding'] else 'utf-8'
                    async with aiofiles.open(file_path, 'r', encoding=encoding, errors='replace') as file:
                        return await file.read()

        except Exception as e:
            logger.exception(f"Failed to read file {file_path}: {e}")
            return ""

    @staticmethod
    async def write_file(file_path: str, content: str):
        """Write content to the file asynchronously."""
        try:
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.debug(f" #### The `file manager agent` has created a new directory: `{directory}` for the file: `{file_path}`")
            
            async with aiofiles.open(file_path, 'w') as file:
                await file.write(content)
            
            if not os.path.exists(file_path):
                logger.debug(f" #### The `file manager agent` has successfully created a new file: `{file_path}`")
            else:
                logger.debug(f" #### The `file manager agent` has successfully updated the file: `{file_path}`")
        except Exception as e:
            logger.error(f" #### The `file manager agent` encountered an error while writing to file `{file_path}`. Error details: `{e}`")

    @staticmethod
    def parse_search_replace_blocks(response: str) -> List[Tuple[str, str]]:
        """
        Parses a response string for single or multiple SEARCH/REPLACE blocks,
        returning search and replace content as tuples. Handles both cases correctly.
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
            # Strip any extra spaces or newlines for cleanliness
            search = search
            replace = replace

            # Append the search and replace blocks as a tuple
            blocks.append((search, replace))

        return blocks

    @classmethod
    async def apply_changes(cls, file_path: str, blocks: List[Tuple[str, str]]) -> str:
        """Apply the changes from SEARCH/REPLACE blocks to the file content."""
        content = await cls.read_file(file_path)
        for search, replace in blocks:
            if search:
                if search not in content:
                    logger.error(f" #### The `file manager agent` couldn't find a match for search block in file: `{file_path}`")
                    continue
                content = content.replace(search, replace)
            else:
                content += f"\n{replace}"
        logger.debug(f" #### The `file manager agent` has successfully applied changes to the content of file: `{file_path}`")
        return content

    @classmethod
    async def process_coding_agent_response(cls, file_path: str, coding_agent_response: str):
        """Process the coding agent response and automatically apply changes to the file."""
        blocks = cls.parse_search_replace_blocks(coding_agent_response)
        if not blocks:
            logger.error(f" #### The `file manager agent` found no valid SEARCH/REPLACE blocks in the coding agent response for file: `{file_path}`")
            return

        new_content = await cls.apply_changes(file_path, blocks)
        await cls.write_file(file_path, new_content)
        logger.debug(f" #### The `file manager agent` has automatically applied changes to file: `{file_path}`")

    @classmethod
    async def handle_coding_agent_response(cls, file_path: str, coding_agent_response: str):
        """Main method to handle coding agent responses and automatically manage code changes for a single file."""
        logger.debug(coding_agent_response)
        try:
            await cls.process_coding_agent_response(file_path, coding_agent_response)
            logger.debug(f" #### The `file manager agent` has successfully processed the coding agent response for file: `{file_path}`")
        except Exception as e:
            logger.error(f" #### The `file manager agent` encountered an error while processing the coding agent response for file `{file_path}`. Error details: `{e}`")