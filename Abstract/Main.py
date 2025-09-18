'''
##DEVELOPER NOTES##

# Fix the algebraic equations
nopip2010: solve x x = 80 - 80
The solution is x = 80.0

Do something with sentiment analysis
-> make it reply based off sentiment
 
add in comments and docstrings
 
stop text to speech saying abstract 1.7

re add in the debug feature of linking keywords
##DEVEVELOPER NOTES##

Project:

Project Name: Abstract chatbot

Abstract is a chatbot designed to converse with users on a wide
array of topics. Abstract was origionally designed in 2022 and has
since been developed into a more robust system.
 
DEVELOPER: Noah Lockley
Version: 1.7

'''

import random
import re
from ext_responses import greetings, goodbyes, questions, other_responses



class ChatbotParams:
    def __init__(self):
        self.model_name = 'Abstract 1.7'
        self.texttospeech = False
        self.sentiment_analysis = False
        self.knowledge_gap_filler = False
        self.feedback_and_ideas = False
        self.filename = "database.txt"
        self.feedback_filename = "feedback_abstract.txt"
        self.idea_filename = "ideas.txt"
        self.banned_users_filename = "banned_users.txt"
        self.Chatlogs_filename = "Chatlogs.txt"
        self.username_filename = "usernames.txt"
        self.rude_words_filename = "rude_words.txt"
        self.feedback_interval = 15
        self.idea_interval = 13
        self.interaction_count = 0
        self.mode = 'debug'

class DataLoader:
    @staticmethod
    def load_data(filename):
        try:
            with open(filename, "r", encoding='utf-8', errors='ignore') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"The file '{filename}' does not exist.")
            return []

    @staticmethod
    def load_responses(filename):
        data = DataLoader.load_data(filename)
        keywords, responses = [], []
        for line in data:
            if ':' in line:
                keyword, response = line.split(":", 1)
                keywords.append(keyword.strip())
                responses.append(response.strip())
        return keywords, responses

class DataSaver:
    @staticmethod
    def save_data(filename, data):
        with open(filename, "w", encoding='utf-8', errors='ignore') as file:
            for item in data:
                file.write(f"{item}\n")

    @staticmethod
    def save_responses(filename, keywords, responses):
        with open(filename, "w", encoding='utf-8', errors='ignore') as file:
            for keyword, response in zip(keywords, responses):
                file.write(f"{keyword}:{response}\n")

    @staticmethod
    def append_data(filename, data):
        with open(filename, "a", encoding='utf-8', errors='ignore') as file:
            file.write(f"{data}\n")

class ChatbotUtils:
    @staticmethod
    def check_rudeness(word, rude_words):
        return word.lower() in rude_words

    @staticmethod
    def is_known_question(question, responses):
        return question in responses

    @staticmethod
    def perform_calculation(query):
        try:
            return str(eval(query))
        except:
            return None

    @staticmethod
    def solve_algebra(user_input):
        pattern = r"(-?\d*)x\s*([+-]?\s*\d*)\s*=\s*(-?\d+)"
        match = re.search(pattern, user_input.replace(' ', ''))
        
        if match:
            a = int(match.group(1)) if match.group(1) and match.group(1) != "-" else 1
            b = int(match.group(2).replace(' ', '').replace('+', '')) if match.group(2) else 0
            c = int(match.group(3))
            
            if a == 0:
                return "infinite solutions" if b == c else "no solution"
            else:
                x = (c - b) / a
                return f"The solution is x = {x}"
        else:
            return "Sorry, I couldn't understand the equation format. Please use 'ax + b = c'."

    @staticmethod
    def text_to_speech(text):
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()

    @staticmethod
    def sentiment_analysis(text):
        from textblob import TextBlob
        blob = TextBlob(text)
        # --> add sentiment analysis code here

