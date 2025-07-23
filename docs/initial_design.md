

# **The Quarto Single Source of Truth: A Unified System for Website, CV, and Resume Generation**

This report provides an exhaustive, expert-level guide to building a robust, automated "single source of truth" system. The objective is to maintain a central set of YAML files containing all professional information, from which a personal website, a comprehensive Curriculum Vitae (CV), and multiple tailored resumes can be generated and published using Quarto. This system leverages the power of Quarto's multi-format publishing capabilities, the elegance of the awesomecv-typst extension, the flexibility of Python scripting, and the automation of GitHub Actions to create a professional, maintainable, and scalable personal branding platform.

## **Section 1: Foundational Setup and Core Concepts**

A robust system requires a solid foundation. This section details the installation of the complete development toolchain and introduces the core principles of Quarto that make this project possible. Correctly configuring this environment is the essential first step toward building the automated generation pipeline.

### **1.1 The Quarto Philosophy: Beyond Markdown**

Quarto is an open-source scientific and technical publishing system that represents a significant evolution from traditional static site generators or markdown converters.1 It is best understood as a literate programming system, designed from the ground up to weave together narrative text, executable code, and its output into polished, reproducible documents.1 This philosophy is central to achieving the "single source of truth" objective.  
Unlike systems that simply convert markdown to HTML, Quarto integrates three powerful components into a single, cohesive workflow:

1. **Enhanced Markdown:** At its core, Quarto uses Pandoc-flavored markdown, which provides excellent support for academic and technical content like LaTeX equations, citations, and cross-references. Quarto extends this with numerous features such as callouts, figure panels, and advanced page layout capabilities, allowing for the creation of complex and beautifully formatted documents.1  
2. **Multi-Language Computation:** Quarto is fundamentally multi-language. It can execute code from Python, R, Julia, and Observable JS directly within a document.2 For a Python developer, this means the full power of the Python ecosystem is available during the document rendering process. Quarto uses Jupyter as the default execution engine for Python, enabling the use of any Python library to process data, generate visualizations, or even programmatically create content.1  
3. **Single-Source Publishing:** The ultimate goal of Quarto is to enable the creation of content for multiple destinations from a single source document. It can produce a vast array of output formats, including HTML for websites, PDF and Typst for print-quality documents, MS Word for collaboration, and Reveal.js presentations, among many others.2

This combination of features transforms a simple text file into a dynamic, reproducible artifact. For this project, it means a .qmd file is not just a static page; it is a program that can read data, perform logic, and generate a perfectly formatted website page or CV as its output.

### **1.2 The Four-Layer Toolchain Installation**

The architecture of the required toolchain is layered and interdependent. A failure in one layer can cause downstream issues that are difficult to diagnose. Therefore, a methodical, layer-by-layer installation is paramount.

#### **Layer 1: The Quarto CLI**

The Quarto Command Line Interface (CLI) is the core engine that orchestrates the entire rendering process. It is a self-contained binary that includes Pandoc and all other necessary components to convert .qmd files into their various output formats.  
For a Python developer, the most idiomatic installation method is via pip. This approach integrates well with Python's existing package management ecosystem.5  
**Installation (Terminal):**

Bash

\# Ensure you are in your project's virtual environment  
pip install quarto-cli

The quarto-cli package on PyPI is a wrapper that downloads the appropriate Quarto binary for the host operating system during installation.5 After installation, the  
quarto command will be available in the shell. To verify the installation, run:

Bash

quarto \--version

Alternative installation methods, such as downloading .deb or .msi installers directly from the Quarto website, are also available for different operating systems.6

#### **Layer 2: The Typst Compiler**

The chosen CV and resume format, awesomecv-typst, leverages Typst, a modern, markup-based typesetting system designed to be a powerful and fast alternative to LaTeX.8 Quarto's role is to generate an intermediate  
.typ file from the source .qmd document. However, an external Typst compiler is required to convert this .typ file into the final, high-quality PDF.  
The installation process for Typst is separate from Quarto. The recommended method is to use a system package manager.9  
**Installation for macOS (Terminal):**

Bash

brew install typst

**Installation for Windows (Terminal):**

Bash

winget install \--id Typst.Typst

For Linux distributions, various package managers are supported, or a pre-compiled binary can be downloaded directly from the Typst GitHub repository.9 Once installed, the  
typst command should be available in the shell. The installation can be verified with:

Bash

typst \--version

#### **Layer 3: Editor Integration (VS Code)**

While any text editor can be used to write Quarto documents, a dedicated extension significantly enhances the authoring experience. For Visual Studio Code, the official Quarto extension is indispensable.10 It provides a suite of tools that streamline development:

* **Live Render and Preview:** A Preview button allows for rendering the document and viewing the output side-by-side with the source code. The preview automatically updates on save.10  
* **Syntax Highlighting:** Provides rich highlighting for Quarto markdown, YAML headers, and embedded code chunks.  
* **Code Completion and Execution:** Offers intelligent code completion and allows for executing code cells interactively within the editor, with output appearing in the Jupyter interactive console.10  
* **Contextual Assistance:** Provides live previews for LaTeX equations and diagrams as they are being typed.10

**Installation (VS Code):**

1. Open the Extensions view (Ctrl+Shift+X).  
2. Search for "Quarto".  
3. Install the official extension published by quarto.org.

#### **Layer 4: Python Environment**

To ensure the project is reproducible and its dependencies are isolated, a dedicated Python virtual environment is a necessity. This becomes especially critical when preparing the project for automated deployment with GitHub Actions, which will need to replicate the environment precisely.11  
**Setup (Terminal):**

Bash

\# Create a new directory for the project  
mkdir my-quarto-system && cd my-quarto-system

\# Create a Python virtual environment  
python \-m venv.venv

