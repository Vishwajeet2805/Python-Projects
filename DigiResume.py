# Project: Digital Resume Builder

def build_resume():
    print("Digital Resume Builder\n")

    name = input("Full Name: ")
    email = input("Email: ")
    phone = input("Phone Number: ")
    summary = input("Short Summary About You: ")

    print("\nEnter your skills (type 'done' when finished):")
    skills = []
    while True:
        skill = input("> ")
        if skill.lower() == 'done':
            break
        skills.append(skill)

    print("\nEnter your experiences (type 'done' when finished):")
    experiences = []
    while True:
        exp = input("> ")
        if exp.lower() == 'done':
            break
        experiences.append(exp)

    resume = f"""
    ================================
            {name.upper()}
    ================================

     Email: {email}
     Phone: {phone}

     SUMMARY
    {summary}

     SKILLS
    - {chr(10) + "- ".join(skills)}

     EXPERIENCE
    - {chr(10) + "- ".join(experiences)}
    """

    filename = name.lower().replace(" ", "_") + "_resume.txt"
    with open(filename, "w") as file:
        file.write(resume)

    print(f"\n Resume saved as '{filename}'!")


build_resume()
