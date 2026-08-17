## Project Structure

```text
customer-support-ai/
│
├── agents/
│   ├── intent_agent.py
│   ├── order_agent.py
│   ├── refund_agent.py
│   ├── payment_agent.py
│   ├── technical_support_agent.py
│   ├── faq_agent.py
│   ├── escalation_agent.py
│   └── email_agent.py
│
├── services/
│   ├── llm_service.py
│   ├── memory_service.py
│   ├── logging_service.py
│   ├── rag_service.py
│   ├── gmail_service.py
│   └── voice_service.py
│
├── data/
│   ├── company_policy.txt
│   ├── refund_policy.txt
│   └── shipping_policy.txt
│
├── knowledge_base/
│   ├── company_policy.pdf
│   ├── refund_policy.pdf
│   └── shipping_policy.pdf
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── test_intent.py
├── test_gmail.py
├── test_email_agent.py
├── test_voice.py
└── test_api_key.py