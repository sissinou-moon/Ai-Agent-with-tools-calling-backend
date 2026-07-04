from app.schemas.messages import MessageRequest
from uuid import UUID
import ollama 
import json

TOOLS = [

{
    "type": "function",
    "function": {
        "name": "get_business_events",
        "description": (
            "Query ONLY the PostgreSQL events table. "
            "The database contains one table called 'events'. "
            "Columns: id, type, created_at, user_id, source, data(JSONB). "
            "Generate a complete PostgreSQL SELECT query."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string"
                }
            },
            "required": ["query"]
        }
    }
},

{
    "type": "function",
    "function": {
        "name": "github_list_pull_requests",
        "description": "List pull requests from a GitHub repository.",
        "parameters": {
            "type": "object",
            "properties": {
                "repository": {
                    "type": "string"
                },
                "state": {
                    "type": "string",
                    "enum": ["open", "closed", "all"]
                }
            },
            "required": ["repository"]
        }
    }
},

{
    "type": "function",
    "function": {
        "name": "notion_add_row_database",
        "description": "Create a new row (page) inside a Notion database. The properties object must match the database schema.",
        "parameters": {
            "type": "object",
            "properties": {
                "database_id": {
                    "type": "string"
                },
                "properties": {
                    "type": "object"
                }
            },
            "required": [
                "database_id",
                "properties"
            ]
        }
    }
},

{
    "type": "function",
    "function": {
        "name": "notion_list_databases",
        "description": "List all databases the user has access to in Notion. Use this whenever you need to locate a database by its name before adding, updating, or querying rows.",
    }
},

{
    "type": "function",
    "function": {
        "name": "notion_get_database_schema",
        "description": "Retrieve the properties (columns), property types, and available select options for a Notion database. Use this before creating a new row if you do not already know the database schema.",
        "parameters": {
            "type": "object",
            "properties": {
                "database_id": {
                    "type": "string"
                },
            },
            "required": [
                "database_id"
            ]
        }
    }
},

{
    "type": "function",
    "function": {
        "name": "gmail_send_email",
        "description": "Send an email.",
        "parameters": {
            "type": "object",
            "properties": {
                "recipient": {
                    "type": "string"
                },
                "subject": {
                    "type": "string"
                },
                "body": {
                    "type": "string"
                }
            },
            "required": [
                "recipient",
                "subject",
                "body"
            ]
        }
    }
}

]

class MessageService:

    def __init__(self):
        pass

    async def message(self, user_id: UUID, body: MessageRequest, conversation_id: str):

        response = ollama.chat(
            model='qwen3:8b',
            messages=[
                {'role': 'user', 'content': body.message}
            ],
            keep_alive=600000,
            tools=TOOLS
        )

        return response["message"]