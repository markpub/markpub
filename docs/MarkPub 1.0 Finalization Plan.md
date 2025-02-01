# MarkPub 1.0 Finalization Plan

## Overview

Goal: Release a production-ready 1.0 version of MarkPub with well-documented features, consistent behavior, and clear upgrade paths.

## 1. Documentation Finalization

### Core Documentation
1. `MarkPub User Documentation.md`
   - Complete reference for all features  
   - TODO: document steps to enable GitHub pages  
	   - include `.github/workflows/gh-pagesV1.yml` in `templates` directory
	   - upon initialization include the repo-name in the `.yml` file build command
	   - add instructions in User Guide (or Quickstart) on how to set up GitHub Pages for a MarkPub repository  
   - Installation and configuration
   - Command reference
   - Configuration file reference

2. `MarkPub User Guide.md`
   - Use cases and examples
   - Best practices
   - Step-by-step tutorials

3. Add new sections:
   - Directory exclusion guide
   - Theme management
   - Bluesky comments integration
   - Version upgrade procedures

### Documentation Organization
```
docs/
├── README.md                     # Project overview
├── CHANGELOG.md                  # Version history
├── MIGRATION.md                  # Upgrade guide
├── user/
│   ├── getting-started.md       # Quick start
│   ├── user-documentation.md    # Complete reference
│   └── user-guide.md           # Tutorial style
└── technical/
    ├── theme-guide.md          # Theme development
    └── contributing.md         # Development guide
```

## 2. CSS Standardization

### Style Review
1. Resolve duplicate declarations in `style.css`:
   ```css
   /* CURRENT */
   body {
     font-size: 1.125rem;
     font-size: 1.0rem;
     line-height: 1.6;
     line-height: 1.3;
   }
   
   /* PROPOSED */
   body {
     font-size: 1rem;      /* Base size */
     line-height: 1.4;     /* Compromise for readability */
   }
   ```

### Unit Standardization
1. Create CSS unit guidelines:
   - `rem` for font sizes and related spacing
   - `em` for component-specific spacing
   - `px` for borders and small fixed sizes
   - `%` for layout and responsive elements

### All Pages Layout
1. Implement proven changes from developer.massive.wiki:
   ```css
   /* Add to style.css */
   .allpages-max-width {
       max-width: 83% !important;
   }
   
   /* Table cell sizing */
   #allPagesTableWrapper td {
       padding: 0.5rem 1rem;
   }
   ```

2. Fix responsive behavior:
   - Test hidden sidebar cases
   - Adjust margins for all viewport sizes
   - Document layout structure

## 3. Theme System

### 1.0 Theme Structure
1. Document current Dolce theme:
   - File organization
   - Template variables
   - CSS architecture
   - JavaScript dependencies

2. Create upgrade path for existing sites:
   ```bash
   # Example upgrade script
   markpub theme update
   ```

### Theme Documentation
1. Create theme development guide:
   - Required files
   - Available template variables
   - CSS guidelines
   - Testing requirements

## 4. Code Stability

### Error Handling
1. Add consistent error messages
2. Improve error recovery
3. Document error conditions

### Testing
1. Add test cases for:
   - Configuration options
   - Theme variations
   - Error conditions
   - File handling

### Version Checks
1. Add version compatibility checks
2. Document version requirements
3. Create upgrade detection

## 5. Release Process

### Version 1.0.0
1. Update version numbers:
   ```python
   # markpub.py
   APPVERSION = 'v1.0.0'
   ```

2. Create release notes:
   - New features
   - Breaking changes
   - Migration steps
   - Known issues

### PyPI Package
1. Update package metadata:
   ```toml
   # pyproject.toml
   [tool.poetry]
   name = "markpub"
   version = "1.0.0"
   description = "A static site generator for Markdown with wiki features"
   ```

2. Verify package contents:
   - Documentation
   - Default theme
   - Dependencies

## 6. Post-1.0 Planning

### Theme Package
1. Plan `markpub-themes` package:
   - Package structure
   - Theme API
   - Installation mechanism
   - Update process

### Future Features
1. Document planned enhancements:
   - Additional themes
   - Theme marketplace
   - Advanced integrations
   - Performance improvements

## Timeline

### Week 1: Documentation and CSS
- Complete user documentation
- Standardize CSS
- Fix All Pages layout

### Week 2: Testing and Stabilization
- Add test cases
- Fix reported issues
- Document error conditions

### Week 3: Release Preparation
- Create release notes
- Update version numbers
- Prepare PyPI package

### Week 4: Release and Follow-up
- Release version 1.0.0
- Monitor for issues
- Begin post-1.0 planning

## Success Criteria

Version 1.0.0 requires:
1. Complete documentation
2. Standardized CSS
3. Stable theme system
4. Clear upgrade path
5. Known issues documented
6. Release notes finalized

## Next Steps

1. Review current documentation gaps
2. Begin CSS standardization
3. Create test cases
4. Plan release schedule

