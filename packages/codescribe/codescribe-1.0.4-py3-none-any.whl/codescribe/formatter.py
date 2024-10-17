from typing import List, Dict


# DSA used here
def sort_contents(contents: List[Dict]) -> List[Dict]:
    return sorted(contents, key=lambda x: x["path"])


def build_directory_structure(contents: List[Dict]) -> str:
    tree = {}
    for item in contents:
        parts = item["path"].split("/")
        current = tree
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]

        current[parts[-1]] = None

    def build_tree(node, prefix="") -> str:
        result = ""
        items = list(node.items())
        for i, (name, subtree) in enumerate(items):
            is_last = i == len(items) - 1
            result += f"{prefix}{'└── ' if is_last else '├── '}{name}\n"
            if subtree is not None:
                result += build_tree(subtree, prefix + ("    " if is_last else "│   "))
        return result

    return build_tree(tree)


def format_repo_contents(contents: List[Dict]) -> str:
    content = sort_contents(contents)
    directory_structure = build_directory_structure(contents)

    formatted_content = f"Directory Structure:\n\n{directory_structure}\n"

    for item in contents:
        formatted_content += (
            f"\n\n---\nFile: {item['path']}\n---\n\n{item['content']}\n"
        )

    return formatted_content
