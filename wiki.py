import wikipediaapi

def get_wikipedia_page_content(page_title):
    wiki_wiki = wikipediaapi.Wikipedia(
    language='fr',
    user_agent='SemanticExplorers/1.0 (theo.flament@etu.umontpellier.fr)'
)
    page = wiki_wiki.page(page_title)

    if page.exists():
        return page.text
    else:
        return f"La page '{page_title}' n'existe pas."

def split_text_into_words(text):
    words = [word.strip(":,;!?()[]«»{}%1234567890") for word in text.split()]
    return words

def write_words_to_file(words):
    with open("BDD.txt", 'w', encoding='utf-8') as file:
        file.write("\n".join(words))

if __name__ == "__main__":
    page_title = "Rhume"
    page_content = get_wikipedia_page_content(page_title)

    if "La page 'Rhume' n'existe pas." not in page_content:
        words = split_text_into_words(page_content)

        print(f"Mots de la page '{page_title}':\n")
        print(words)
        write_words_to_file(words)
        print("Les mots ont été écrits dans le fichier 'BDD.txt'.")
    else:
        print(page_content)
