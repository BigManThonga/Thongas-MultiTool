import os
import subprocess

# Define the 'tools' directory (relative to where the script is running)
tools_dir = os.path.join(os.getcwd(), 'tools')

# List of tools with their specific Python files to run from the 'tools' directory
tools = {
    "MPTube": "MPTube/MPTube.py",
    "PDF Reader": "PDF Reader/pdfread.py",
    "Sysfetch": "Sysfetch/Sysfetch.py",
    "ImgAsciiConvert": "Image to ASCII art/ImgAsciiConvert.py",
    # "Tool": "ToolPath",
}

# Ensure the 'tools' directory exists
if not os.path.exists(tools_dir):
    os.makedirs(tools_dir)

# Install packages from requirements.txt
def install_requirements():
    requirements_path = os.path.join(os.getcwd(), 'requirements.txt')
    if os.path.exists(requirements_path):
        print("Installing required packages...")
        try:
            subprocess.check_call(['pip', 'install', '-r', requirements_path])
            print("Packages installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install packages: {e}")
    else:
        print("No requirements.txt file found. Skipping package installation.")

# Display the multitool manager menu
def display_menu():
    print("Thonga's Multitool v1.0\n")
    while True:
        command = input("> ").strip()
        if command.lower() == "tmt help":
            display_help()
        elif command.lower() == "tmt about":
            print("\nVersion: 1.0\n")
        elif command.lower() == "tmt listtool":
            list_tools()
        elif command.lower().startswith("tmt "):
            run_tool(command[4:].strip())
        elif command.lower() == "exit":
            print("Exiting")
            break
        else:
            print("Invalid command. Type 'TMT Help' for a list of commands.")

# Display the help menu
def display_help():
    print("\nAvailable commands:")
    print("TMT Help        - Lists all commands")
    print("TMT About       - Displays the version string of 1.0")
    print("TMT [Tool Name] - Runs a specified tool")
    print("TMT ListTool    - Lists all tools\n")

# List all tools in the 'tools' directory (based on the list in the script)
def list_tools():
    print("\nAvailable tools:")
    for tool in tools:
        print(f"- {tool}")
    print()

# Run a specified tool by pointing to its specific Python file
def run_tool(tool_name):
    if tool_name in tools:
        tool_script = tools[tool_name]
        tool_path = os.path.join(tools_dir, tool_script)

        if os.path.exists(tool_path):
            print(f"Running {tool_name}... ({tool_path})")
            try:
                subprocess.run(["python", tool_path], check=True)
            except subprocess.CalledProcessError as e:
                print(f"\nError running the tool: {e}\n")
        else:
            print(f"\nError: The tool '{tool_name}' script does not exist in the specified folder.\n")
    else:
        print(f"\nError: Tool '{tool_name}' not found.\n")

# Main program
if __name__ == "__main__":
    install_requirements()
    display_menu()
