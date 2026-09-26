from ai.agent import classify_input


test_inputs = [
    "Explain what machine learning is.",
    "Analyze this image.",
    "What does my uploaded document say?",
    "Search for the latest weather information."
]


print("\n===== ARGUS AGENT ROUTER TEST =====\n")

for user_input in test_inputs:
    category = classify_input(user_input)

    print("Input:", user_input)
    print("Category:", category)
    print("-" * 50)