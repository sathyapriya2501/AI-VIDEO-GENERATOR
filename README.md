# AI Video Generator Agent

> **Project Status:** Prototype / Active Development

AI Video Generator Agent is an internship project that converts a text
prompt into a short video using an AI scene planner, text-to-speech,
image-based scene composition, and FFmpeg rendering.

## Project Overview

The long-term goal is:

``` text
User Prompt
    ↓
AI Scene Planner
    ↓
Dynamic Asset Selection
    ↓
Missing Asset Generation
    ↓
Text-to-Speech
    ↓
Scene Composition
    ↓
FFmpeg Rendering
    ↓
Final MP4
```

### Current Working Pipeline

The currently verified prototype works as:

``` text
User Prompt
    ↓
Groq AI Scene Planner
    ↓
Tamil / English Script
    ↓
edge-tts Voice Generation
    ↓
Sample Image-Based Scene Composition
    ↓
FFmpeg Rendering
    ↓
Final MP4
    ↓
React Frontend Display
```

The dynamic asset-selection and missing-asset-generation stages are
planned improvements and are not yet fully implemented.

------------------------------------------------------------------------

## Current Features

### Implemented

-   AI scene planning using Groq
-   Tamil and English script generation
-   Structured scene JSON generation
-   Tamil/English text-to-speech using `edge-tts`
-   Image-based avatar composition
-   Background image composition
-   Prop image composition
-   FFmpeg-based video rendering
-   Audio + video combination
-   Flask backend API
-   React + Vite frontend
-   Generated audio playback in the frontend
-   Generated MP4 display in the frontend
-   Local video serving through Flask
-   Basic scene information display

### Not Yet Fully Implemented

-   Fully dynamic asset selection based on every generated scene
-   Automatic missing-asset generation
-   True talking-avatar animation
-   Lip synchronization
-   Full dynamic camera-motion rendering
-   Multi-scene timeline generation
-   Complete one-click automated pipeline
-   Production deployment

------------------------------------------------------------------------

## Example Use Case

Example prompt:

``` text
Create a 30-second video of a farmer explaining water conservation in a Tamil Nadu village.
```

The AI Scene Planner can generate information such as:

``` text
Character: Farmer
Background: Village
Action: Talk
Expression: Neutral
Prop: Water Pot
Camera: Wide Shot
Language: Tamil
Voice: Male
```

The generated Tamil script is then passed to the text-to-speech system.

------------------------------------------------------------------------

## Sample Assets

The current prototype uses sample image assets such as:

``` text
assets/
├── avatars/
│   └── farmer.jpg
│
├── backgrounds/
│   └── village.jpg
│
└── props/
    └── water_pot.jpg
```

Sample verified dimensions:

  Asset             Approx. Size
  --------------- --------------
  farmer.jpg           640 × 640
  village.jpg          554 × 361
  water_pot.jpg       736 × 1104

Additional characters, backgrounds, and props can be added as the asset
system becomes dynamic.

> Make sure any asset added to the repository is appropriate for
> redistribution and does not violate copyright or licensing
> restrictions.

------------------------------------------------------------------------

## Current Testing

The following parts of the prototype have been tested locally:

### Backend

Health endpoint:

``` text
GET /
```

Expected response:

``` text
AI Video Generator Backend is Running!
```

### Scene Planning

``` text
POST /plan-scene
```

Tested with Tamil and English prompts.

The API returns structured scene information including:

-   duration
-   language
-   character
-   background
-   script
-   action
-   expression
-   props
-   camera
-   voice

### Voice Generation

``` text
POST /generate-audio
```

Tamil male voice generation has been successfully tested.

Generated file:

``` text
output/scene_audio.mp3
```

### Video Rendering

FFmpeg rendering has been successfully tested with the sample assets and
generated audio.

A verified sample output was approximately:

``` text
Resolution: 1280 × 720
Video: H.264
Audio: AAC
Duration: approximately 21 seconds
```

Actual duration and output content can change depending on the generated
script and audio.

### Frontend

The React frontend has been tested with the following workflow:

``` text
Enter Prompt
    ↓
Generate Scene
    ↓
Generate Voice
    ↓
Generate Video
    ↓
View MP4
```

------------------------------------------------------------------------

## Important Current Limitation

The current renderer still uses sample asset paths for composition.

For example, the prototype renderer currently works with assets such as:

``` text
farmer.jpg
village.jpg
water_pot.jpg
```

Therefore, changing the AI-generated character/background/prop values
does not yet automatically change the rendered assets.

For example, the Scene Planner may generate:

``` text
Character: Doctor
Background: Hospital
```

but the current renderer does not automatically locate and use
`doctor.jpg` and `hospital.jpg`.

This is one of the next major implementation tasks.

------------------------------------------------------------------------

## Tech Stack

### Backend

-   Python
-   Flask
-   Flask-CORS
-   OpenAI-compatible Python client
-   Groq API
-   python-dotenv
-   edge-tts

### Frontend

-   React
-   Vite
-   JavaScript
-   HTML
-   CSS

### Video

-   FFmpeg
-   FFprobe

