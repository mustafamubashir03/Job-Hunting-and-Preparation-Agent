import os
import dotenv

dotenv.load_dotenv()

from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

resume = TextFileKnowledgeSource(
    file_path=["resume.txt"]
)

print("Created successfully")