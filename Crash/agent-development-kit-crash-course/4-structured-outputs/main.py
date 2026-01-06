from email_agent.Rootagent import RootAgent

root = RootAgent(gmail_server_url="http://localhost:3333")

result = root.run(
    user_prompt="Write a polite follow-up email after an interview",
    recipient="hr@company.com",
    approved=False,  # must be explicitly flipped
)

print(result)
