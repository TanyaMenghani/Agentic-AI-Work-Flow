from typing import Optional, List
from pydantic import BaseModel, EmailStr

# Replace this import with the MCP client you are actually using
# The name varies depending on your MCP SDK
from mcp import MCPClient


# -------- Schema for sending (STRICT) --------
class SendEmail(BaseModel):
    to: EmailStr
    subject: str
    body: str
    attachments: List[str] = []
    approved: bool = False


class EmailSendError(Exception):
    pass


# -------- MCP Wrapper --------
class GmailMCP:
    """
    Thin Gmail MCP wrapper.
    No LLM. No drafting. No safety guessing.
    """

    def __init__(self, server_url: str):
        self.client = MCPClient(server_url=server_url)

    def send(self, email: SendEmail) -> dict:
        """
        Send email via Gmail MCP.

        HARD RULE:
        - approved MUST be True
        """

        if not email.approved:
            raise EmailSendError(
                "Email not approved. Refusing to send."
            )

        if not email.subject.strip():
            raise EmailSendError("Subject cannot be empty.")

        if not email.body.strip():
            raise EmailSendError("Body cannot be empty.")

        payload = {
            "to": email.to,
            "subject": email.subject,
            "body": email.body,
            "attachments": email.attachments,
        }

        return self.client.call_tool(
            tool_name="send_email",
            arguments=payload
        )
