#GPT: how parse the abc by FULL_PATH_FILE item split the OUTPUTS , match the "Open the file" as one group

abc = [
  {
    "INPUT": "I need support phone login",
    "FULL_PATH_FILE": [
      "app/controllers/users_controller.rb",
      "app/models/user.rb",
      "config/routes.rb",
      "app/views/devise/registrations/new.html.erb"
    ],
    "OUTPUTS": [
      "STEP1: Open the file app/models/user.rb",
      "STEP2: Add a new field to the User model for phone number",
      "STEP3: Implement validation logic for phone number in the User model",
      "STEP4: Open the file app/controllers/users_controller.rb",
      "STEP5: Locate the create action in the UsersController to handle signup",
      "STEP6: Update the create action to accept and save phone number",
      "STEP7: Open the file config/routes.rb",
      "STEP8: Update the routes file to include phone-based signup routes if necessary",
      "STEP9: Open the file app/views/devise/registrations/new.html.erb",
      "STEP10: Add a new input field for phone number in the signup form",
      "STEP11: Test the signup process to ensure phone number is being saved and validated correctly",
      "STEP12: Open the file app/controllers/sessions_controller.rb",
      "STEP13: Locate and update the login function to accept and authenticate using a phone number"
    ]
  }
]

# Function to parse the OUTPUTS based on FULL_PATH_FILE
def parse_outputs(abc):
    result = {}
    for item in abc:
        full_path_files = item['FULL_PATH_FILE']
        outputs = item['OUTPUTS']

        current_file = None
        steps = []

        for output in outputs:
            if "Open the file" in output:
                if current_file:
                    result[current_file] = steps
                current_file = output.split("Open the file ")[1]
                steps = [output]
            else:
                if current_file:
                    steps.append(output)

        if current_file:
            result[current_file] = steps

    return result

# Parse the OUTPUTS
parsed_outputs = parse_outputs(abc)

# Print the result
#for file, steps in parsed_outputs.items():
#    print(f"File: {file}")
#    for step in steps:
#        print(f"  {step}")

        #print()  # For better readability
# File: app/models/user.rb
#   STEP1: Open the file app/models/user.rb
#   STEP2: Add a new field to the User model for phone number
#   STEP3: Implement validation logic for phone number in the User model
# File: app/controllers/users_controller.rb
#   STEP4: Open the file app/controllers/users_controller.rb
#   STEP5: Locate the create action in the UsersController to handle signup
#   STEP6: Update the create action to accept and save phone number
# File: config/routes.rb
#   STEP7: Open the file config/routes.rb
#   STEP8: Update the routes file to include phone-based signup routes if necessary
# File: app/views/devise/registrations/new.html.erb
#   STEP9: Open the file app/views/devise/registrations/new.html.erb
#   STEP10: Add a new input field for phone number in the signup form
#   STEP11: Test the signup process to ensure phone number is being saved and validated correctly
# File: app/controllers/sessions_controller.rb
#   STEP12: Open the file app/controllers/sessions_controller.rb
#   STEP13: Locate and update the login function to accept and authenticate using a phone number
#
# print(parsed_outputs)

# {'app/models/user.rb': ['STEP1: Open the file app/models/user.rb', 'STEP2: Add a new field to the User model for phone number', 'STEP3: Implement validation logic for phone number in the User model'], 'app/controllers/users_controller.rb': ['STEP4: Open the file app/controllers/users_controller.rb', 'STEP5: Locate the create action in the UsersController to handle signup', 'STEP6: Update the create action to accept and save phone number'], 'config/routes.rb': ['STEP7: Open the file config/routes.rb', 'STEP8: Update the routes file to include phone-based signup routes if necessary'], 'app/views/devise/registrations/new.html.erb': ['STEP9: Open the file app/views/devise/registrations/new.html.erb', 'STEP10: Add a new input field for phone number in the signup form', 'STEP11: Test the signup process to ensure phone number is being saved and validated correctly'], 'app/controllers/sessions_controller.rb': ['STEP12: Open the file app/controllers/sessions_controller.rb', 'STEP13: Locate and update the login function to accept and authenticate using a phone number']}

## AND ===== Other ！！！

dicts = [{'INPUT': 'I need support phone login', 'FULL_PATH_FILE': 'app/controllers/users_controller.rb', 'OUTPUTS': ['STEP1: Open the file app/controllers/users_controller.rb', 'STEP2: Locate the login function', 'STEP3: Add a new argument to the login function for phone number', 'STEP4: Implement phone number validation logic', 'STEP5: Update the authentication logic to support phone number login']},
{'INPUT': 'Create an admin dashboard', 'FULL_PATH_FILE': 'app/controllers/users_controller.rb', 'OUTPUTS': ['STEP1: Open the file app/controllers/users_controller.rb', 'STEP2: Design the layout and structure of the admin dashboard', 'STEP3: Implement backend logic to gather necessary data for the dashboard', 'STEP4: Update the frontend to display data in an intuitive way', 'STEP5: Ensure secure access to the admin dashboard']},
{'INPUT': 'Enable multi-language support', 'FULL_PATH_FILE': 'config/initializers/inflections.rb', 'OUTPUTS': ['STEP1: Open the file config/initializers/inflections.rb', 'STEP2: Add a new setting for user language preference', 'STEP3: Integrate a translation library to handle multiple languages', 'STEP4: Update the frontend to allow users to select their preferred language', 'STEP5: Ensure all UI text is translatable by externalizing strings']}]

for item in dicts:
    print(item['INPUT'])

task_stri="""
```json
[{
  "INPUT": "I need support phone login",
  "FULL_PATH_FILE": "app/controllers/users_controller.rb",
  "OUTPUTS": [
    "STEP1: Open the file app/controllers/users_controller.rb",
    "STEP2: Locate the function handling user sign up",
    "STEP3: Add new fields and logic to the sign-up function to support phone number",
    "STEP4: Implement phone number validation logic",
    "STEP5: Update the user model (app/models/user.rb) to include phone number",
    "STEP6: Update the frontend to include phone number input for sign-up",
    "STEP7: Modify backend and database migration files if necessary to support phone number"
  ]
}]
```
"""
json_stri = task_stri.split("```json")[1].split("```")[0].strip()
print(json_stri)