\# Activate the virtual environment  
\# On macOS/Linux:  
source.venv/bin/activate  
\# On Windows:  
\#.venv\\Scripts\\activate

\# Install the required Python library for parsing YAML  
pip install pyyaml

All subsequent pip install and quarto commands should be run from within this activated environment.

### **1.3 Creating Your Quarto Project: The Central Hub**

With the toolchain in place, the next step is to initialize a Quarto Project. A project provides a formal structure for managing multiple documents, sharing configuration, and defining render targets.11 This is the ideal structure for a system that will produce a website, a CV, and multiple resumes.  
To create a new project, use the quarto create project command. For this system, starting with a website project type is the most logical choice.13  
**Initialization (Terminal):**

Bash

\# From within the project directory with the activated venv  
quarto create project website.

This command initializes the current directory as a Quarto website project. It creates several files, the most important of which is \_quarto.yml.13 This file acts as the central control panel for the entire system. Initially, it will contain basic website configuration:  
**\_quarto.yml (Initial State):**

YAML

project:  
  type: website

website:  
  title: "My Website"  
  navbar:  
    left:  
      \- href: index.qmd  
        text: Home  
      \- about.qmd

format:  
  html:  
    theme: cosmo  
    css: styles.css

This file defines the project type, shared metadata that applies to all documents, and default options for output formats.11 It will be expanded significantly as the system is built out.

### **1.4 "Hello, World": Your First Render**

To confirm that all layers of the toolchain are functioning correctly, a simple render test is essential. The quarto preview command starts a local web server, renders the specified file (or the entire project), and opens a browser to display the result. It also watches for file changes and automatically refreshes the preview.13

1. Open the project directory in VS Code.  
2. Ensure the index.qmd file contains a basic YAML header and some text.  
3. Click the Preview button in the top-right of the VS Code editor, or run the command in the integrated terminal:

**Execution (Terminal):**

Bash

quarto preview

This command should successfully render index.qmd and about.qmd into HTML files within a \_site directory and display the homepage in a browser or the VS Code preview pane.15 This successful render validates the entire setup and provides the foundation for the more complex work ahead.

## **Section 2: Architecting the Single Source of Truth: Your YAML Data Model**

The core of this system is the "single source of truth." This is not just a concept but a tangible data architecture. By separating the data (the "what" of your professional life) from its presentation (the "how" it appears on a website or CV), you create a system that is efficient, maintainable, and scalable. A change to a job title or skill, made in one central location, will automatically propagate across all generated outputs upon the next render. YAML is the ideal format for this data model due to its human-readable syntax and excellent support in Python.

### **2.1 Principles of Data-Presentation Separation**

The fundamental design principle is to treat your professional information as a structured dataset. Instead of hardcoding your work experience into a markdown file, you define it as a series of entries in a data file. The Quarto documents (.qmd files) then become templates that read this data and render it into the appropriate format.  
This approach has several profound advantages:

* **Maintainability:** Updating your information involves editing a simple, structured text file, not navigating complex markdown or HTML layouts.  
* **Consistency:** Ensures that your job titles, dates, and project descriptions are identical across your website, CV, and all resumes, eliminating embarrassing inconsistencies.  
* **Scalability:** Adding a new project, skill, or publication is a matter of appending a new entry to the relevant data file. The presentation layer automatically adapts.  
* **Programmability:** By structuring the data, it becomes queryable. This is the key that unlocks the ability to generate tailored resumes by programmatically filtering and selecting relevant data points.

### **2.2 The Master YAML Files**

To keep the project organized and the data model modular, all data files will reside in a dedicated \_data/ directory at the project root. This separation keeps the main project directory clean and the data logically segmented.  
The proposed data model consists of the following files:

* **\_data/personal.yml:** This file will store core identity and contact information. It will contain your name, professional title or tagline, a brief summary or bio, and contact details like email, phone, address, and links to social/professional profiles (LinkedIn, GitHub, etc.). This data will be used in the header of the CV and the "About" section of the website.  
* **\_data/experience.yml:** This file will list all professional roles. Each entry will be an object containing keys for title, company, location, start\_date, end\_date, and a list of achievements. To enable the creation of tailored resumes, a crucial tags field will be added to each achievement. For example, an achievement might be tagged with \['aerospace', 'python', 'simulation'\], allowing a Python script to later select only those achievements relevant to an aerospace engineering role.  
* **\_data/education.yml:** A straightforward list of educational qualifications. Each entry will have keys for degree, institution, location, and date\_range.  
* **\_data/skills.yml:** This file will contain a structured inventory of skills. To provide organization, skills will be grouped into categories (e.g., "Programming Languages," "Data Science Frameworks," "Aerospace Software"). Each individual skill entry will also have a field tag (e.g., \['datascience', 'research'\]) to allow for filtering based on the target job domain.  
* **\_data/projects.yml:** A portfolio of key projects. Each entry will include a title, description, a list of technologies used, a url to the project or repository, and tags for filtering (e.g., \['data-visualization', 'python', 'public-facing'\]).  
* **\_data/publications.yml:** A list of academic or professional publications. Each entry will have standard bibliographic fields like title, authors, journal\_or\_conference, year, doi, and url.

The foresight in this data model lies in the inclusion of metadata fields like tags and field. These fields transform the YAML files from a simple data store into a queryable database. Without this metadata, programmatic filtering for tailored resumes would be impossible. This design anticipates the needs of the most complex output (the tailored resumes) and builds that capability into the data model from the very beginning.

### **2.3 The YAML Schema Blueprint**

To ensure consistency and facilitate the writing of Python parsing scripts, the following table defines the precise schema for each YAML file. This blueprint serves as a definitive guide for data entry and as a reference when developing the rendering logic.  
**Table 1: Proposed YAML Data Structure and Schema**

