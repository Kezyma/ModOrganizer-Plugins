# Plugin Finder JSON Generator

The Plugin Finder JSON Generator is a web-based tool that helps plugin authors create manifest files for Plugin Finder.

## Access the Generator

**[Open Plugin Finder JSON Generator](https://kezyma.github.io/index.html?p=pluginfinder-generator)**

## Features

- Load existing JSON files to edit
- Form-based input with validation
- Automatic version number formatting
- MO2 version compatibility dropdowns
- Live JSON preview
- Download generated JSON file

## Usage

### Starting a New Manifest

1. Fill in the **Plugin Information** section:
   - Plugin Name (required)
   - Plugin Author (required)
   - Description (optional, max 350 characters)
   - Documentation URL (optional)
   - GitHub URL (optional)
   - Nexus URL (optional)

2. Add versions using the **Create** button in the Versions section

3. For each version, provide:
   - Version number (using the segmented input fields)
   - Release date
   - MO2 compatibility ranges (optional)
   - Download URL (direct link to zip file)
   - Plugin install paths (required)
   - Locale paths (optional)
   - Data paths for cleanup (optional)
   - Release notes (optional)

4. Review the JSON preview at the bottom

5. Click **Save** to download your manifest file

### Editing an Existing Manifest

1. Use **Select Existing** to load a JSON file from your computer, or
2. Enter a URL to load an existing manifest

The form will populate with the existing values for editing.

### Loading the Example

Click **Example** to load a sample manifest showing the expected format.

## Field Reference

See the [Plugin Finder documentation](pluginfinder.md#adding-your-plugin) for detailed field descriptions.

## Tips

- Version numbers should match the format displayed in Mod Organizer's settings
- Download URLs must point directly to the zip file, not a download page
- Keep descriptions under 350 characters as some themes truncate longer text
- Test your download URL before submitting