### Development

-   Git
-   GitHub
-   Visual Studio Code

------------------------------------------------------------------------

## Project Structure

``` text
AI-VIDEO-GENERATOR/
│
├── backend/
│   ├── app.py
│   ├── tts.py
│   ├── scene_composer.py
│   ├── asset_selector.py
│   ├── requirements.txt
│   ├── .env
│   └── venv/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── ...
│   ├── package.json
│   ├── package-lock.json
│   └── node_modules/
│
├── assets/
│   ├── avatars/
│   ├── backgrounds/
│   ├── props/
│   └── asset_metadata.json
│
├── output/
│   └── generated media files
│
├── .gitignore
├── README.md
└── ...
```

### Files that should NOT be committed

``` text
backend/venv/
frontend/node_modules/
.env
generated output media
cache files
temporary files
```

------------------------------------------------------------------------

## Prerequisites

Install the following before running the project:

-   Python 3.12 or later
-   Node.js 20 or later
-   npm
-   Git
-   FFmpeg
-   FFprobe
-   A Groq API key

Check installations:

``` cmd
python --version
node --version
npm --version
git --version
ffmpeg -version
ffprobe -version
```

------------------------------------------------------------------------

## Backend Setup

Open Command Prompt or PowerShell:

``` cmd
cd /d D:\AI-VIDEO-GENERATOR\backend
```

Create the virtual environment:

``` cmd
python -m venv venv
```

Activate it:

``` cmd
venv\Scripts\activate
```

Install dependencies:

``` cmd
pip install -r requirements.txt
```

If the requirements file does not yet exist, the expected core packages
are:

``` text
Flask
flask-cors
python-dotenv
openai
edge-tts
```

------------------------------------------------------------------------

## Environment Variables

Create:

``` text
backend/.env
```

Add:

``` env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit the real API key.

The `.env` file should be ignored by Git.

A safe repository can optionally include:

``` text
.env.example
```

with:

``` env
GROQ_API_KEY=your_groq_api_key_here
```

------------------------------------------------------------------------

## Frontend Setup

Open another terminal:

``` cmd
cd /d D:\AI-VIDEO-GENERATOR\frontend
```

Install dependencies:

``` cmd
npm install
```

Start the Vite development server:

``` cmd
npm run dev
```

The frontend normally runs at:

``` text
http://localhost:5173
```

------------------------------------------------------------------------

## Running the Project

Two terminals are normally required.

### Terminal 1 --- Backend

``` cmd
cd /d D:\AI-VIDEO-GENERATOR\backend
venv\Scripts\activate
python app.py
```

Backend:

``` text
http://127.0.0.1:5000
```

### Terminal 2 --- Frontend

``` cmd
cd /d D:\AI-VIDEO-GENERATOR\frontend
npm run dev
```

Frontend:

``` text
http://localhost:5173
```

------------------------------------------------------------------------

## How to Use

1.  Open the React frontend.
2.  Enter a video prompt.
3.  Click **Generate Scene**.
4.  Review the generated scene plan.
5.  Click **Generate Voice**.
6.  Listen to the generated audio.
7.  Generate/render the video using the current prototype workflow.
8.  View the final MP4 in the frontend.

------------------------------------------------------------------------

## Backend API

### `GET /`

Checks whether the backend is running.

### `POST /plan-scene`

Generates a structured scene plan from a user prompt.

Example request:

``` json
{
  "prompt": "Create a short Tamil video of a farmer explaining water conservation."
}
```

### `POST /generate-audio`

Generates speech from the generated script.

Example:

``` json
{
  "script": "வணக்கம் நண்பர்களே!",
  "voice": {
    "gender": "Male",
    "language": "Tamil"
  }
}
```

### `GET /video/<filename>`

Serves generated media from the output directory.

Example:

``` text
http://127.0.0.1:5000/video/scene_audio.mp3
```

------------------------------------------------------------------------

## Git Ignore Policy

The repository should ignore:

``` gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.venv/
venv/
env/

# Environment / secrets
.env
.env.*
!.env.example

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
pnpm-debug.log*

# Build
dist/
build/

