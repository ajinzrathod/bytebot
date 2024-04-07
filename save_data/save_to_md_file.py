def save_to_file(content, response_text):
    with open("data.md", "a") as file:
        file.write("### Plain Text:\n")
        file.write(f"{content}\n\n")
        file.write("### Response Text:\n")
        file.write(f"{response_text}\n\n")
        file.write("---\n\n")