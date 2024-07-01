import openai
import pandas as pd

# Read the Excel file
mb = pd.read_excel('Mood board.xlsx')

# Extract the column containing sentences
con = mb.iloc[:, 6]

# Initialize OpenAI API
openai.api_key = "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"
completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a bot to extract keywords from sentences."},
                {"role": "user", "content": "do you know what is love"}]
        )
print(completion.choices[0].message.content)
# Function to abstract keywords from text using OpenAI's GPT-3
# def abstract(text):
#     try:
#         completion = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a bot to extract keywords from sentences."},
#                 {"role": "user", "content": text}]
#         )
#         return completion.choices[0].message.content
#     except Exception as e:
#         print(f"Error processing text: {text}. Error: {e}")
#         return ""
#
# # Process each sentence and store the results
# res = [abstract(sentence) for sentence in con]
#
# # Create a DataFrame from the results
# new_df = pd.DataFrame(res)
#
# # Print and save the DataFrame to a CSV file
# print(new_df)
# with open('result.csv', mode='a', newline='') as file:
#     new_df.to_csv(file, header=False, index=False)
