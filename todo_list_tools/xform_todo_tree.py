def convert_tree_to_markdown(tree_input):
    markdown_lines = []
    for line in tree_input.strip().split('\n'):
        # Find the index of '├' or '└'
        idx = line.find('├')
        if idx == -1:
            idx = line.find('└')
        if idx == -1:
            continue  # Skip lines that don't have '├' or '└'
        # Compute the level
        level = idx // 4
        # Extract the content after '├───' or '└───'
        content = line[idx + 4:].strip()
        # Append to markdown lines with proper indentation
        markdown_lines.append('  ' * level + '* ' + content)
    return '\n'.join(markdown_lines)

# Sample input
tree_input = '''
 └───[26] sleep
     ├───[27] get tired
     ├───[45] read
     │    ├───[50] find something to read
     │    │    ├───[52] pick the subject
     │    │    │    └───[54] list the subjects
     │    │    │        └───[55] find the subject lister
     │    │    └───[56] find the dam glasses
     │    └───[51] put some dam glasses on
     └───[46] count sheep
         ├───[47] smoke something
         ├───[48] find something to smoke
         └───[49] determine the amount of sheep to count
             └───[53] think about what color the sheep are
'''

# Convert and print the markdown output
markdown_output = convert_tree_to_markdown(tree_input)
print(markdown_output)
