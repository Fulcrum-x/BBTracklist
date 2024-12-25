# Spotify Album BBCode Generator

A tool to generate BBCode formatted album descriptions using Spotify data. The tool securely stores Spotify API credentials using Windows DPAPI encryption.

## Requirements
- Python 3.6+
- Windows OS (for DPAPI encryption)
- Spotify Developer Account

## Installation
1. Clone this repository
2. Install requirements:
```bash
pip install -r requirements.txt
```
3. Get Spotify API Credentials:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new application
   - Get your Client ID and Client Secret

## Usage
1. Run `run.bat`
2. On first run, enter your Spotify API credentials (they will be securely stored)
3. Enter artist name and album name
4. BBCode will be generated and automatically copied to your clipboard

## Features
- Secure credential storage using Windows DPAPI
- Automatic clipboard copying
- Track duration formatting
- Total album length calculation
- Support for featured artists
- BBCode formatting optimized for music sites

## Files
- `run.bat` - Main launcher script
- `album_bbcode.py` - Main album info fetcher and BBCode generator
- `credentials_manager.py` - Handles secure storage of Spotify credentials
- `credential_setup.py` - Command-line interface for credential management

## Dependencies
- spotipy
- pywin32