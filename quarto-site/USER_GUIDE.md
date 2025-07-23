# Quarto Personal Website & CV/Resume System - User Guide

## Overview

This system provides a unified solution for generating your personal website, CV, and tailored resumes from a single set of YAML data files. Built with Quarto, it allows you to maintain all your professional information in one place while generating multiple output formats.

## System Components

### 1. Data Files (`_data/`)
All your professional information is stored in YAML files:

- **`personal.yml`**: Contact information, bio, and social media links
- **`experience.yml`**: Work history with tagged achievements 
- **`education.yml`**: Academic qualifications
- **`skills.yml`**: Technical skills organized by category
- **`projects.yml`**: Portfolio projects with descriptions
- **`publications.yml`**: Academic papers and publications

### 2. Website Pages
The website automatically generates pages from your data:
- Homepage (index.qmd)
- Projects showcase
- Experience timeline  
- Skills grid
- Publications list

### 3. CV/Resume System
- **Full CV**: Complete academic/professional record
- **Tailored Resumes**: Profile-based filtering for specific job applications

## Getting Started

### Prerequisites
1. Python 3.x installed
2. Git for version control

### Installation

1. **Install Quarto**:
   ```bash
   # Download and extract Quarto
   wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.7.31/quarto-1.7.31-linux-amd64.tar.gz
   tar -xzf quarto-1.7.31-linux-amd64.tar.gz
   export PATH="$PWD/quarto-1.7.31/bin:$PATH"
   ```

2. **Install Python dependencies**:
   ```bash
   pip install pyyaml
   ```

3. **For CV generation, install Typst**:
   ```bash
   wget https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz
   tar -xf typst-x86_64-unknown-linux-musl.tar.xz
   export PATH="$PWD/typst-x86_64-unknown-linux-musl:$PATH"
   ```

## Updating Your Information

### 1. Personal Information
Edit `_data/personal.yml`:
```yaml
info:
  name: "Your Name"
  firstname: "First"
  lastname: "Last"
  position: "Your Title"
  summary: |
    Your professional summary here...

contact:
  email: "your.email@example.com"
  phone: "+1 (555) 123-4567"
  address: "City, State"

social:
  github: "yourusername"
  linkedin: "yourusername"
  orcid: "0000-0000-0000-0000"
```

### 2. Experience
Edit `_data/experience.yml`:
```yaml
jobs:
  - title: "Job Title"
    company: "Company Name"
    location: "City, State"
    start_date: "2023-01"
    end_date: "Present"
    achievements:
      - description: "What you accomplished"
        tags: ["research", "python", "leadership"]
```

**Important**: Use tags to categorize achievements for resume filtering:
- `research`, `teaching` - Academic roles
- `aerospace`, `mission-planning` - Industry-specific
- `python`, `data-science` - Technical skills
- `leadership`, `communication` - Soft skills

### 3. Skills
Edit `_data/skills.yml`:
```yaml
skill_sets:
  - category: "Programming Languages"
    skills:
      - name: "Python"
        level: 5  # 1-5 scale
        field: ["data-science", "research"]
```

## Building the Website

### Generate Everything
```bash
quarto render
```

### Preview Locally
```bash
quarto preview
```
Then open http://localhost:4444 in your browser.

### Generate Specific Pages
```bash
quarto render index.qmd projects.qmd
```

## Creating Tailored Resumes

The system supports profile-based resume generation. Define profiles in the Quarto configuration files:

### 1. Research-Focused Resume
Create `_quarto-research.yml`:
```yaml
project:
  render:
    - resume_template.qmd
format:
  awesomecv-typst:
    output-file: "YourName_Resume_Research.pdf"
```

### 2. Generate with Profile
```bash
QUARTO_PROFILE=research quarto render
```

The pre-render script will automatically filter your experience and projects based on the tags relevant to that profile.

## Customization

### Website Styling
Edit `styles.css` to customize:
- Colors and fonts
- Layout spacing
- Component styles

### Resume Templates
The CV uses the `awesomecv-typst` format. Customize in the YAML frontmatter:
```yaml
style:
  color-accent: "516db0"  # Accent color in hex
```

## Deployment

### GitHub Pages

1. **Enable GitHub Actions**: The included workflow (`.github/workflows/publish.yml`) automatically builds and deploys your site.

2. **Configure Repository**:
   - Go to Settings → Pages
   - Source: Deploy from a branch
   - Branch: gh-pages

3. **Update Site URL**: Edit `_quarto.yml`:
   ```yaml
   website:
     site-url: "https://yourusername.github.io/your-repo"
   ```

### Manual Deployment
```bash
quarto publish gh-pages
```

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Install all Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **CV generation fails**: Ensure you have:
   - Valid FontAwesome icon strings (e.g., "fa envelope", "fa brands github")
   - No profile photo specified (or provide a valid image)

3. **Python code not executing**: Check that PyYAML is installed

### Tips

- **Test locally** before deploying
- **Use descriptive tags** for better resume filtering
- **Keep achievements concise** - one line each
- **Update regularly** - treat it as a living document

## Project Structure

```
quarto-site/
├── _data/                 # Your professional data
│   ├── personal.yml
│   ├── experience.yml
│   ├── education.yml
│   ├── skills.yml
│   ├── projects.yml
│   └── publications.yml
├── _site/                 # Generated website
├── scripts/
│   └── generate_resume_data.py  # Resume filtering
├── _quarto.yml           # Main configuration
├── _quarto-*.yml         # Profile configurations
├── index.qmd             # Homepage
├── projects.qmd          # Projects page
├── experience.qmd        # Experience page
├── skills.qmd            # Skills page
├── publications.qmd      # Publications page
└── styles.css            # Custom styling
```

## Advanced Features

### Adding New Sections
1. Create a new YAML file in `_data/`
2. Create a corresponding `.qmd` page
3. Add to navigation in `_quarto.yml`

### Custom Resume Profiles
1. Define tag sets for different industries
2. Create profile-specific Quarto configs
3. Generate targeted resumes with relevant content

### Automation
The GitHub Actions workflow automatically:
- Builds the website on every push
- Generates all resume variants
- Deploys to GitHub Pages

---

## Next Steps

1. **Customize your data** in the `_data/` directory
2. **Preview locally** with `quarto preview`
3. **Deploy to GitHub Pages** by pushing to your repository
4. **Share your site** and download tailored resumes as needed

For questions or issues, consult the Quarto documentation at https://quarto.org/