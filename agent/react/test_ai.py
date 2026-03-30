import re



match = re.search(r"\w+\[(.*?)\]", text, re.DOTALL)
return match.group(1) if match else ""