| File Name | Purpose | Top-Level Key(s) | Entry Structure (Keys & Example Types) |
| :---- | :---- | :---- | :---- |
| \_data/personal.yml | Core identity and contact info | info, contact, social | name: string, position: string, summary: multiline-string, email: string, phone: string, website: url, linkedin: url, github: url |
| \_data/experience.yml | Professional work history | jobs | A list of objects, each with: title: string, company: string, location: string, start\_date: YYYY-MM, end\_date: YYYY-MM or Present, achievements: list-of-objects where each object is {description: string, tags: list-of-strings} |
| \_data/education.yml | Academic background | degrees | A list of objects, each with: degree: string, major: string, institution: string, location: string, date\_range: string |
| \_data/skills.yml | Technical and soft skills | skill\_sets | A list of objects, each with: category: string, skills: list-of-objects where each object is {name: string, level: int(1-5), field: list-of-strings} |
| \_data/projects.yml | Portfolio of projects | projects | A list of objects, each with: title: string, description: multiline-string, technologies: list-of-strings, url: url, tags: list-of-strings |
| \_data/publications.yml | List of publications | publications | A list of objects, each with: title: string, authors: string, venue: string, year: int, doi: string, url: url |

Adhering to this schema will make the subsequent steps of programmatically generating content significantly more straightforward and robust.

## **Section 3: Building the Personal Website**

With the data architecture defined, the next step is to build the first output: a professional, data-driven personal website. This process involves configuring the Quarto website project and creating dynamic pages that pull content directly from the YAML files using embedded Python code. This approach ensures the website is a living document that updates automatically as the underlying data changes.

### **3.1 Configuring a Quarto Website Project**

The \_quarto.yml file is the control center for the website. It defines the site's overall structure, navigation, appearance, and other project-wide settings.11  
First, the project type is already set to website. Next, the navigation bar and theme can be customized. Quarto websites can use any of the 25 themes from the Bootswatch project, providing a wide range of aesthetic choices with minimal effort.15 The navigation bar is defined by a list of links. Quarto conveniently allows linking directly to the source  
.qmd files, and it will automatically resolve the links to the correct output .html files during rendering.13  
Here is an example of an updated \_quarto.yml for the website:  
\_quarto.yml (Website Configuration):

YAML

project:  
  type: website  
  output-dir: \_site \# Explicitly define the output directory

website:  
  title: "John Doe | Aerospace & Data Science"  
  site-url: "https://your-github-username.github.io/your-repo-name" \# Important for feeds and metadata  
  navbar:  
    left:  
      \- href: index.qmd  
        text: Home  
      \- href: projects.qmd  
        text: Projects  
      \- href: cv/cv.pdf \# Direct link to the CV PDF  
        text: CV  
  page-footer: "Copyright 2024, John Doe"

format:  
  html:  
    theme:  
      light: flatly  
      dark: darkly  
    css: styles.css  
    toc: true

This configuration sets a title, defines a navigation bar with links to the homepage, a projects page, and the yet-to-be-created CV PDF. It also specifies a theme (flatly for light mode, darkly for dark mode) and a custom stylesheet (styles.css) for any further tweaks.16 The  
site-url is essential for generating correct absolute links and for features like RSS feeds.18

### **3.2 Creating Dynamic Pages with Python**

The true power of this system is realized by generating page content programmatically. Instead of manually writing markdown for each project or skill, a Python script embedded within a .qmd file will read the YAML data and generate the markdown dynamically.  
This process leverages Quarto's ability to execute code chunks. A code chunk is a block of code, in this case Python, that is executed during the quarto render command. The output of this code can be captured and inserted into the final document.19  
Let's create the projects.qmd page. This file will contain a Python code chunk that reads \_data/projects.yml and generates a formatted list of projects.

## **projects.qmd:**

## **title: "My Projects"**

Here are some of the key projects I have worked on.{python}  
\#| echo: false  
\#| output: asis  
import yaml

# **Load the project data from the YAML file**

with open('\_data/projects.yml', 'r') as f:  
projects\_data \= yaml.safe\_load(f)

# **Loop through each project and print its details in Markdown format**

for project in projects\_data.get('projects',):  
title \= project.get('title', 'N/A')  
url \= project.get('url', '')  
description \= project.get('description', '')  
technologies \= project.get('technologies',)

\# Create the title with a link if a URL is provided  
if url:  
    print(f"\#\#\# \[{title}\]({url})")  
else:  
    print(f"\#\#\# {title}")  
      
\# Print the description  
print(f"\\n{description}\\n")

\# Print the technologies used  
if technologies:  
    tech\_list \= ", ".join(f"\`{tech}\`" for tech in technologies)  
    print(f"\*\*Technologies:\*\* {tech\_list}\\n")  
      
\# Add a horizontal rule for separation  
print("---\\n")

Two critical chunk options make this work 20:

* \#| echo: false: This option tells Quarto to execute the Python code but not to include the code itself in the final rendered HTML page. The user will only see the output.  
* \#| output: asis: This stands for "as-is". It instructs Quarto to treat the standard output of the Python script (everything generated by print()) as raw markdown to be parsed and rendered, rather than as plain text to be displayed in a pre-formatted block.

This pattern can be replicated for other pages. An experience.qmd page could read \_data/experience.yml to list job history, and a skills.qmd page could create categorized lists from \_data/skills.yml. The website becomes a living document; adding a new project is as simple as adding an entry to projects.yml and re-rendering. This fundamentally changes the maintenance model from "editing a website" to "curating a dataset."

### **3.3 Styling and Layout**

While the chosen Bootswatch theme provides a strong visual foundation, Quarto offers powerful tools for more granular control over page layout.22 Content can be arranged using CSS grid-like column layouts directly in markdown.  
For example, to place an image next to a block of text, you can use a div with column classes:  
::: {.columns}  
::: {.column width="60%"}  
This is the main text content that will occupy 60% of the available width. It can contain paragraphs, lists, and other markdown elements.  
:::  
::: {.column width="40%"}