# Generated output
output/*
!output/.gitkeep

# Cache / temporary files
*.tmp
*.temp
*.log
.pytest_cache/
.mypy_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
desktop.ini
```

Small project assets can be committed when their licensing permits it.

------------------------------------------------------------------------

## GitHub Team Workflow

Use `main` as the stable branch.

Recommended structure:

``` text
main
  ↓
feature branch
  ↓
development
  ↓
pull request
  ↓
main
```

### Example

Create a feature branch:

``` cmd
git checkout -b feature/dynamic-assets
```

Work on the feature and test it.

Check changes:

``` cmd
git status
```

Review the actual changes:

``` cmd
git diff
```

Stage:

``` cmd
git add .
```

Commit:

``` cmd
git commit -m "Add dynamic asset selection"
```

Before pushing, update your branch:

``` cmd
git pull --rebase origin main
```

Then push:

``` cmd
git push -u origin feature/dynamic-assets
```

Create a Pull Request on GitHub and merge it into `main` after review.

------------------------------------------------------------------------

## Safe Git Habits

### Before starting work

``` cmd
git status
git pull origin main
```

### Before committing

``` cmd
git status
git diff
```

### After completing a small feature

``` cmd
git add .
git commit -m "Describe the completed change"
```

### Before pushing

Make sure:

-   `.env` is not staged
-   `venv` is not staged
-   `node_modules` is not staged
-   generated videos/audio are not staged
-   the application still runs

Then:

``` cmd
git push
```

### Avoid losing local work

Before risky Git operations, make sure your changes are committed or
safely stashed.

``` cmd
git status
```

If you need a temporary backup:

``` cmd
git stash
```

Restore later:

``` cmd
git stash pop
```

A normal commit is usually the better long-term backup for completed
work.

------------------------------------------------------------------------

## Recommended Commit Messages

Use small, meaningful commits.

Examples:

``` text
Add Groq scene planner
Add Tamil TTS generation
Add sample scene composer
Add React scene display
Add video playback to frontend
Add dynamic asset metadata
Fix FFmpeg video rendering
Update project README
```

Avoid vague commits such as:

``` text
update
changes
final
new
test
```

------------------------------------------------------------------------

## Future Roadmap

### Phase 1 --- Core Prototype

-   [x] Groq scene planning
-   [x] Tamil/English script generation
-   [x] Text-to-speech
-   [x] Sample image composition
-   [x] FFmpeg rendering
-   [x] React frontend
-   [x] MP4 display

### Phase 2 --- Dynamic Assets

-   [ ] Dynamic character selection
-   [ ] Dynamic background selection
-   [ ] Dynamic prop selection
-   [ ] Asset metadata lookup
-   [ ] Safe fallback assets
-   [ ] Add more characters
-   [ ] Add more backgrounds
-   [ ] Add more props

### Phase 3 --- AI Asset Generation

-   [ ] Detect missing assets
-   [ ] Generate missing images
-   [ ] Save generated assets
-   [ ] Add generated assets to asset metadata

### Phase 4 --- Animation

-   [ ] Better avatar movement
-   [ ] Talking-avatar animation
-   [ ] Lip-sync
-   [ ] Expression animation
-   [ ] Dynamic camera movement
-   [ ] Scene transitions

### Phase 5 --- Complete Video Pipeline

-   [ ] Multi-scene video generation
-   [ ] Automatic scene timeline
-   [ ] Automatic voice generation
-   [ ] Automatic rendering
-   [ ] Automatic output naming
-   [ ] Output cleanup
-   [ ] Better error handling
-   [ ] One-click generation

### Phase 6 --- Team / Production Improvements

-   [ ] Automated tests
-   [ ] Better API validation
-   [ ] Logging
-   [ ] Configuration management
-   [ ] Deployment
-   [ ] CI/CD
-   [ ] Documentation improvements

------------------------------------------------------------------------

## Current Project Stage

The project is currently at the **working prototype stage**.

The core local pipeline has been verified:

``` text
Prompt
  ↓
Groq Scene Planning
  ↓
Script
  ↓
Tamil/English TTS
  ↓
Image-Based Scene
  ↓
FFmpeg
  ↓
MP4
  ↓
React Frontend
```

The next major engineering task is to make the renderer use the
AI-generated scene values dynamically instead of relying on fixed sample
assets.

------------------------------------------------------------------------

## Team Contribution Guidelines

Before modifying the project:

1.  Pull the latest `main`.
2.  Create a feature branch.
3.  Make one focused change.
4.  Test locally.
5.  Commit the change.
6.  Push the feature branch.
7.  Open a Pull Request.
8.  Review before merging into `main`.

Example:

``` cmd
git checkout main
git pull origin main
git checkout -b feature/my-feature
```

After development:

``` cmd
git status
git add .
git commit -m "Implement my feature"
git push -u origin feature/my-feature
```

------------------------------------------------------------------------

## Important Security Notes

Never commit:

``` text
GROQ_API_KEY
.env
passwords
tokens
private credentials
personal access keys
```

If an API key is accidentally pushed to GitHub, revoke/rotate the key
immediately and replace it with a new key.

------------------------------------------------------------------------

## Development Notes

Generated files such as:

``` text
output/scene_audio.mp3
output/scene.mp4
output/scene_zoom.mp4
```

are reproducible build artifacts and should normally remain outside Git.

The source code, configuration templates, asset metadata, and small
permitted sample assets should remain version controlled.

------------------------------------------------------------------------

## License

This project is currently an internship/project prototype.

Add an appropriate open-source license here if the project is later
intended for public redistribution.

------------------------------------------------------------------------

## Current Status Summary

**Status:** Working Prototype

**Core AI planning:** Working

**Tamil/English TTS:** Working

**Sample image composition:** Working

**FFmpeg rendering:** Working

**React frontend:** Working

**Final MP4 display:** Working

**Dynamic asset selection:** In progress

**Missing asset generation:** Planned

**Talking avatar / lip-sync:** Planned

**Multi-scene generation:** Planned

**Production deployment:** Planned
