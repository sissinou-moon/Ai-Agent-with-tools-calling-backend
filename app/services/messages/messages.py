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
    "name": "github_get_user_repositories",
    "description": "Retrieves all GitHub repositories connected by the authenticated user from the application's database. Returns the repository owner, repository name, and any metadata needed for subsequent GitHub operations. The assistant should call this tool before searching code when the target repository is unknown.",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "string",
          "description": "Authenticated user's unique ID."
        }
      },
      "required": [
        "user_id"
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
        "app": {
            "type": "string",
            "value": "Notion"
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