:::  
:::  
Quarto also allows for placing content in the page margin, creating full-bleed sections that span the entire page width, or creating callout blocks to highlight specific information.22 For fine-grained visual adjustments not covered by the theme or layout options, custom CSS rules can be added to the  
styles.css file, which was linked in the \_quarto.yml configuration.15

## **Section 4: Generating the Comprehensive CV with awesomecv-typst**

The next major output is a comprehensive, beautifully typeset Curriculum Vitae in PDF format. This is achieved by leveraging a Quarto extension that integrates with the Typst typesetting system. The key to this process is creating a Python-based "adapter" that translates the data from our custom YAML format into the specific format required by the CV template.

### **4.1 Installing and Using a Quarto Extension**

Quarto extensions are self-contained packages that can provide new output formats, templates, shortcodes, or filters. They are a powerful way to extend Quarto's built-in functionality.24 The  
quarto-awesomecv-typst extension provides a custom format that replicates the popular "Awesome-CV" LaTeX style using Typst.25  
To use an extension, it must first be installed into the project. The quarto add command handles downloading the extension from a GitHub repository and placing it in a local \_extensions directory.26 It is crucial to commit this directory to version control to ensure the project is fully reproducible by anyone, at any time, without relying on the external availability of the extension.26  
**Installation (Terminal):**

Bash

quarto add extension kazuyanagimoto/quarto-awesomecv-typst

This command creates the \_extensions/kazuyanagimoto/quarto-awesomecv-typst/ directory and populates it with the necessary template files (.typ) and configuration (\_extension.yml).25

### **4.2 Creating the CV Document (cv.qmd)**

A new Quarto document, cv.qmd, will serve as the source for the CV. Its YAML header must be configured to use the newly installed format and to provide the specific metadata the template requires.  
The awesomecv-typst format expects several specific keys in the YAML header 25:

* format: awesomecv-typst: Specifies that this document should be rendered using the custom format.  
* author: A nested object containing firstname, lastname, position, and a list of contacts. Each contact can have an icon, text, and url.  
* style: An object to control aesthetics like color-accent and fonts (font-header, font-text).  
* profile-photo: An optional path to a profile picture.

**cv.qmd (Initial YAML Header):**

YAML

\---  
format: awesomecv-typst  
author:  
  firstname: "John"  
  lastname: "Doe"  
  position: "Aerospace Engineer & Data Scientist"  
  contacts:  
    \- icon: fa-solid fa-envelope  
      text: "john.doe@email.com"  
      url: "mailto:john.doe@email.com"  
    \- icon: fa-brands fa-github  
      text: "johndoe"  
      url: "https://github.com/johndoe"  
    \- icon: fa-brands fa-linkedin  
      text: "johndoe"  
      url: "https://www.linkedin.com/in/johndoe"  
style:  
  color-accent: "516db0"  
  font-header: "Roboto"  
  font-text: "Source Sans Pro"  
profile-photo: "assets/profile.jpg"  
\---

Note that icon names (e.g., fa-solid fa-envelope) should match those available from Font Awesome, as the template uses a Typst package to render them.25

### **4.3 Data Mapping: From YAML to Typst**

This is the most critical part of generating the CV. The awesomecv-typst template uses a specific Typst function, \#resume-entry(...), to create the main entries in the CV sections (like work experience and education).28 Our internal YAML data model is designed for flexibility, while the template has its own, more rigid data requirements. Therefore, a Python script inside  
cv.qmd must act as an "adapter," translating our data format into the template's expected format.  
This adapter pattern is a robust software design choice. It decouples our core data from the presentation layer. If, in the future, a different CV template is desired, only this adapter script needs to be modified, not the underlying data files in the \_data/ directory.  
The Python script will load the master YAML files, loop through the data, and programmatically print the Typst-specific markdown.  
**cv.qmd (Full Content with Python Adapter):**

YAML

\---  
\# (YAML header from above)  
\---

