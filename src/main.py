from textnode import TextNode, TextType

def copy_source_to_destination(source, destination):
    pass

def main():
    node = TextNode("Hello, bold world!", TextType.BOLD, "https://example.com")
    print(node)

if __name__ == "__main__":
    main()
