from agents.email_agent import handle_email_query


question = "What are my latest emails?"

answer = handle_email_query(question)

print("\n========== AI EMAIL RESPONSE ==========\n")
print(answer)