\`\`\`{python}  
\#| echo: false  
\#| output: asis

import yaml  
from datetime import datetime

\# \--- Helper Functions \---  
def format\_date\_range(start, end):  
    """Formats start and end dates into a string."""  
    start\_date \= datetime.strptime(start, '%Y-%m')  
    start\_str \= start\_date.strftime('%b %Y')  
    if end.lower() \== 'present':  
        end\_str \= 'Present'  
    else:  
        end\_date \= datetime.strptime(end, '%Y-%m')  
        end\_str \= end\_date.strftime('%b %Y')  
    return f"{start\_str} \- {end\_str}"

def print\_resume\_entry(item):  
    """Prints a Typst \#resume-entry function call."""  
    title \= item.get('title', '')  
    location \= item.get('location', '')  
    date \= item.get('date', '')  
    description \= item.get('description', '')  
      
    \# Escape quotes and backslashes for Typst strings  
    title \= title.replace('"', '\\\\"').replace('\\\\', '\\\\\\\\')  
    location \= location.replace('"', '\\\\"').replace('\\\\', '\\\\\\\\')  
    date \= date.replace('"', '\\\\"').replace('\\\\', '\\\\\\\\')  
    description \= description.replace('"', '\\\\"').replace('\\\\', '\\\\\\\\')

    print(f'\#resume-entry(title: "{title}", location: "{location}", date: "{date}", description: "{description}")')

def print\_resume\_items(items):  
    """Prints a list of items as a Typst bulleted list."""  
    if items:  
        print('\#resume-item\[')  
        for item in items:  
            desc \= item.get('description', '').replace('"', '\\\\"').replace('\\\\', '\\\\\\\\')  
            print(f'- {desc}')  
        print('\]')

\# \--- Load All Data \---  
with open('\_data/personal.yml', 'r') as f:  
    personal\_data \= yaml.safe\_load(f)  
with open('\_data/experience.yml', 'r') as f:  
    experience\_data \= yaml.safe\_load(f)  
with open('\_data/education.yml', 'r') as f:  
    education\_data \= yaml.safe\_load(f)  
with open('\_data/skills.yml', 'r') as f:  
    skills\_data \= yaml.safe\_load(f)

\# \--- Render CV Sections \---

\# Summary  
print('== Summary')  
print(personal\_data.get('info', {}).get('summary', ''))  
print('\\\\') \# Typst line break

\# Work Experience  
print('== Work Experience')  
for job in experience\_data.get('jobs',):  
    job\_entry \= {  
        'title': job.get('title'),  
        'location': job.get('location'),  
        'date': format\_date\_range(job.get('start\_date'), job.get('end\_date')),  
        'description': job.get('company')  
    }  
    print\_resume\_entry(job\_entry)  
    print\_resume\_items(job.get('achievements',))  
print('\\\\')

\# Education  
print('== Education')  
for degree in education\_data.get('degrees',):  
    edu\_entry \= {  
        'title': degree.get('degree'),  
        'location': degree.get('location'),  
        'date': degree.get('date\_range'),  
        'description': degree.get('institution')  
    }  
    print\_resume\_entry(edu\_entry)  
print('\\\\')

\# Skills  
print('== Skills')  
for skill\_set in skills\_data.get('skill\_sets',):  
    category \= skill\_set.get('category')  
    skills \= ", ".join(\[s.get('name') for s in skill\_set.get('skills',)\])  
    skill\_entry \= {  
        'title': category,  
        'description': skills  
    }  
    \# Using resume-entry for skills requires a bit of a hack,  
    \# leaving location and date blank.  
    print(f'\#resume-entry(title: "{skill\_entry\["title"\]}", description: "{skill\_entry\["description"\]}", location: "", date: "")')

This script defines helper functions to format data and print the required Typst syntax. It then loads all the master YAML files and iterates through them, calling the helper functions to generate the content for each section of the CV. The \== Section Title syntax creates a major section heading in the awesomecv-typst format.  
To generate the CV, simply render this file:  
Execution (Terminal):

Bash

quarto render cv.qmd

This command will execute the Python script, pass the resulting .typ file to the Typst compiler, and produce a polished cv.pdf file in the project's root directory.

## **Section 5: Mastering Tailored Resumes with Project Profiles**

This section addresses the most advanced requirement of the system: generating multiple, distinct resumes tailored for specific job applications (e.g., for research, aerospace engineering, and data science roles). This is accomplished using two powerful Quarto features in concert: Project Profiles and Pre-render Scripts. This combination provides a highly flexible and scalable architecture for programmatic content filtering and generation.

### **5.1 Introduction to Quarto Project Profiles**

Quarto Project Profiles are the native mechanism for creating different "versions" of a project's output from the same set of source files.31 A profile allows for overriding project configurations, setting environment variables, and conditionally including content based on which profile is active.  
Profiles are defined by creating additional YAML configuration files in the project root. The file name convention is \_quarto-\<profile-name\>.yml. For this project, we will create profiles for each target resume:

* \_quarto-research.yml  
* \_quarto-aerospace.yml  
* \_quarto-datascience.yml

A specific profile is activated during rendering using the \--profile command-line flag.31 For example, to render the research-focused resume, the command would be:

Bash

quarto render \--profile research

When this command is run, Quarto merges the configuration from \_quarto-research.yml with the main \_quarto.yml file, giving the profile-specific settings precedence.

### **5.2 Strategy 1: Basic Tailoring with Conditional Content**

Quarto provides a straightforward method for conditional content using special div blocks. The when-profile attribute can be used to mark content that should only be included when a specific profile is active.31  
For example, in a .qmd file, one could include a publications section only for the "research" profile:  
::: {.content-visible when-profile="research"}  
\== Publications  
(Content for publications goes here...)  
:::  
This approach is simple and effective for coarse-grained control, such as including or excluding entire sections. However, it quickly becomes unmanageable for the fine-grained filtering required for this project (e.g., selecting specific bullet points from within a single job experience). The .qmd file would become cluttered with complex conditional logic, violating the principle of separating data from presentation.

### **5.3 Strategy 2: Advanced Tailoring with Pre-render Scripts**

The superior and more scalable solution is to use a pre-render script. This is a script that Quarto executes *before* it begins the main rendering process.33 This script has the power to programmatically modify project data, making it the perfect tool for filtering and tailoring the resume content.  
The workflow is as follows:

1. Configure the Pre-render Script: The \_quarto.yml file is updated to specify a Python script to run before rendering.  
   \_quarto.yml (with pre-render script):  
   YAML  
   project:  
     \#... other project settings  
     pre-render: scripts/generate\_resume\_data.py

2. Create the Filtering Script: A new script, scripts/generate\_resume\_data.py, is created. This script is the "brain" of the tailoring system. It will:  
   a. Read the QUARTO\_PROFILE environment variable, which Quarto automatically sets to the name of the active profile.33

   b. Load the master data from all the files in the \_data/ directory.  
   c. Based on the active profile, it will perform filtering logic. For the "aerospace" profile, it will select skills with the aerospace field tag and job achievements with the aerospace tag.  
   d. It can also reorder entire sections. For the "research" profile, it might place the "Education" and "Publications" sections before "Work Experience."  
   e. Finally, the script will write its filtered and reordered data to a single, temporary data file, such as \_data/tmp\_resume\_data.yml.  
3. **Create Simple Resume Templates:** Instead of one complex cv.qmd, we create a single, generic resume template, resume\_template.qmd. This file's only job is to read the temporary data file and render it using the awesomecv-typst format. It contains no filtering logic itself.  
4. Configure Profiles to Render the Template: Each profile's configuration file (\_quarto-research.yml, etc.) will do two things:  
   a. Specify that it should render the resume\_template.qmd file.  
   b. Define a unique output file name to prevent profiles from overwriting each other's PDFs.  
   **\_quarto-research.yml:**  
   YAML  
   project:  
     render:  
       \- resume\_template.qmd

   format:  
     awesomecv-typst:  
       output-file: "John\_Doe\_Resume\_Research.pdf"

This architecture centralizes all the complex tailoring logic into one clean, maintainable Python script, keeping the Quarto documents simple and focused on presentation.  
To illustrate the superiority of this architecture, the following table compares the two strategies.  
**Table 2: Comparison of Resume Tailoring Strategies**

| Feature | Strategy 1: Conditional Content | Strategy 2: Pre-render Script |
| :---- | :---- | :---- |
| **Flexibility** | Low. This method is effective for showing or hiding entire, self-contained blocks of content. It is poorly suited for filtering individual items within a list (e.g., bullet points) or for dynamically reordering sections. | High. It offers complete programmatic control. The Python script can filter, transform, reorder, or even generate new data on the fly based on any conceivable logic. |
| **Complexity** | Low initial setup cost. However, the complexity grows exponentially as more profiles and filtering rules are added, leading to a convoluted and hard-to-read .qmd file. | Higher initial setup cost, as it requires writing a separate Python script. However, ongoing complexity is low, as all logic is contained in one place. |
| **Maintainability** | Poor. The tailoring logic is scattered throughout the .qmd files within div blocks, making it difficult to understand the overall behavior for any given profile and hard to update without introducing errors. | Excellent. All tailoring logic is centralized in a single, well-structured Python script (generate\_resume\_data.py). This makes it easy to modify, debug, and extend. |
| **Scalability** | Poor. Adding a new resume target (e.g., "management") requires adding new conditional divs throughout the document, further complicating the source file. | Excellent. Adding a new resume target is as simple as adding a new if/elif block to the Python script and creating a corresponding \_quarto-\<new-profile\>.yml file. The core data and templates remain unchanged. |

The pre-render script strategy, while requiring more initial development, is the unequivocally superior architecture for this use case. It aligns perfectly with software engineering best practices by separating concerns, centralizing logic, and creating a system that is robust, maintainable, and scalable for the long term.

## **Section 6: Automating Deployment with GitHub Actions**

The final step is to automate the entire process, from rendering all outputs to publishing them online. This is achieved using GitHub Actions, a powerful continuous integration and continuous deployment (CI/CD) platform built into GitHub.12 The goal is to create a workflow that, upon every push to the  
main branch, automatically builds the website, the comprehensive CV, and all tailored resumes, and then deploys them to GitHub Pages.

### **6.1 Publishing to GitHub Pages: The Target**

GitHub Pages is a free service for hosting static websites directly from a GitHub repository.35 Quarto produces exactly this: a collection of static HTML, CSS, JavaScript, and PDF files. The standard practice for publishing a Quarto project is to configure a GitHub Action to render the project and push the resulting output files to a special  
gh-pages branch. GitHub Pages is then configured to serve the website from this branch.12

### **6.2 Configuring the GitHub Actions Workflow**

The entire CI/CD pipeline is defined in a single YAML file located at .github/workflows/publish.yml. This file specifies the trigger for the workflow, the environment to set up, and the sequence of commands to execute.12  
The workflow must perform several key steps:

1. **Trigger:** The workflow will be configured to run automatically on any push event to the main branch.  
2. **Checkout Code:** The first step in any job is to check out the repository's source code.  
3. **Set up Environment:** The virtual machine running the action needs the complete toolchain installed. This includes setting up Python and installing dependencies from requirements.txt, installing the Quarto CLI, and, crucially, installing the Typst compiler.  
4. **Render All Outputs:** This is the most critical stage. A simple quarto render is insufficient as it would only build the default project (the website). The workflow must explicitly invoke the quarto render command for each desired output artifact, using the appropriate profiles.  
5. **Publish:** The final step involves using a dedicated action to gather all the generated files (the \_site directory and all PDF files) and deploy them to the gh-pages branch.

Here is a complete, annotated workflow file that accomplishes this multi-stage build and deployment process.  
**.github/workflows/publish.yml:**

YAML

\# Name of the workflow  
name: Build and Deploy Quarto Project

\# Controls when the workflow will run  
on:  
  \# Allows manual triggering from the Actions tab  
  workflow\_dispatch:  
  \# Triggers the workflow on push events to the main branch  
  push:  
    branches:  
      \- main

\# A workflow run is made up of one or more jobs that can run sequentially or in parallel  
jobs:  
  build-and-deploy:  
    \# The type of runner that the job will run on  
    runs-on: ubuntu-latest

    \# Grant write permissions to the GITHUB\_TOKEN to allow deployment to gh-pages  
    permissions:  
      contents: write

    steps:  
      \# 1\. Check out the repository code  
      \- name: Check out repository  
        uses: actions/checkout@v4

      \# 2\. Set up Python environment  
      \- name: Set up Python  
        uses: actions/setup-python@v5  
        with:  
          python-version: '3.11'  
      \- name: Install Python dependencies  
        run: |  
          pip install \-r requirements.txt

      \# 3\. Set up Quarto CLI  
      \- name: Set up Quarto  
        uses: quarto-dev/quarto-actions/setup@v2  
        with:  
          \# Use the latest version of Quarto  
          version: latest

      \# 4\. Install Typst compiler (essential for PDF generation)  
      \- name: Install Typst  
        uses: typst-community/setup-typst@v3  
        with:  
          version: 'latest'

      \# 5\. Render all project outputs  
      \- name: Render Website  
        run: quarto render \--output-dir docs

      \- name: Render Comprehensive CV  
        run: |  
          quarto render cv.qmd  
          mkdir \-p docs/cv  
          mv cv.pdf docs/cv/cv.pdf

      \- name: Render Research Resume  
        run: |  
          quarto render \--profile research  
          mv John\_Doe\_Resume\_Research.pdf docs/cv/

      \- name: Render Aerospace Resume  
        run: |  
          quarto render \--profile aerospace  
          mv John\_Doe\_Resume\_Aerospace.pdf docs/cv/  
        
      \- name: Render Data Science Resume  
        run: |  
          quarto render \--profile datascience  
          mv John\_Doe\_Resume\_DataScience.pdf docs/cv/

      \# 6\. Deploy to GitHub Pages  
      \- name: Deploy to GitHub Pages  
        uses: peaceiris/actions-gh-pages@v4  
        with:  
          github\_token: ${{ secrets.GITHUB\_TOKEN }}  
          publish\_dir:./docs  
          \# Use a custom commit message  
          commit\_message: "Deploy: ${{ github.event.head\_commit.message }}"

This workflow demonstrates the necessary multi-stage build process. It renders the website to a docs directory. Then, it renders the CV and each resume PDF individually. After each PDF is created, it is moved into a docs/cv subdirectory. This organization ensures that the final deployment step can publish the entire docs directory, which now contains both the website and all the PDF documents, to GitHub Pages in a clean, structured manner.

### **6.3 Managing Dependencies and Secrets**

For the GitHub Actions workflow to succeed, the environment on the runner must perfectly mirror the local development environment. The requirements.txt file is essential for this, as it lists all necessary Python packages (like pyyaml) for the pip install step.12  
To create this file:  
Execution (Terminal):

Bash

pip freeze \> requirements.txt

This file should be committed to the repository.  
While this project does not initially require secrets, if it were to evolve to include, for example, fetching data from a private API, API keys should never be hardcoded. They should be stored as encrypted secrets in the GitHub repository's settings (Settings \> Secrets and variables \> Actions) and accessed in the workflow file using the ${{ secrets.MY\_SECRET\_NAME }} syntax.

## **Conclusions and Future Directions**

This report has detailed the architecture and implementation of a comprehensive, automated personal branding and professional document generation system using Quarto. By adhering to the principle of a "single source of truth" with a structured YAML data model, this system achieves remarkable efficiency, consistency, and scalability.  
**System Capabilities Summary:**

* **Centralized Data Management:** All personal, professional, and academic information is maintained in a set of clean, human-readable YAML files, completely separating data from presentation.  
* **Dynamic Website Generation:** A professional, multi-page website is generated programmatically. Content updates are driven by changes to the YAML data, eliminating the need for manual HTML or markdown editing.  
* **High-Quality CV Production:** A comprehensive, beautifully typeset CV is produced in PDF format using the powerful awesomecv-typst extension, with content dynamically populated from the central data store.  
* **Tailored Resume Automation:** The system's most powerful feature is its ability to generate multiple, distinct resumes tailored for specific industries or roles. This is achieved through a sophisticated pre-render script that programmatically filters and arranges data based on Quarto Project Profiles.  
* **Fully Automated Deployment:** The entire build and deployment process is automated via GitHub Actions. A single git push triggers the regeneration of the website, the CV, and all tailored resumes, publishing the updated artifacts to GitHub Pages seamlessly.

Future Directions:  
The architecture established here is highly extensible. Several future enhancements could be built upon this foundation:

* **Adding a Blog:** Quarto has excellent support for creating blogs.4 A new  
  \_data/posts.yml could be created, and a listing page could programmatically generate a blog index.  
* **Interactive Visualizations:** For a data scientist or engineer, the website could be enhanced with interactive plots using libraries like Plotly or Altair. Quarto's support for Jupyter allows these to be embedded directly.2  
* **Generating Multiple Formats:** The CV and resumes are currently PDFs. With minor modifications to the format key in the .qmd files, MS Word (.docx) or HTML versions could also be generated as part of the CI/CD pipeline.2  
* **Data from APIs:** The pre-render scripts could be extended to pull data from external APIs. For example, a script could fetch a list of recent GitHub contributions or pull publication data directly from an ORCID profile.

In conclusion, by leveraging the unique capabilities of the Quarto ecosystem, it is possible to construct a highly sophisticated and automated personal content platform. This system not only solves the immediate need for a website, CV, and resumes but also provides a robust and scalable foundation for managing one's professional identity for years to come.

#### **Works cited**

1. Intro to Quarto, accessed July 23, 2025, [https://jjallaire.quarto.pub/intro-to-quarto/](https://jjallaire.quarto.pub/intro-to-quarto/)  
2. Quarto, accessed July 23, 2025, [https://quarto.org/](https://quarto.org/)  
3. R Quarto Tutorial \- How To Create Interactive Markdown Documents \- Appsilon, accessed July 23, 2025, [https://www.appsilon.com/post/r-quarto-tutorial](https://www.appsilon.com/post/r-quarto-tutorial)  
4. Guide – Quarto, accessed July 23, 2025, [https://quarto.org/docs/guide/](https://quarto.org/docs/guide/)  
5. quarto-cli \- PyPI, accessed July 23, 2025, [https://pypi.org/project/quarto-cli/](https://pypi.org/project/quarto-cli/)  
6. Get Started – Quarto, accessed July 23, 2025, [https://quarto.org/docs/get-started/](https://quarto.org/docs/get-started/)  
7. Install Quarto \- Posit Docs, accessed July 23, 2025, [https://docs.posit.co/resources/install-quarto.html](https://docs.posit.co/resources/install-quarto.html)  
8. Typst Documentation, accessed July 23, 2025, [https://typst.app/docs/](https://typst.app/docs/)  
9. typst/typst: A new markup-based typesetting system that is ... \- GitHub, accessed July 23, 2025, [https://github.com/typst/typst](https://github.com/typst/typst)  
10. Quarto \- Visual Studio Marketplace, accessed July 23, 2025, [https://marketplace.visualstudio.com/items?itemName=quarto.quarto](https://marketplace.visualstudio.com/items?itemName=quarto.quarto)  
11. Project Basics \- Quarto, accessed July 23, 2025, [https://quarto.org/docs/projects/quarto-projects.html](https://quarto.org/docs/projects/quarto-projects.html)  
12. GitHub Pages – Quarto, accessed July 23, 2025, [https://quarto.org/docs/publishing/github-pages.html](https://quarto.org/docs/publishing/github-pages.html)  
13. Creating a Website – Quarto, accessed July 23, 2025, [https://quarto.org/docs/websites/](https://quarto.org/docs/websites/)  
14. Project Options \- Quarto, accessed July 23, 2025, [https://quarto.org/docs/reference/projects/options.html](https://quarto.org/docs/reference/projects/options.html)  
15. data whiskeRs | A beginner's guide to building a simple website with ..., accessed July 23, 2025, [https://jadeyryan.com/blog/2024-02-19\_beginner-quarto-netlify/](https://jadeyryan.com/blog/2024-02-19_beginner-quarto-netlify/)  
16. 18 Websites \- Quarto: The Definitive Guide, accessed July 23, 2025, [https://quarto-tdg.org/websites](https://quarto-tdg.org/websites)  
17. Website Options \- Quarto, accessed July 23, 2025, [https://quarto.org/docs/reference/projects/websites.html](https://quarto.org/docs/reference/projects/websites.html)  
18. Document Listings \- Quarto, accessed July 23, 2025, [https://quarto.org/docs/websites/website-listings.html](https://quarto.org/docs/websites/website-listings.html)  
19. Tutorial: Computations – Quarto, accessed July 23, 2025, [https://quarto.org/docs/get-started/computations/rstudio.html](https://quarto.org/docs/get-started/computations/rstudio.html)  
20. 31\. Quarto — Python for Data Science, accessed July 23, 2025, [https://aeturrell.github.io/python4DS/quarto.html](https://aeturrell.github.io/python4DS/quarto.html)  
21. Execution Options \- Quarto, accessed July 23, 2025, [https://quarto.org/docs/computations/execution-options.html](https://quarto.org/docs/computations/execution-options.html)  
22. Article Layout \- Quarto, accessed July 23, 2025, [https://quarto.org/docs/authoring/article-layout.html](https://quarto.org/docs/authoring/article-layout.html)  
23. Quarto Tips and Tricks \- Productive R workflow, accessed July 23, 2025, [https://www.productive-r-workflow.com/quarto-tricks](https://www.productive-r-workflow.com/quarto-tricks)  
24. Quarto Extensions, accessed July 23, 2025, [https://quarto.org/docs/extensions/](https://quarto.org/docs/extensions/)  
25. kazuyanagimoto/quarto-awesomecv-typst: A Quarto \+ Typst ... \- GitHub, accessed July 23, 2025, [https://github.com/kazuyanagimoto/quarto-awesomecv-typst](https://github.com/kazuyanagimoto/quarto-awesomecv-typst)  
26. Managing Extensions \- Quarto, accessed July 23, 2025, [https://quarto.org/docs/extensions/managing.html](https://quarto.org/docs/extensions/managing.html)  
27. How to use QUARTO extensions ? \- General \- Posit Community, accessed July 23, 2025, [https://forum.posit.co/t/how-to-use-quarto-extensions/165572](https://forum.posit.co/t/how-to-use-quarto-extensions/165572)  
28. kazuyanagimoto/typstcv: An automated Quarto \+ Typst CV \- GitHub, accessed July 23, 2025, [https://github.com/kazuyanagimoto/typstcv](https://github.com/kazuyanagimoto/typstcv)  
29. modern-cv – Typst Universe, accessed July 23, 2025, [https://typst.app/universe/package/modern-cv/](https://typst.app/universe/package/modern-cv/)  
30. typstcv: CV for Quarto & Typst \- R packages by kazuyanagimoto (Kazuharu Yanagimoto), accessed July 23, 2025, [https://kazuyanagimoto.r-universe.dev/typstcv](https://kazuyanagimoto.r-universe.dev/typstcv)  
31. Project Profiles – Quarto, accessed July 23, 2025, [https://quarto.org/docs/projects/profiles.html](https://quarto.org/docs/projects/profiles.html)  
32. Creating tutorial worksheets; Quarto profiles for the win\! \- R-bloggers, accessed July 23, 2025, [https://www.r-bloggers.com/2025/07/creating-tutorial-worksheets-quarto-profiles-for-the-win/](https://www.r-bloggers.com/2025/07/creating-tutorial-worksheets-quarto-profiles-for-the-win/)  
33. Project Scripts – Quarto, accessed July 23, 2025, [https://quarto.org/docs/projects/scripts.html](https://quarto.org/docs/projects/scripts.html)  
34. Quarto project scripts are awesomeness \- Chris von Csefalvay, accessed July 23, 2025, [https://chrisvoncsefalvay.com/posts/quarto-project-scripts/](https://chrisvoncsefalvay.com/posts/quarto-project-scripts/)  
35. Publishing Basics \- Quarto, accessed July 23, 2025, [https://quarto.org/docs/publishing/](https://quarto.org/docs/publishing/)  
36. Explore and setup – Making sharable documents with Quarto \- openscapes.github.io, accessed July 23, 2025, [https://openscapes.github.io/quarto-website-tutorial/explore.html](https://openscapes.github.io/quarto-website-tutorial/explore.html)  
37. Gallery \- Quarto, accessed July 23, 2025, [https://quarto.org/docs/gallery/](https://quarto.org/docs/gallery/)