console.log("Frontend loaded successfully");

let availableTemplates = {};
let availableFormats = {};

// Load templates and formats on page load
async function loadTemplates() {
    try {
        const response = await fetch('/api/ai/templates');
        if (response.ok) {
            const data = await response.json();
            availableTemplates = data.templates;
        }
    } catch (error) {
        console.error('Error loading templates:', error);
    }
}

async function loadFormats() {
    try {
        const response = await fetch('/api/ai/export-formats');
        if (response.ok) {
            const data = await response.json();
            availableFormats = data.formats;
        }
    } catch (error) {
        console.error('Error loading formats:', error);
    }
}

// Call on page load
document.addEventListener('DOMContentLoaded', () => {
    loadTemplates();
    loadFormats();
});

async function generateResume() {
    try {
        // Show template and format selection modal
        const selection = await showTemplateAndFormatSelector();
        if (!selection) return; // User cancelled

        const { template, format } = selection;

        const response = await fetch('/api/ai/generate-resume', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                template: template,
                format: format
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `HTTP error! status: ${response.status}`);
        }

        // Handle file downloads for binary formats
        if (format === 'pdf' || format === 'docx') {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;

            const formatInfo = availableFormats.find(f => f.format === format);
            const extension = formatInfo ? formatInfo.extension : '.txt';
            a.download = `resume_${Date.now()}${extension}`;

            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            alert(`Resume downloaded successfully as ${format.toUpperCase()}!`);
        } else {
            // Handle text format
            const data = await response.json();
            console.log('Resume generated:', data);
            
            // Check if it's HTML format
            if (data.format === 'html') {
                displayHTMLContent('Resume', data.resume);
            } else {
                displayContent('Resume', data.resume);
            }
        }
    } catch (error) {
        console.error('Error generating resume:', error);
        alert('Error generating resume: ' + error.message);
    }
}

async function generateCoverLetter() {
    try {
        const jobTitle = prompt('Enter target job title (optional):', '');
        const companyName = prompt('Enter company name (optional):', '');
        
        const requestBody = {};
        if (jobTitle) requestBody.job_title = jobTitle;
        if (companyName) requestBody.company_name = companyName;
        
        const response = await fetch('/api/ai/generate-cover-letter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Cover letter generated:', data);
        displayContent('Cover Letter', data.cover_letter);
    } catch (error) {
        console.error('Error generating cover letter:', error);
        alert('Error generating cover letter: ' + error.message);
    }
}

async function generatePortfolio() {
    try {
        const response = await fetch('/api/ai/generate-portfolio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Portfolio generated:', data);
        displayContent('Portfolio', data.portfolio);
    } catch (error) {
        console.error('Error generating portfolio:', error);
        alert('Error generating portfolio: ' + error.message);
    }
}

