from agent import email_making_agent
from mcp import GmailMCP, SendEmail


class RootAgent:
    """
    Root orchestrator.
    - Coordinates drafting and sending
    - Holds system configuration
    - NO LLM creativity
    """

    def __init__(self, gmail_server_url: str):
        self.gmail = GmailMCP(gmail_server_url)

    def run(
        self,
        user_prompt: str,
        to: str,
        approved: bool = False,
    ):
        """
        user_prompt : instruction for drafting the email
        to          : recipient email address
        approved    : MUST be True to send
        """

        # 1. Generate draft (LLM call)
        draft_result = email_making_agent.run(user_prompt)
        email = draft_result["email"]

        # 2. If not approved, stop here
        if not approved:
            return {
                "status": "draft_only",
                "subject": email.subject,
                "body": email.body,
            }

        # 3. Send email via MCP
        send_request = SendEmail(
            to=to,
            subject=email.subject,
            body=email.body,
            approved=True,  # explicit gate
        )

        return self.gmail.send(send_request)
