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
      "name": "github_search_code",
      "description": "Searches a GitHub repository for files matching a code query. The query can contain function names, class names, variable names, imports, filenames, keywords, or code snippets. Returns matching file paths and metadata so the assistant can inspect the relevant files.",
      "parameters": {
        "type": "object",
        "properties": {
          "owner": {
            "type": "string",
            "description": "GitHub repository owner."
          },
          "repo": {
            "type": "string",
            "description": "Repository name."
          },
          "query": {
            "type": "string",
            "description": "GitHub code search query."
          }
        },
        "required": [
          "owner",
          "repo",
          "query"
        ]
      }
    }
},

{
  "type": "function",
  "function": {
    "name": "notion_add_row_database",
    "description": "Create a new row in a Notion database. The AI should provide only the column values. The backend will convert them to the correct Notion property format using the database schema.",
    "parameters": {
      "type": "object",
      "properties": {
        "database_id": {
          "type": "string"
        },
        "values": {
          "type": "object",
          "description": "Dictionary mapping database column names to their values. Example: {\"Order\":\"#1024\",\"Customer\":\"John Doe\",\"Total\":42.5,\"Paid\":true}"
        }
      },
      "required": [
        "database_id",
        "values"
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