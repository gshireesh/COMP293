import json
import string
from string import Template

resume_template = {
    "name": "Shireesh Kumar Gadidesi",
    "title": "Sr Software Engineer",
    "phone_no": "+1 209-242-4056",
    "email": "reachme@shireesh.com",
    "linked_in": "https://www.linkedin.com/in/gshireeshkumar/",
    "github": "https://github.com/gshireesh",
    "place": "San Francisco, CA",
    "environments": [
        "linux",
        "windows"
    ],
    "fontend": [
        "Javascript", "Typescript", "Angular", "React", "D3"
    ],
    "backend": [
        "Python", "Nodejs", "Java", "SQL", "Django", "Express", "GraphQl", "RabbitMq", "Kafka", "Redis"
    ],
    "cloud_and_automation": [
        "AWS", "Azure", "GCP", "Docker", "Linux", "Kubernetes", "Terraform", "Ansible", "Jenkins"
    ],
    "about": "<gpt>$about_prompt</gpt>",
    "education": [
        {
            "degree": "Master of Science",
            "department": "Computer Science",
            "institution": "University of the pacific",
            "location": "Stockton, CA, USA"
        },
        {
            "degree": "Bachelor of Technology",
            "department": "Computer Science and Engineering",
            "institution": "National Institute of Technology",
            "location": "Warangal, India"
        },
        {
            "degree": "Secondary School",
            "institution": "St Ann's School",
            "location": "Khammam, India"
        }
    ],
    "Interests": ["Family", "Math", "Thought experiments", "chess", "travelling", "movies"],
    "Experiences": [
        {
            "company": "6Sense Insights",
            "from": "Nov 21",
            "to": "Aug 22",
            "role": "Senior Software Engineer"
        },
        {
            "company": "Udaan",
            "from": "Jun 19",
            "to": "Aug 22",
            "role": "Product Engineer"
        },
        {
            "company": "StartupByte",
            "from": "Sep 16",
            "to": "May 19",
            "role": "Lead Full Stack Engineer"
        },
        {
            "company": "Factset Research Systems",
            "from": "Jun 14",
            "to": "Aug 16",
            "role": "software engineer"
        }
    ]
}

about_prompt = """
    generate a summary of 8-10 lines for the details in the json.
    It should professional as if a 9 year software engineer would write
"""

# tpl = Template(json.dumps(resume_template))
# tpl.substitute()


def flatten_json(y, prefix=''):
    out = {}
    if isinstance(y, dict):
        for key in y:
            result = flatten_json(y[key], prefix=prefix + key + '.')
            out.update(result)
    elif isinstance(y, list):
        for index, item in enumerate(y):
            result = flatten_json(item, prefix=prefix + str(index) + '.')
            out.update(result)
    else:
        out[prefix[:-1]] = y  # remove the trailing dot
    return out


def unflatten_json(y):
    out = {}
    for key, value in y.items():
        parts = key.split('.')
        d = out
        for part in parts[:-1]:
            if part not in d:
                d[part] = {}
            d = d[part]
        d[parts[-1]] = value
    return out


sensitive_words = [
    "name", "location", "phone", "email", "linkedin", "github",
]


def is_word_in_array(word, array):
    for item in array:
        if word.find(item) != -1:
            return True
    return False


def mask_sensitive_words(obj):
    flat = flatten_json(obj)
    mask = {}
    for k, v in flat.items():
        if is_word_in_array(k, sensitive_words) or is_word_in_array(v, sensitive_words):
            mask[k] = flat[k]
            flat[k] = "**"
    return unflatten_json(flat), unflatten_json(mask)





formats = {
    "undergrad": {
        "email": "s_gadidesi@u.pacific.edu",
    },
    "senior_software_engineer": {

    }
}

#%%
a, b = mask_sensitive_words(resume_template)

#%%
def process_templates(obj, meta):
    flat = flatten_json(obj)
    for k, v in flat.items():
        tpl = Template(v)
        flat[k] = tpl.substitute(meta)
    return unflatten_json(flat)


final = process_templates(a,{"about_prompt": about_prompt})

#%%
def save_to_file(data, name="./sample.json"):
    json_object = json.dumps(data, indent=4)

    # Writing to sample.json
    with open(name, "w") as outfile:
        print("done")
        outfile.write(json_object)

save_to_file(final)



#%%
import pandas as pd
df2 = pd.DataFrame({"x":[1,2], "y":[3,4]})
df3 = pd.DataFrame({"x":[11,21], "y":[31,41]})
#%%


json.loads()


#%%

from PIL import Image, ImageDraw, ImageFont

# Sample long and wide text
long_text = """This is a long text that could be very wide and needs to fit within the specified image width without word-wrapping. This allows you to generate an image that accommodates the entire text width."""
#
# import subprocess
#
# # Using system() method to
# # execute shell commands
# subprocess.Popen('pwd', shell=True)

# Define the image size and font size
image_width = 800
image_height = 600
font_size = 20

# Create a blank image
img = Image.new('RGB', (image_width, image_height), color='white')
draw = ImageDraw.Draw(img)

# Load a font
font = ImageFont.truetype('./arial.ttf', font_size)

# Calculate the maximum number of lines that can fit within the image
max_lines = int(image_height / font_size)

# Split the text into lines
lines = long_text.split("")

# Initialize y-coordinate for drawing
y = 10

# Loop through the lines and draw them on the image
for line in lines:
    if y + font_size <= image_height:
        draw.text((10, y), line, fill='black', font=font)
        y += font_size
    else:
        break

# Save or display the image
img.save('wide_text_image.png')

# To display the image, you can use a library like Matplotlib
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.imshow(img)
plt.axis('off')
plt.title('Image with Wide Text')
plt.show()


#%%
from rich import pretty
pretty.install()
from rich.console import Console

console = Console()
console.print("Hello", "World!", style="bold red")


#%%
import datashader as ds, pandas as pd, colorcet
df  = pd.read_csv('census.csv')
cvs = ds.Canvas(plot_width=850, plot_height=500)
agg = cvs.points(df, 'longitude', 'latitude')
img = ds.tf.shade(agg, cmap=colorcet.fire, how='log')
