import re
abc = """
Step1: Find the file path for supporting phone login:

```python
'lib/assets/.keep'
```

Step2:
```json
[
    {
        "INPUT": "I need support phone login",
        "FULL_PATH_FILE": "lib/assets",
        "OUTPUTS": [
            "STEP1: Open the file login.py",
            "STEP2: Locate the login function",
            "STEP3: Add a new argument to the login function for phone number",
            "STEP4: Implement phone number validation logic",
            "STEP5: Update the authentication logic to support phone number login"
        ]
    }
]
```
"""
# json_string = re.search(r'json\n(.*)’, abc, re.DOTALL).group(1)

json_content_match = re.search(r"```json(.*?)```", abc, re.DOTALL)
print(json_content_match.group(1).strip())
