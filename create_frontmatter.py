from datetime import datetime

# Input data
title = "A short story of randomness (I)"
date_str = "Sun, 04 Apr 2021 07:17:45 GMT"
tags = ['kotlin', 'determinism', 'random', 'randomness']
# Author is captured but not used in this frontmatter block as per instructions
author = "Enrique López-Mañas"
images = []

# Reformat date
# Parse the original date string. Example: "Sun, 04 Apr 2021 07:17:45 GMT"
# RFC 822/1123 format. Python's strptime format code for this is '%a, %d %b %Y %H:%M:%S %Z'
dt_object = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
formatted_date = dt_object.strftime('%Y-%m-%d')

# Construct frontmatter string
frontmatter = "+++\n"
frontmatter += f'title = "{title}"\n'
frontmatter += f'date = "{formatted_date}"\n'
frontmatter += f'tags = {tags}\n'  # TOML arrays are represented like Python lists
frontmatter += f'images = {images}\n'
frontmatter += "+++\n"

print(frontmatter)
