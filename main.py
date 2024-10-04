import os
import datetime
import subprocess

def create_file(date, file_id):
    """Creates a file with a specific naming pattern and writes the filename into it."""
    filename = f"{date.strftime('%Y_%m_%d')}_{file_id}.txt"
    with open(filename, 'w') as file:
        file.write(filename)
    return filename

def commit_file(message, date):
    """Commits with a specified message and commit date."""
    commit_date = date.strftime('%Y-%m-%dT%H:%M:%S')
    subprocess.run(["git", "commit", "-m", message, "--date", commit_date])

def push_changes():
    """Pushes changes to the remote repository."""
    subprocess.run(["git", "push"])

def main(remote_url, start_year=2023):
    # Ensure a git repository is initialized
    if not os.path.isdir('.git'):
        subprocess.run(["git", "init"])
        # Set the remote repository
        subprocess.run(["git", "remote", "add", "origin", remote_url])
    
    # Generate a date range from start_year to today
    today = datetime.date.today()
    current_date = datetime.date(start_year, 1, 1)
    
    while current_date <= today:
        file_ids = []

        # Create and commit files for each day, then delete and commit
        files_to_commit = 11
        for file_id in range(1, files_to_commit):  # Create 5 files per day
            filename = create_file(current_date, file_id)
            file_ids.append(filename)
            subprocess.run(["git", "add", filename])
        
        # First Commit: Adding files
        commit_file(f"Add files for {current_date}", current_date)

        # Second Commit: Remove the files
        for filename in file_ids:
            os.remove(filename)
            subprocess.run(["git", "rm", filename])
        
        # Commit the removal
        commit_file(f"Remove files for {current_date}", current_date)

        # Push changes to the remote repository
        push_changes()
        
        # Move to the next day
        current_date += datetime.timedelta(days=1)

if __name__ == "__main__":
    # Set your remote repository URL
    remote_url = "https://your-remote-repository-url.git"
    main(remote_url)
