import re
import requests
import base64

def search_github(query):
    base_url = "https://api.github.com/search/code"
    access_token = "YOURGITHUBAPI"  # Ihr persönlicher Zugriffstoken hier
    headers = {"Authorization": f"token {access_token}"}
    params = {"q": query}

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

def filter_characters(text):
    # Filterfunktion, um nur Buchstaben (groß und klein) und Zahlen zuzulassen
    allowed_chars_pattern = re.compile(r"[a-zA-Z0-9]+")
    filtered_text = "".join(filter(lambda char: allowed_chars_pattern.match(char), text))
    return filtered_text

if __name__ == "__main__":
    search_query = "sk-"
    search_result = search_github(search_query)

    if search_result:
        with open("result.txt", "w") as result_file:
            for item in search_result["items"]:
                content_url = item["url"]
                try:
                    response = requests.get(content_url)
                    response.raise_for_status()
                    content = response.json()["content"]
                    decoded_content = base64.b64decode(content).decode("utf-8")
                    search_match = re.search(r'sk-([a-zA-Z0-9]{48})', decoded_content)
                    if search_match:
                        found_string = search_match.group(1)
                        filtered_string = filter_characters(found_string)
                        result_file.write("Repository: {}\n".format(item["repository"]["name"]))
                        result_file.write("Path: {}\n".format(item["path"]))
                        result_file.write("URL: {}\n".format(item["html_url"]))
                        result_file.write("Found String: {}\n".format(filtered_string))
                        result_file.write("-" * 30 + "\n")
                except requests.exceptions.RequestException as e:
                    print("Error:", e)