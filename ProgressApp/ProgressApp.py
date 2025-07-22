class Goal:
    def __init__(self,title,description,deadline):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.progress = 0

print("Welcome to the Progress App!")
users_list = []

def createUsers(first_name, last_name, email, password):
    user = {
        "first_name" : first_name,
        "last_name" : last_name,
        "email" : email,
        "password" : password
    }
    users_list.append(user)
    print(f"User {first_name} {last_name} created successfully.")

def getUsers():
    return users_list

def askQuestion(question):
    print(question)
    answer = input("Your answer: ")
    return answer

def main():
    print("Whats your first name?")
    first_name = input("First Name: ")
    print("Whats your last name?")
    last_name = input("Last Name: ")

    createUsers(first_name, last_name, first_name.lower() + last_name.lower() + "@example.com", "password123")

    print("Whats your goal?")
    goal_title = input("Goal Title: ")
    print("Describe your goal:")
    goal_description = input("Goal Description: ")
    print("In how many days do you want to achieve this goal?")
    goal_deadline = input("Goal Deadline (in days): ")

    goal = Goal(goal_title, goal_description, goal_deadline)
    print(f"Goal '{goal.title}' created with description: '{goal.description}' and deadline: {goal.deadline} days.")

    print("Here are the users in the system:")
    print("====================================")
    userList = getUsers()
    for user in userList:
        print(f"User: {user['first_name']} {user['last_name']}, Email: {user['email']}")

    print

if __name__ == "__main__":
    main()