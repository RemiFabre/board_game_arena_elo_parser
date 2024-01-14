import os

results_folder = "./results/"
readme_file_path = "./README.md"


# This function reads the current README.md file and replaces the "# Results" section
def update_readme_with_images(readme_path, results_path):
    print("Read the current README contents")
    with open(readme_path, "r") as file:
        readme_contents = file.readlines()

    # Find the section to replace
    start_index = readme_contents.index("# Results\n")
    end_index = start_index + 1  # Initialize with the next line

    # Find the end of the "# Results" section
    for i in range(start_index + 1, len(readme_contents)):
        if readme_contents[i].startswith("#"):
            end_index = i
            break

    # Remove the current results section
    del readme_contents[start_index:end_index]

    # Generate the new results section
    new_results_section = ["# Results\n"]
    images = [img for img in os.listdir(results_path) if img.endswith(".png")]
    games = sorted(set(img.split("_")[0] for img in images))

    for game in games:
        new_results_section.append(f"### {game}\n")
        for img in sorted(images):
            if img.startswith(game):
                img_path = f"{results_path}{img}"
                new_results_section.append(
                    f"**{img.replace('_', ' ').rsplit('.', 1)[0]}**\n"
                )
                new_results_section.append(f"![{img}]({img_path})\n")

    # Insert the new results section into the README
    readme_contents[start_index:start_index] = new_results_section

    print("Write the updated contents back to the README.md...")
    with open(readme_path, "w") as file:
        file.writelines(readme_contents)


update_readme_with_images(readme_file_path, results_folder)
