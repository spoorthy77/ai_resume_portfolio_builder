# AI Resume & Portfolio Builder

A full-stack application that leverages AI to generate, enhance, and optimize resumes and cover letters.

## Features

- AI-powered resume generation using Grok API
- Resume optimization and content enhancement
- Cover letter generation
- Portfolio creation and management
- Multiple resume templates
- Export to PDF format
- User authentication system
- Responsive web interface

## Tech Stack

**Backend:**
- Python 3.11
- Flask
- SQLAlchemy ORM
- Grok AI API

**Frontend:**
- React 18
- Tailwind CSS
- Axios

**DevOps:**
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Heroku/AWS deployment ready

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)
- Git

## Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-resume-portfolio-builder.git
cd ai-resume-portfolio-builder
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

### 3. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 4. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

### 5. Run the application

**Option A: Traditional Development**

```bash
# Terminal 1 - Backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm start
```

**Option B: Using Docker Compose**

```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000/api

## Project Structure

```
├── app.py                    # Flask application entry point
├── backend/
│   ├── config.py            # Configuration management
│   ├── routes/              # API endpoints
│   │   ├── ai_routes.py
│   │   ├── auth_routes.py
│   │   └── profile_routes.py
│   └── services/            # Business logic
│       ├── ai_resume_enhancer.py
│       ├── resume_generator.py
│       ├── cover_letter_generator.py
│       └── ...
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API client
│   │   └── App.jsx
│   └── package.json
├── .github/
│   └── workflows/           # GitHub Actions workflows
├── Dockerfile               # Production Docker image
├── docker-compose.yml       # Local development container setup
└── README.md
```

## API Documentation

### Authentication Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Resume Endpoints

- `POST /api/resumes/generate` - Generate resume from profile
- `POST /api/resumes/enhance` - Enhance resume with AI
- `POST /api/resumes/export` - Export resume to PDF

### Profile Endpoints

- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile

### AI Content Endpoints

- `POST /api/ai/generate-content` - Generate content using Grok
- `POST /api/ai/compress-content` - Compress/optimize content

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `GROK_API_KEY` - Grok API authentication key
- `OPENAI_API_KEY` - OpenAI API key (optional)
- `FLASK_ENV` - Development/Production environment
- `SECRET_KEY` - Flask secret key

## GitHub Actions CI/CD

The project includes automated CI/CD pipelines:

### CI Pipeline (`ci-cd.yml`)
- Runs tests on Python 3.10 & 3.11
- Runs frontend build tests
- Security vulnerability scanning with Trivy
- Linting and code quality checks

### Deployment Pipeline (`deploy.yml`)
- Automatic deployment on push to main branch
- Supports Heroku and AWS EC2 deployment
- Slack notifications

### Setting up GitHub Secrets

Add these secrets to your GitHub repository settings:

```
HEROKU_API_KEY      - Your Heroku API key
HEROKU_APP_NAME     - Your Heroku application name
HEROKU_EMAIL        - Your Heroku email
EC2_HOST            - EC2 instance hostname
EC2_USER            - EC2 SSH username
EC2_PRIVATE_KEY     - EC2 SSH private key
SLACK_WEBHOOK       - Slack webhook for notifications
```

## Deployment Options

### Option 1: Heroku Deployment

1. Create a Heroku account and app
2. Add GitHub secrets for Heroku
3. Push to main branch - automatic deployment triggers

### Option 2: Docker-based Deployment

```bash
# Build image
docker build -t ai-resume-portfolio:latest .

# Run container
docker run -p 5000:5000 --env-file .env ai-resume-portfolio:latest
```

### Option 3: AWS EC2

1. Launch an EC2 instance with Docker installed
2. Clone repository on instance
3. Configure GitHub secrets with EC2 details
4. Push to main - automatic deployment via GitHub Actions

## Testing

### Backend Testing

```bash
pip install pytest pytest-cov
pytest backend/tests/ -v
```

### Frontend Testing

```bash
cd frontend
npm test
```

## Contributing

1. Create a feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit changes (`git commit -m 'Add AmazingFeature'`)
3. Push to branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

## Security Notes

- Never commit `.env` files with real API keys
- Use environment variables for secrets
- Keep dependencies updated
- Review GitHub Actions logs for deployment issues
- Enable branch protection rules on main

## Troubleshooting

### Port already in use
```bash
# Kill process on port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

### Docker issues
```bash
# Clear Docker cache
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
```

### Frontend build errors
```bash
# Clear npm cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please open a GitHub issue or contact the maintainers.

---

**Last Updated:** February 2026
