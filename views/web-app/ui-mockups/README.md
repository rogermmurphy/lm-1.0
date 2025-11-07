# Dashboard UI Mockups

This folder contains HTML mockups for the dashboard redesign using Tailwind CSS v3.

## Design System

- **Theme:** Light theme with white background
- **Primary Color:** Blue (#2563EB / blue-600)
- **Font:** Inter (Google Fonts)
- **Border Radius:** rounded-xl (12px), rounded-2xl (16px)
- **Shadows:** shadow-lg, shadow-xl
- **Typography:** Bold headings, medium body text

## Mockups

### 1. dashboard-main-complete.html
Three-column layout showing the overall dashboard structure:
- **Left Sidebar (~250px):** Classes list, Calendar button, Games list
- **Main Content (flex-1):** Dashboard metrics tiles (default view)
- **Right Sidebar (~350px):** AI Chat Bot

### 2. dashboard-metrics-view.html
Detailed view of the metrics tiles in the main content area:
- Past 7-Day Activity
- Games Played
- Active Classes
- Assignments Due

### 3. class-details-view.html
View shown when a class is clicked from the left sidebar:
- Class name and info
- Books/Textbooks section
- Recordings section
- Transcripts section
- Notes section
- Assignments section
- Calendar Events section

### 4. themes/theme-showcase.html
Interactive theme preview showing all 5 available themes:
- **☀️ Bright (Current):** White bg, Gray-900 text, Blue-600 primary
- **🌙 Dark:** Gray-800 bg, Gray-100 text, Blue-500 primary
- **⚫ High Contrast:** Black bg, White text, Yellow-400 accent, 4px borders
- **💗 Pink:** Pink-50 bg, Pink-900 text, Pink-600 primary
- **🌊 Light Blue:** Sky-50 bg, Sky-900 text, Sky-600 primary

## Usage

Open each HTML file in a browser to preview the design. These are static mockups using realistic data to demonstrate layout and styling.

## Next Steps

After approval:
1. Convert mockups to React components
2. Connect to backend APIs
3. Implement interactivity
4. Test with real data
