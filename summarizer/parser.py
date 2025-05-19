def parse_chat(lines):
    user_msgs, ai_msgs = [], []

    for line in lines:
        if line.startswith("User:"):
            user_msgs.append(line[5:].strip())
        elif line.startswith("AI:"):
            ai_msgs.append(line[3:].strip())

    return user_msgs, ai_msgs