class Chatbot:
    def __init__(self):
        self.params = ChatbotParams()
        self.keywords, self.responses = DataLoader.load_responses(self.params.filename)
        self.rude_words = DataLoader.load_data(self.params.rude_words_filename)
        self.ideas = DataLoader.load_data(self.params.idea_filename)
        self.banned_users = DataLoader.load_data(self.params.banned_users_filename)
        self.usernames = DataLoader.load_data(self.params.username_filename)

    def login(self):
        while True:
            print("Abstract may make mistakes \n")
            print("1. Log in with an existing username\n2. Create a new account")
            choice = input("Please choose an option (1/2): ")
            
            if choice == "1":
                username = input("Please enter your username: ").lower()
                if username == 'debug':
                    self.params.mode = 'debug'
                    print("Entered debugger mode")
                    return username
                elif username in self.usernames and username not in self.banned_users:
                    print(f"Access granted! Welcome, {username.title()} \n")
                    greeting = f"{self.params.model_name}: {random.choice(greetings)}"
                    print(greeting)
                    if self.params.texttospeech:
                        ChatbotUtils.text_to_speech(greeting)
                    return username
                elif username in self.banned_users:
                    print("Access denied! This username is banned. Please try a different username.")
                else:
                    print("Access denied! Invalid username. Please try again.")
            elif choice == "2":
                new_username = input("Please enter a new username: ").strip().lower()
                if new_username not in self.usernames and new_username not in self.banned_users:
                    self.usernames.append(new_username)
                    DataSaver.save_data(self.params.username_filename, self.usernames)
                    print(f"Account created successfully! Welcome, {new_username.title()}")
                    return new_username
                elif new_username in self.banned_users:
                    print("Access denied! This username is banned. Please try a different username.")
                else:
                    print("Username already exists. Please choose a different username.")
            else:
                print("Invalid input. Please enter a valid option.")

    def process_input(self, parsed_user_input, username):
        if parsed_user_input[0] == "calculate":
            calculation_query = user_input[9:].strip()
            result = ChatbotUtils.perform_calculation(calculation_query)
            return f"The result is {result}" if result else "Sorry, I couldn't perform that calculation."

        elif any(phrase in parsed_user_input for phrase in ["whats x", "find x", "solve x"]):
            return ChatbotUtils.solve_algebra(user_input)

        elif "give me an idea" in parsed_user_input or "i need ideas" in parsed_user_input:
            if self.ideas:
                idea = random.choice(self.ideas)
                self.ideas.remove(idea)
                return f"Here's an idea for you: {idea}"
            return "I'm sorry, I don't have any ideas at the moment."

        elif parsed_user_input[0] == "copy me" or parsed_user_input[0] == "repeat after me":
            text_to_repeat = re.sub(r"^(copy me|repeat after me)", "", user_input, flags=re.IGNORECASE).strip()
            return f"{self.params.model_name}: {text_to_repeat}"

        # Collect matching responses
        matching_responses = []

        for keyword, response in zip(self.keywords, self.responses):
            if keyword.lower() in parsed_user_input:  # Check if the keyword is in the user input
                matching_responses.append(response)

        # Debugging: Print all matching responses if in debug mode
        if self.params.mode == 'debug':
            print("Matching responses:", matching_responses)

        # Return a random response from all matching responses, or a default response if none found
        if matching_responses:
            return f"{self.params.model_name}: {random.choice(matching_responses)}"

        

    def run(self):
        username = self.login()
        user_input = input(f"{username}: ").lower()
        parsed_user_input = user_input.split()
        
        print(parsed_user_input)
        while user_input not in ["bye", "goodbye", "night", "i have to go", "i have to go now", "night night", "exit", "leave", "goodnight"]:
            if username in self.banned_users:
                print("You have been banned for using inappropriate language. Logging out...")
                break

            for word in user_input.split():
                if ChatbotUtils.check_rudeness(word, self.rude_words):
                    print("I'm sorry, but that language is not appropriate. You have been banned.")
                    self.banned_users.append(username)
                    DataSaver.save_data(self.params.banned_users_filename, self.banned_users)
                    return

            if self.params.sentiment_analysis:
                sentiment = ChatbotUtils.sentiment_analysis(user_input)
                if sentiment < -0.1:
                    print(f"{self.params.model_name}: This seems negative (polarity: {sentiment:.2f})")
                elif sentiment > 0.1:
                    print(f"{self.params.model_name}: This seems positive (polarity: {sentiment:.2f})")
                else:
                    print(f"{self.params.model_name}: This seems neutral (polarity: {sentiment:.2f})")

            response = self.process_input(parsed_user_input, username)

            if response:
                print(response)
                if self.params.texttospeech:
                    ChatbotUtils.text_to_speech(response)
                DataSaver.append_data(self.params.Chatlogs_filename, f"{username}:{user_input}:{response}")
            else:
                print("I don't know that. What are the important keywords in your input?")
                while True or self.params.mode == 'debug' and user_input == 'know$$debug':
                    user_keywords = input("Please type a keyword (or 'no' to finish): ")
                    if user_keywords.lower() == 'no':
                        break
                    new_response = input(f"How should I respond to '{user_keywords}'? ")
                    self.keywords.append(user_keywords)
                    self.responses.append(new_response)

                DataSaver.save_responses(self.params.filename, self.keywords, self.responses)
                print("Keywords and responses saved!")
                response = f"{self.params.model_name}: {random.choice(questions)}"
                print(response)
                if self.params.texttospeech:
                    ChatbotUtils.text_to_speech(response)

            if self.params.feedback_and_ideas:
                self.handle_feedback_and_ideas()

            self.params.interaction_count += 1
            user_input = input(f"{username}: ").lower()
            
            
        goodbye_message = random.choice(goodbyes)
        print(goodbye_message)
        if self.params.texttospeech:
            ChatbotUtils.text_to_speech(goodbye_message)

    def handle_feedback_and_ideas(self):
        if self.params.interaction_count % self.params.feedback_interval == 0:
            feedback_choice = input("Do you have feedback regarding the function of this chatbot? (yes/no): ")
            if feedback_choice.lower() == "yes":
                feedback = input("Please provide any feedback: ")
                DataSaver.append_data(self.params.feedback_filename, feedback)
                print("Thank you for your feedback!")

        if self.params.interaction_count % self.params.idea_interval == 0:
            idea_choice = input("Do you have any creative/random ideas or concepts that might inspire people? (yes/no): ")
            if idea_choice.lower() == "yes":
                idea = input("Please share your idea: ")
                self.ideas.append(idea)
                DataSaver.save_data(self.params.idea_filename, self.ideas)
                print("Thank you for your idea!")

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.run()


