import streamlit as st
import json
from pathlib import Path


parent_directory = Path(__file__).resolve().parents[1]


class Entry:
    def __init__(self, title, username, password, url="", tags: list = [None], note=""):
        self.entry = {title: {
            "username": username,
            "password": password,
            "url": url,
            "tags": [i for i in tags],
            "note": note}
        }

    def get(self):
        return self.entry


class PM:
    def __init__(self):
        self.db = {}
        self.load_json()

    def get(self, title):
        return self.db[title]

    def show_all(self):
        return self.db

    def add_update(self, entry: Entry):
        self.db.update(entry.get())
        self.save_json()

    def delete(self, title):
        removed = self.db.pop(title, None)
        self.save_json()
        return removed

    def search(self, title="", tag=""):
        output = {}

        if title in self.db.keys():
            output[title] = self.db[title]

        for key in self.db.keys():
            if isinstance(self.db[key]["tags"], list):
                for db_tag in self.db[key]["tags"]:
                    if db_tag == tag and key not in output.keys():
                        output[key] = self.db[key]
        return output

    def save_json(self, file_path="/data/password-manager.json"):
        str_db = json.dumps(self.db)

        with open(str(parent_directory) + file_path, 'w') as f:
            f.write(str_db)

    def load_json(self, file_path="/data/password-manager.json"):
        f = open(str(parent_directory) + file_path, 'r')
        self.db = json.load(f)


def get_pm():
    pm = PM()
    return pm


def search_page():
    col1, col2 = st.columns(2)
    title = col1.text_input("Title")
    tag = col2.text_input("Tag/Keyword")

    if len(title) > 0 or len(tag) > 0:
        json_db = get_pm().search(title, tag)
    else:
        json_db = get_pm().show_all()

    list_json(json_db)


def list_json(json_db):
    for key in json_db.keys():
        with st.expander(key):
            st.write(json_db[key])


def view_page(action=None):
    str_tags = ""

    if action is None:
        title = st.text_input("Title", value="")
    else:
        title = st.selectbox("Title", options=get_pm().db.keys())
        entry = get_pm().get(title)
        tags = entry["tags"]
        str_tags = ','.join(tags)

    with st.form("Add"):

        col1, col2 = st.columns(2)
        username = col1.text_input("Username", value=entry["username"] if action is not None else "")
        password = col2.text_input("Password", type="password", value=entry["password"] if action is not None else "")

        col1, col2 = st.columns(2)
        url = col1.text_input("URL", value=entry["url"] if action is not None else "")

        tags = col2.text_input("Tags (Comma Separated Values)", value=str_tags)

        notes = st.text_area("Notes", value=entry["note"] if action is not None else "")

        if action is not None:
            col1, col2 = st.columns(2)
            update_button = col1.form_submit_button("Update")
            delete_button = col2.form_submit_button("Delete")
        else:
            add_button = st.form_submit_button("Add")

        if action is not None:
            if delete_button:
                get_pm().delete(title)
                st.warning("Record deleted")

            if update_button:
                entry = Entry(title, username, password, url, [tags], notes)
                get_pm().add_update(entry)
                st.success("Record updated")
        else:
            if add_button:
                entry = Entry(title, username, password, url, [tags], notes)
                get_pm().add_update(entry)
                st.success("Record Added")


def main():
    st.title("Password Manager")

    main_menu = ["Search", "Add", "Update/Delete"]
    page = st.sidebar.selectbox("Main Menu", options=main_menu, index=0)

    if page.lower() == "search":
        search_page()
    if page.lower() == "add":
        view_page()
    if page.lower() == "update/delete":
        view_page(action="ud")


if __name__ == '__main__':
    main()
