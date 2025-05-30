from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

# Email details
sender_email = os.getenv('SENDER_MAIL')
password = os.getenv('SMTP_PASSWORD')  # Use an app password, not your actual email password

# Initialize FastMCP server
mcp = FastMCP("mail sender")


def send_email_definition(receiver_email: str, subject: str, body: str) -> None:
    """Send a plain text email using smtplib and EmailMessage."""

    if not sender_email or not password:
        raise EnvironmentError("Missing SENDER_MAIL or SMTP_PASSWORD in .env")

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


@mcp.tool()
async def send_email(receiver_email: str, subject: str, body: str) -> None:
    """Send an email to the receiver with the given subject and body."""
    # Since send_email_definition is sync, run it in a thread pool
    import asyncio
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, send_email_definition, receiver_email, subject, body)


#run the server
if __name__ == "__main__":
    transport = "stdio"
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")