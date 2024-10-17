import os
from bs4 import BeautifulSoup

def convert_html_files(templates_dir):
    # Check if templates directory exists
    if not os.path.exists(templates_dir):
        print("The templates folder does not exist in the root project.")
        return  # Exit the function if the directory does not exist

    # Traverse the templates directory
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                convert_file(file_path)

def convert_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Add {% load static %} at the top of the file if not present
    if not soup.find(text="{% load static %}"):
        content = "{% load static %}\n" + str(soup)
    else:
        content = str(soup)

    # Remove existing DOCTYPE declarations
    if content.lower().startswith('<!doctype'):
        content = content.split('\n', 1)[1]  # Remove the first line (doctype)

    # Update img, script, and link tags
    for tag in soup.find_all(['img', 'script', 'link']):
        if tag.name == 'img':
            src = tag.get('src')
            if src and "{% static" not in src:
                tag['src'] = "{% static '" + src + "' %}"
        elif tag.name in ['script', 'link']:
            src = tag.get('src') or tag.get('href')
            if src and "{% static" not in src:
                if tag.name == 'script':
                    tag['src'] = "{% static '" + src + "' %}"
                else:
                    tag['href'] = "{% static '" + src + "' %}"

    # Rebuild the final content
    final_content = str(soup.prettify())

    # Check and add <!DOCTYPE html> if it's not present
    if '<!doctype html>' not in final_content.lower():
        final_content = '{% load static %}\n<!DOCTYPE html>\n' + final_content
        final_content = final_content.replace('<!DOCTYPE doctype html>', '')
    else:
        # Ensure the correct DOCTYPE is used
        final_content = final_content.replace('<!DOCTYPE doctype html>', '')

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)


