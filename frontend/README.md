# React Frontend

Modern React-based frontend with Tailwind CSS styling.

## Setup

```bash
cd frontend
npm install
npm start
```

## Features

### ✅ Implemented
- **React 18** - Latest React with hooks
- **React Router v6** - SPA navigation
- **Tailwind CSS** - Utility-first styling
- **Context API** - Global state management
- **Axios** - HTTP client for API calls
- **React Hot Toast** - Notifications
- **Heroicons** - Beautiful SVG icons

### 📦 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Header.jsx      # Navigation header
│   └── Form.jsx        # Form components
├── pages/              # Page components
│   ├── Dashboard.jsx   # Main dashboard
│   ├── Login.jsx       # Login page
│   └── Resume.jsx      # Resume builder
├── context/            # State management
│   └── AppContext.jsx  # Global app context
├── services/           # API services
│   └── api.js         # Axios API calls
├── App.jsx             # Main app component
├── index.css           # Tailwind styles
└── index.js            # Entry point
```

## Key Components

### Header
- Responsive navigation
- Mobile menu toggle
- User authentication links

### Dashboard
- Feature grid (Resume, Portfolio, Cover Letter, AI Enhancement)
- Stats display
- Quick navigation

### Resume Generator
- Template selection (Professional, Modern, Simple, Technical)
- Format selection (PDF, DOCX, HTML)
- Live preview
- Download functionality

### Form Components
- FormInput - Text input with error handling
- FormTextarea - Multi-line input
- FormSelect - Dropdown selection
- Button - Customizable button component
- Card - Reusable card container

## API Integration

All API calls are handled through `/src/services/api.js`:

```javascript
// Example usage
import { resumeAPI } from './services/api';

const response = await resumeAPI.generateResume(data, template, format);
```

## Styling with Tailwind CSS

- Utility-first approach
- Custom components in `index.css`
- Color scheme: Blue (#0066ff) and Purple (#9333ea)
- Responsive design with breakpoints

## State Management

Using React Context API with custom hooks:

```javascript
import { useApp } from './context/AppContext';

const { user, profile, loading } = useApp();
```

## Environment Variables

```env
REACT_APP_API_URL=http://localhost:5000/api
```

## Running Locally

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```

3. **Build for production**
   ```bash
   npm run build
   ```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