async function analyzeResume() {
    try {
        const jobDescription = document.getElementById('jobDescriptionInput').value.trim();
        
        if (!jobDescription) {
            alert('Please enter a job description to analyze');
            return;
        }
        
        // Show loading state
        document.getElementById('analyzeLoader').style.display = 'block';
        document.getElementById('analysisResults').style.display = 'none';
        
        const response = await fetch('/api/ai/analyze-resume', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                job_description: jobDescription
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Resume analysis:', data);
        displayAnalysisResults(data);
    } catch (error) {
        console.error('Error analyzing resume:', error);
        alert('Error analyzing resume: ' + error.message);
    } finally {
        document.getElementById('analyzeLoader').style.display = 'none';
    }
}

function displayAnalysisResults(data) {
    const resultsContainer = document.getElementById('analysisResults');
    const matchScore = data.match_score || 0;
    const missingKeywords = data.missing_keywords || [];
    const overlappingKeywords = data.overlapping_keywords || [];
    const suggestions = data.suggestions || [];
    
    // Update match score
    document.getElementById('matchScoreText').textContent = `${matchScore}%`;
    const scoreBar = document.getElementById('matchScoreBar');
    scoreBar.style.width = `${matchScore}%`;
    
    // Set color based on score
    if (matchScore >= 75) {
        scoreBar.style.backgroundColor = '#4CAF50'; // Green
    } else if (matchScore >= 50) {
        scoreBar.style.backgroundColor = '#2196F3'; // Blue
    } else if (matchScore >= 25) {
        scoreBar.style.backgroundColor = '#FF9800'; // Orange
    } else {
        scoreBar.style.backgroundColor = '#f44336'; // Red
    }
    
    scoreBar.textContent = `${matchScore}%`;
    
    // Update overlapping keywords
    const overlappingContainer = document.getElementById('overlappingKeywords');
    if (overlappingKeywords && overlappingKeywords.length > 0) {
        overlappingContainer.innerHTML = overlappingKeywords
            .map(keyword => `<span style="background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 4px; font-size: 12px;">${keyword}</span>`)
            .join('');
    } else {
        overlappingContainer.innerHTML = '<span style="color: #999; font-size: 14px;">No matching keywords found</span>';
    }
    
    // Update missing keywords
    const missingContainer = document.getElementById('missingKeywords');
    if (missingKeywords && missingKeywords.length > 0) {
        missingContainer.innerHTML = missingKeywords
            .map(keyword => `<span style="background-color: #f44336; color: white; padding: 5px 10px; border-radius: 4px; font-size: 12px;">${keyword}</span>`)
            .join('');
    } else {
        missingContainer.innerHTML = '<span style="color: #999; font-size: 14px;">Your resume covers all identified key skills!</span>';
    }
    
    // Update suggestions
    const suggestionsContainer = document.getElementById('suggestions');
    if (suggestions && suggestions.length > 0) {
        suggestionsContainer.innerHTML = suggestions
            .map(suggestion => `<li style="margin-bottom: 8px;">${suggestion}</li>`)
            .join('');
    } else {
        suggestionsContainer.innerHTML = '<li style="margin-bottom: 8px;">No suggestions at this time</li>';
    }
    
    // Show results
    resultsContainer.style.display = 'block';
    
    // Scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function displayContent(title, content) {
    // Create modal to display content
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 30px;
        border-radius: 8px;
        max-width: 900px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        z-index: 1000;
    `;

    modal.innerHTML = `
        <h2>${title}</h2>
        <pre style="white-space: pre-wrap; word-wrap: break-word; font-family: 'Courier New', monospace; font-size: 12px; background-color: #f5f5f5; padding: 15px; border-radius: 4px; max-height: 60vh; overflow-y: auto;">${escapeHtml(content)}</pre>
        <div style="margin-top: 20px; display: flex; gap: 10px;">
            <button onclick="downloadContent('${title}', this)" style="padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; flex: 1;">📥 Download TXT</button>
            <button onclick="copyToClipboard('${escapeForJS(content)}')" style="padding: 10px 20px; background-color: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; flex: 1;">📋 Copy</button>
            <button onclick="this.closest('div').parentElement.remove(); document.querySelector('[data-backdrop]').remove();" style="padding: 10px 20px; background-color: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer; flex: 1;">✕ Close</button>
        </div>
    `;

    const backdrop = document.createElement('div');
    backdrop.setAttribute('data-backdrop', 'true');
    backdrop.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        z-index: 999;
    `;
    backdrop.onclick = () => {
        modal.remove();
        backdrop.remove();
    };

    document.body.appendChild(backdrop);
    document.body.appendChild(modal);
}

function displayHTMLContent(title, htmlContent) {
    // Create modal to display HTML content with clickable links
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 30px;
        border-radius: 8px;
        max-width: 900px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        z-index: 1000;
    `;

    modal.innerHTML = `
        <h2>${title}</h2>
        <div style="border: 1px solid #ddd; padding: 20px; border-radius: 4px; max-height: 60vh; overflow-y: auto; background: white;">${htmlContent}</div>
        <div style="margin-top: 20px; display: flex; gap: 10px;">
            <button onclick="downloadHTMLContent('${title}', this)" style="padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; flex: 1;">📥 Download HTML</button>
            <button onclick="copyHTMLToClipboard('${escapeForJS(htmlContent)}')" style="padding: 10px 20px; background-color: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; flex: 1;">📋 Copy HTML</button>
            <button onclick="this.closest('div').parentElement.remove(); document.querySelector('[data-backdrop-html]').remove();" style="padding: 10px 20px; background-color: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer; flex: 1;">✕ Close</button>
        </div>
    `;

    const backdrop = document.createElement('div');
    backdrop.setAttribute('data-backdrop-html', 'true');
    backdrop.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        z-index: 999;
    `;
    backdrop.onclick = () => {
        modal.remove();
        backdrop.remove();
    };

    document.body.appendChild(backdrop);
    document.body.appendChild(modal);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function escapeForJS(text) {
    return text.replace(/'/g, "\\'").replace(/\n/g, '\\n');
}

function showTemplateAndFormatSelector() {
    return new Promise((resolve) => {
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 30px;
            border-radius: 8px;
            max-width: 700px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            z-index: 1001;
        `;

        let html = `
            <h2>Select Resume Template & Format</h2>
            <p style="color: #666; margin-bottom: 20px;">Choose your preferred style and download format</p>

            <h3 style="margin-bottom: 15px;">📄 Template Style</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 30px;">
        `;

        // Template selection
        const templates = availableTemplates;
        for (const [key, template] of Object.entries(templates)) {
            html += `
                <div onclick="selectTemplateOption(this, '${key}')" class="template-option" style="
                    padding: 15px;
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    text-align: center;
                    background-color: #f9f9f9;
                " onmouseover="this.style.borderColor='#667eea'; this.style.backgroundColor='#f0f0ff';" onmouseout="this.style.borderColor='#ddd'; this.style.backgroundColor='#f9f9f9';">
                    <div style="font-size: 32px; margin-bottom: 10px;">${template.icon}</div>
                    <div style="font-weight: bold; color: #333; margin-bottom: 5px;">${template.name}</div>
                    <div style="font-size: 12px; color: #666;">${template.description}</div>
                </div>
            `;
        }

        html += `
            </div>

            <h3 style="margin-bottom: 15px;">📁 Download Format</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 20px;">
        `;

        // Format selection
        const formats = availableFormats;
        formats.forEach(format => {
            html += `
                <div onclick="selectFormatOption(this, '${format.format}')" class="format-option" style="
                    padding: 15px;
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    text-align: center;
                    background-color: #f9f9f9;
                " onmouseover="this.style.borderColor='#28a745'; this.style.backgroundColor='#f0fff0';" onmouseout="this.style.borderColor='#ddd'; this.style.backgroundColor='#f9f9f9';">
                    <div style="font-size: 24px; margin-bottom: 10px;">📄</div>
                    <div style="font-weight: bold; color: #333; margin-bottom: 5px;">${format.name}</div>
                    <div style="font-size: 12px; color: #666;">${format.extension}</div>
                </div>
            `;
        });

        html += `
            </div>
            <div style="display: flex; gap: 10px;">
                <button onclick="closeSelector()" style="
                    flex: 1;
                    padding: 10px;
                    background-color: #6c757d;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                ">Cancel</button>
                <button onclick="confirmSelection()" id="confirmBtn" style="
                    flex: 1;
                    padding: 10px;
                    background-color: #007bff;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    opacity: 0.5;
                " disabled>Generate Resume</button>
            </div>
            <input type="hidden" id="selectedTemplate" value="">
            <input type="hidden" id="selectedFormat" value="">
        `;

        modal.innerHTML = html;

        const backdrop = document.createElement('div');
        backdrop.setAttribute('data-selector-backdrop', 'true');
        backdrop.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
        `;

        let selectedTemplate = null;
        let selectedFormat = 'html'; // Default to HTML for clickable links

        // Auto-select defaults after DOM is ready
        setTimeout(() => {
            // Auto-select first template
            const firstTemplate = document.querySelector('.template-option');
            if (firstTemplate) {
                const templateKey = Object.keys(availableTemplates)[0];
                firstTemplate.click();
            }
            
            // Auto-select HTML format
            const htmlFormatOption = Array.from(document.querySelectorAll('.format-option'))
                .find(el => el.textContent.includes('HTML'));
            if (htmlFormatOption) {
                htmlFormatOption.click();
            }
        }, 0);

        window.selectTemplateOption = function(element, templateKey) {
            document.querySelectorAll('.template-option').forEach(el => {
                el.style.borderColor = '#ddd';
                el.style.backgroundColor = '#f9f9f9';
            });
            element.style.borderColor = '#667eea';
            element.style.backgroundColor = '#f0f0ff';
            selectedTemplate = templateKey;
            document.getElementById('selectedTemplate').value = templateKey;
            updateConfirmButton();
        };

        window.selectFormatOption = function(element, formatKey) {
            document.querySelectorAll('.format-option').forEach(el => {
                el.style.borderColor = '#ddd';
                el.style.backgroundColor = '#f9f9f9';
            });
            element.style.borderColor = '#28a745';
            element.style.backgroundColor = '#f0fff0';
            selectedFormat = formatKey;
            document.getElementById('selectedFormat').value = formatKey;
            updateConfirmButton();
        };

        window.updateConfirmButton = function() {
            const btn = document.getElementById('confirmBtn');
            if (selectedTemplate && selectedFormat) {
                btn.disabled = false;
                btn.style.opacity = '1';
            } else {
                btn.disabled = true;
                btn.style.opacity = '0.5';
            }
        };

        window.confirmSelection = function() {
            if (selectedTemplate && selectedFormat) {
                modal.remove();
                backdrop.remove();
                resolve({ template: selectedTemplate, format: selectedFormat });
            }
        };

        window.closeSelector = function() {
            modal.remove();
            backdrop.remove();
            resolve(null);
        };

        backdrop.onclick = () => {
            window.closeSelector();
        };

        document.body.appendChild(backdrop);
        document.body.appendChild(modal);
    });
}

function downloadContent(title, button) {
    const content = button.closest('div').parentElement.querySelector('pre').textContent;
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', `${title.replace(' ', '_')}.txt`);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

function copyToClipboard(content) {
    const modal = event.target.closest('div');
    const textContent = modal.parentElement.querySelector('pre').textContent;
    navigator.clipboard.writeText(textContent).then(() => {
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = '✓ Copied!';
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy to clipboard');
    });
}

function downloadHTMLContent(title, button) {
    const htmlDiv = button.closest('div').parentElement.querySelector('div[style*="border"]');
    const content = htmlDiv.innerHTML;
    const fullHTML = `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .name {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .contact {
            font-size: 12px;
        }
        .contact a {
            color: #0066cc;
            text-decoration: none;
        }
        .contact a:hover {
            text-decoration: underline;
        }
        .section-title {
            margin-top: 25px;
            font-weight: bold;
            border-bottom: 1px solid black;
            padding-bottom: 5px;
        }
        ul {
            margin-top: 5px;
        }
        .project-title {
            font-weight: bold;
            margin-top: 10px;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
${content}
</body>
</html>`;
    
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/html;charset=utf-8,' + encodeURIComponent(fullHTML));
    element.setAttribute('download', `${title.replace(' ', '_')}.html`);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

function copyHTMLToClipboard(content) {
    // Create a temporary element to get the actual HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = content;
    const htmlContent = tempDiv.innerHTML;
    
    navigator.clipboard.writeText(htmlContent).then(() => {
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = '✓ Copied!';
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy HTML to clipboard');
    });
}


