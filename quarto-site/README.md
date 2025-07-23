# Quarto Personal Website & CV/Resume System

A modern, data-driven system for generating your personal website, CV, and tailored resumes from a single source of truth.

## 🚀 Quick Start

1. **Run the setup script**:
   ```bash
   ./setup.sh
   ```

2. **Set your PATH**:
   ```bash
   export PATH="$PWD/quarto-1.7.31/bin:$PWD/typst-x86_64-unknown-linux-musl:$PATH"
   ```

3. **Edit your data** in `_data/`:
   - `personal.yml` - Contact info and bio
   - `experience.yml` - Work history
   - `education.yml` - Academic background
   - `skills.yml` - Technical skills
   - `projects.yml` - Portfolio items
   - `publications.yml` - Papers and articles

4. **Preview your site**:
   ```bash
   quarto preview
   ```

5. **Build everything**:
   ```bash
   quarto render
   ```

## 📁 Project Structure

```
_data/          # Your professional data (YAML files)
_site/          # Generated website output
scripts/        # Helper scripts
*.qmd           # Page templates
_quarto*.yml    # Configuration files
```

## 📖 Documentation

See [`USER_GUIDE.md`](USER_GUIDE.md) for comprehensive documentation including:
- Detailed setup instructions
- Data file schemas
- Customization options
- Deployment guide
- Troubleshooting tips

## 🎯 Features

- **Single Source of Truth**: Maintain your data in one place
- **Multiple Outputs**: Website, CV, and tailored resumes
- **Tag-Based Filtering**: Create targeted resumes for different roles
- **Modern Design**: Clean, responsive website with dark mode
- **GitHub Actions**: Automated building and deployment

## 🛠️ Troubleshooting

If you encounter issues:
1. Ensure Python 3 and PyYAML are installed
2. Check that all YAML files are valid
3. For CV issues, verify FontAwesome icon format
4. See the full troubleshooting guide in `USER_GUIDE.md`

## 📝 License

This project is open source. Feel free to customize and use for your own portfolio!