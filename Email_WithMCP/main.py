from agent import root_agent

root = root_agent(gmail_server_url="http://localhost:3333")

result = root.run(
    user_prompt="Write a polite follow-up email after an interview",
    recipient="tanya5menghani@gmail.com",
    approved=True,
)

print(result)
