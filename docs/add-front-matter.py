import os
import datetime

def add_front_matter(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            title = os.path.splitext(filename)[0]
            created_date = datetime.datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d')

            with open(filepath, 'r') as file:
                content = file.read()

            front_matter = f"---\ntitle: {title}\ntags: inbox\ncreated: {created_date}\n---\n\n"
            new_content = front_matter + content

            with open(filepath, 'w') as file:
                file.write(new_content)
            print(f"Added front matter to {filename}")

# Specify the directory containing your markdown files
directory = '.'
add_front_matter(directory)
