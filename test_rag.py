from tools.rag_tool import search_knowledge_base

result = search_knowledge_base.invoke({
    "query": "flight cancel karne pe kitna refund milega"
})

print(result)