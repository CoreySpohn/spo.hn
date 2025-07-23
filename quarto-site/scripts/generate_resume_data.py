#!/usr/bin/env python3
"""
Pre-render script for generating tailored resume data based on the active Quarto profile.
This script reads the QUARTO_PROFILE environment variable and filters the master YAML data
accordingly, writing the filtered data to temporary files for the resume template to use.
"""

import os
import yaml
import copy
from pathlib import Path

def filter_by_tags(items, target_tags):
    """Filter a list of items based on their tags."""
    filtered = []
    for item in items:
        # Get tags from the item
        item_tags = item.get('tags', [])
        # Check if any of the target tags are in the item's tags
        if any(tag in item_tags for tag in target_tags):
            filtered.append(item)
    return filtered

def filter_achievements(jobs, target_tags):
    """Filter job achievements based on tags."""
    filtered_jobs = []
    for job in jobs:
        filtered_job = copy.deepcopy(job)
        # Filter achievements
        achievements = job.get('achievements', [])
        filtered_achievements = filter_by_tags(achievements, target_tags)
        filtered_job['achievements'] = filtered_achievements
        # Only include job if it has achievements after filtering
        if filtered_achievements:
            filtered_jobs.append(filtered_job)
    return filtered_jobs

def filter_skills(skill_sets, target_fields):
    """Filter skills based on field tags."""
    filtered_skill_sets = []
    for skill_set in skill_sets:
        filtered_set = copy.deepcopy(skill_set)
        skills = skill_set.get('skills', [])
        filtered_skills = []
        for skill in skills:
            skill_fields = skill.get('field', [])
            if any(field in skill_fields for field in target_fields):
                filtered_skills.append(skill)
        filtered_set['skills'] = filtered_skills
        # Only include skill set if it has skills after filtering
        if filtered_skills:
            filtered_skill_sets.append(filtered_set)
    return filtered_skill_sets

def main():
    # Get the active profile from environment variable
    profile = os.environ.get('QUARTO_PROFILE', 'default')
    print(f"Generating resume data for profile: {profile}")
    
    # Define tag mappings for each profile
    profile_configs = {
        'research': {
            'job_tags': ['research', 'academic', 'teaching', 'publication'],
            'skill_fields': ['research', 'data-science', 'mathematics', 'optimization'],
            'project_tags': ['research', 'open-source', 'algorithms', 'mathematics'],
            'section_order': ['education', 'publications', 'experience', 'projects', 'skills']
        },
        'aerospace': {
            'job_tags': ['aerospace', 'nasa', 'mission-planning', 'optics', 'simulation'],
            'skill_fields': ['aerospace', 'simulation', 'engineering', 'optics'],
            'project_tags': ['aerospace', 'simulation', 'optics', 'nasa'],
            'section_order': ['experience', 'education', 'projects', 'skills', 'publications']
        },
        'datascience': {
            'job_tags': ['data-science', 'machine-learning', 'python', 'software-development', 'optimization'],
            'skill_fields': ['data-science', 'machine-learning', 'database', 'python'],
            'project_tags': ['data-science', 'data-visualization', 'python', 'jax', 'optimization'],
            'section_order': ['experience', 'education', 'projects', 'skills']
        },
        'default': {
            'job_tags': None,  # Include all
            'skill_fields': None,  # Include all
            'project_tags': None,  # Include all
            'section_order': ['experience', 'education', 'projects', 'publications', 'skills']
        }
    }
    
    # Get configuration for current profile
    config = profile_configs.get(profile, profile_configs['default'])
    
    # Load all master data files
    data_dir = Path('_data')
    
    with open(data_dir / 'personal.yml', 'r') as f:
        personal_data = yaml.safe_load(f)
    
    with open(data_dir / 'experience.yml', 'r') as f:
        experience_data = yaml.safe_load(f)
    
    with open(data_dir / 'education.yml', 'r') as f:
        education_data = yaml.safe_load(f)
    
    with open(data_dir / 'skills.yml', 'r') as f:
        skills_data = yaml.safe_load(f)
    
    with open(data_dir / 'projects.yml', 'r') as f:
        projects_data = yaml.safe_load(f)
    
    with open(data_dir / 'publications.yml', 'r') as f:
        publications_data = yaml.safe_load(f)
    
    # Filter data based on profile
    filtered_data = {
        'personal': personal_data,
        'education': education_data,
        'section_order': config['section_order']
    }
    
    # Filter experience
    if config['job_tags']:
        jobs = experience_data.get('jobs', [])
        filtered_jobs = filter_achievements(jobs, config['job_tags'])
        filtered_data['experience'] = {'jobs': filtered_jobs}
    else:
        filtered_data['experience'] = experience_data
    
    # Filter skills
    if config['skill_fields']:
        skill_sets = skills_data.get('skill_sets', [])
        filtered_skill_sets = filter_skills(skill_sets, config['skill_fields'])
        filtered_data['skills'] = {'skill_sets': filtered_skill_sets}
    else:
        filtered_data['skills'] = skills_data
    
    # Filter projects
    if config['project_tags']:
        projects = projects_data.get('projects', [])
        filtered_projects = filter_by_tags(projects, config['project_tags'])
        filtered_data['projects'] = {'projects': filtered_projects[:5]}  # Limit to 5
    else:
        filtered_data['projects'] = {'projects': projects_data.get('projects', [])[:5]}
    
    # Publications - include for research profile, limit for others
    if profile == 'research':
        filtered_data['publications'] = publications_data
    elif profile in ['aerospace', 'default']:
        # Include only top 3 publications
        pubs = publications_data.get('publications', [])
        filtered_data['publications'] = {'publications': pubs[:3]}
    else:
        # Data science profile - no publications
        filtered_data['publications'] = {'publications': []}
    
    # Write filtered data to temporary file
    output_file = data_dir / 'tmp_resume_data.yml'
    with open(output_file, 'w') as f:
        yaml.dump(filtered_data, f, default_flow_style=False, sort_keys=False)
    
    print(f"Generated filtered resume data at: {output_file}")
    
    # Also create individual filtered files for easier access
    for key, value in filtered_data.items():
        if key not in ['section_order']:
            output_file = data_dir / f'tmp_{key}.yml'
            with open(output_file, 'w') as f:
                yaml.dump(value, f, default_flow_style=False, sort_keys=False)

if __name__ == '__main__':
    main()