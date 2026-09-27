// Production Render Backend API URL
const PRODUCTION_API = 'https://tech-hub-1-vc99.onrender.com';

// Smart API base resolution: seamlessly handles Localhost, Vercel, and Render
function resolveApiBase() {
    const host = window.location.hostname;
    // 1. Localhost development (Flask port 5000, Live Server port 5500, or local file)
    if (host === 'localhost' || host === '127.0.0.1' || window.location.protocol === 'file:') {
        if (window.location.port === '5000') {
            return window.location.origin;
        }
        return 'http://localhost:5000';
    }
    // 2. Production Vercel deployment (tech-hub-nine.vercel.app or any *.vercel.app)
    if (host.includes('vercel.app')) {
        return PRODUCTION_API;
    }
    // 3. Running directly on Render
    if (host.includes('onrender.com')) {
        return window.location.origin;
    }
    // 4. Default to production Render backend
    return PRODUCTION_API;
}

let API_BASE = resolveApiBase();
const REMOTE_FALLBACK_API = PRODUCTION_API;

let currentToken = localStorage.getItem('token') || null;
let currentUser = JSON.parse(localStorage.getItem('user') || 'null');
let allResults = null;
window.currentAnswersMap = {}; // Safe lookup map to avoid inline string literal errors
window.attachedFile = null; // Attached file or code snippet state

// ================= THEME MANAGEMENT =================
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon();
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon();
}

function updateThemeIcon() {
    const theme = document.documentElement.getAttribute('data-theme') || 'dark';
    const icon = document.getElementById('theme-icon');
    if (icon) {
        icon.innerHTML = theme === 'dark' 
            ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
            : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    }
}

// ================= UI NOTIFICATIONS & LOADERS =================
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3200);
}

function showLoading(text = 'Searching across technical platforms...') {
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.6);backdrop-filter:blur(8px);z-index:9999;display:flex;align-items:center;justify-content:center;';
    const card = document.createElement('div');
    card.style.cssText = 'background:var(--bg-primary);padding:40px 50px;border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,0.4);border:1px solid var(--border);text-align:center;min-width:320px;max-width:90%;';
    card.innerHTML = `
        <div class="spinner"></div>
        <p style="margin-top:20px;color:var(--text-primary);font-size:16px;font-weight:600;">${text}</p>
        <p style="margin-top:8px;color:var(--text-muted);font-size:13px;">Stack Overflow, Gemini AI, GitHub, Reddit, Wikipedia, YouTube, Dev.to, Google Search</p>
    `;
    overlay.appendChild(card);
    document.body.appendChild(overlay);
}

function hideLoading() {
    const loading = document.getElementById('loading-overlay');
    if (loading) loading.remove();
}

function redirect(page) { window.location.href = page; }
function isLoggedIn() { return currentToken !== null; }
function getHeaders() {
    const headers = { 'Content-Type': 'application/json' };
    if (currentToken) headers['Authorization'] = `Bearer ${currentToken}`;
    return headers;
}
function formatDate(d) {
    if (!d) return '';
    const dt = new Date(d);
    return isNaN(dt.getTime()) ? d : dt.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

// XSS Prevention: Safe HTML text encoder
function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

window.codeSnippetsRegistry = window.codeSnippetsRegistry || {};

// Rich Markdown and Code Formatter with Polyglot Code Blocks & Copy Support
function formatAnswerBody(raw) {
    if (!raw) return '';
    // 1. Extract and preserve code blocks
    const codeBlocks = [];
    let text = raw.replace(/```([a-zA-Z0-9_+-]*)\n([\s\S]*?)```/g, function(match, lang, code) {
        const placeholder = `__CODE_BLOCK_${codeBlocks.length}__`;
        const snippetId = `snip_${Math.random().toString(36).substr(2, 8)}_${codeBlocks.length}`;
        window.codeSnippetsRegistry[snippetId] = code.trim();

        const langBadge = escapeHtml(lang || 'code').toUpperCase();
        const htmlBlock = `
            <div class="code-block" id="block-${snippetId}">
                <div class="code-header">
                    <span class="code-lang">${langBadge}</span>
                    <button type="button" class="btn-copy-code" onclick="copyCodeSnippet(this, '${snippetId}')">
                        📋 Copy Code
                    </button>
                </div>
                <pre><code>${escapeHtml(code.trim())}</code></pre>
            </div>
        `;
        codeBlocks.push(htmlBlock);
        return placeholder;
    });

    // 2. Escape HTML on text
    text = escapeHtml(text);

    // 3. Format inline code `code`
    text = text.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');

    // 4. Format bold **text**
    text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

    // 5. Format headers ### Header and ## Header
    text = text.replace(/^### (.*$)/gim, '<h4 style="font-size:16px; font-weight:700; margin:14px 0 6px 0; color:var(--text-primary);">$1</h4>');
    text = text.replace(/^## (.*$)/gim, '<h3 style="font-size:18px; font-weight:700; margin:16px 0 8px 0; color:var(--text-primary);">$1</h3>');

    // 6. Format bullet points
    text = text.replace(/^\s*[-*]\s+(.*$)/gim, '<div style="margin:4px 0 4px 12px; display:flex; align-items:flex-start;"><span style="color:var(--accent);margin-right:8px;font-weight:bold;">•</span><span>$1</span></div>');

    // 7. Format paragraph breaks
    text = text.replace(/\n\n/g, '<div style="height:10px;"></div>');
    text = text.replace(/\n/g, '<br>');

    // 8. Re-inject code blocks
    codeBlocks.forEach((cb, idx) => {
        text = text.replace(`__CODE_BLOCK_${idx}__`, cb);
    });

    return text;
}

function copyCodeSnippet(buttonEl, snippetId) {
    const code = window.codeSnippetsRegistry[snippetId];
    if (!code) return;
    navigator.clipboard.writeText(code).then(() => {
        if (buttonEl) {
            const originalHtml = buttonEl.innerHTML;
            buttonEl.classList.add('copied');
            buttonEl.innerHTML = '✓ Copied!';
            setTimeout(() => {
                buttonEl.classList.remove('copied');
                buttonEl.innerHTML = originalHtml;
            }, 2000);
        }
        showToast('Code copied to clipboard!');
    }).catch(() => {
        showToast('Failed to copy code', 'error');
    });
}

// ================= AUTHENTICATION =================
async function register() {
    const nameEl = document.getElementById('register-name');
    const emailEl = document.getElementById('register-email');
    const passwordEl = document.getElementById('register-password');

    if (!nameEl || !emailEl || !passwordEl) return;
    const name = nameEl.value.trim();
    const email = emailEl.value.trim();
    const password = passwordEl.value;

    if (!name || !email || !password) {
        showToast('Please fill all fields', 'error');
        return;
    }

    try {
        let res;
        try {
            res = await fetch(`${API_BASE}/api/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, password })
            });
        } catch {
            res = await fetch(`${REMOTE_FALLBACK_API}/api/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, password })
            });
        }
        const data = await res.json();
        if (data.success) {
            showToast('Registration successful! Please log in.');
            setTimeout(() => redirect('login.html'), 1000);
        } else {
            showToast(data.error || 'Registration failed', 'error');
        }
    } catch {
        showToast('Connection error to server', 'error');
    }
}

async function login() {
    const emailEl = document.getElementById('login-email');
    const passwordEl = document.getElementById('login-password');

    if (!emailEl || !passwordEl) return;
    const email = emailEl.value.trim();
    const password = passwordEl.value;

    if (!email || !password) {
        showToast('Please enter email and password', 'error');
        return;
    }

    try {
        let res;
        try {
            res = await fetch(`${API_BASE}/api/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
        } catch {
            res = await fetch(`${REMOTE_FALLBACK_API}/api/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
        }
        const data = await res.json();
        if (data.success) {
            currentToken = data.token;
            currentUser = data.user;
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            showToast(`Welcome back, ${data.user.name}!`);
            setTimeout(() => redirect('dashboard.html'), 800);
        } else {
            showToast(data.error || 'Login failed', 'error');
        }
    } catch {
        showToast('Connection error to server', 'error');
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    currentToken = null;
    currentUser = null;
    showToast('Logged out');
    setTimeout(() => redirect('index.html'), 500);
}

// ================= FILE ATTACHMENT HANDLING =================
function triggerFileUpload() {
    const input = document.getElementById('file-upload-input');
    if (input) input.click();
}

function handleFileUpload(event) {
    const file = event.target.files && event.target.files[0];
    if (!file) return;

    if (file.size > 500 * 1024) {
        showToast('File too large (maximum limit is 500 KB)', 'error');
        event.target.value = '';
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        const content = e.target.result;
        window.attachedFile = {
            name: file.name,
            size: file.size,
            content: content
        };

        const bar = document.getElementById('attached-file-bar');
        const nameEl = document.getElementById('attached-file-name');
        const sizeEl = document.getElementById('attached-file-size');

        if (nameEl) nameEl.textContent = file.name;
        if (sizeEl) {
            const kb = (file.size / 1024).toFixed(1);
            sizeEl.textContent = `(${kb} KB)`;
        }
        if (bar) bar.style.display = 'inline-flex';

        // Pre-fill query if empty
        const searchInput = document.getElementById('search-input');
        if (searchInput && !searchInput.value.trim()) {
            searchInput.value = `Explain and analyze ${file.name}`;
        }
        showToast(`Attached ${file.name}`);
    };
    reader.onerror = function() {
        showToast('Failed to read file contents', 'error');
    };
    reader.readAsText(file);
}

function removeAttachedFile() {
    window.attachedFile = null;
    const input = document.getElementById('file-upload-input');
    if (input) input.value = '';
    const bar = document.getElementById('attached-file-bar');
    if (bar) bar.style.display = 'none';
    showToast('File removed');
}

// ================= SEARCH EXECUTION =================
async function performSearch() {
    const input = document.getElementById('search-input');
    let query = input ? input.value.trim() : '';

    // If query is empty but user uploaded a file, create default query
    if (!query && window.attachedFile) {
        query = `Explain and analyze ${window.attachedFile.name}`;
        if (input) input.value = query;
    }

    if (!query && !window.attachedFile) {
        showToast('Please enter a technical question or attach a file', 'error');
        return;
    }

    const payload = {
        query: query,
        file_name: window.attachedFile ? window.attachedFile.name : null,
        file_content: window.attachedFile ? window.attachedFile.content : null
    };

    const loadingMsg = window.attachedFile 
        ? `Analyzing ${window.attachedFile.name} across 11 technical engines...`
        : 'Searching across technical platforms & ChatGPT...';

    showLoading(loadingMsg);
    try {
        let res;
        try {
            res = await fetch(`${API_BASE}/api/search`, {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify(payload)
            });
        } catch (localErr) {
            console.log('Local backend not reachable, connecting to live engine fallback...');
            res = await fetch(`${REMOTE_FALLBACK_API}/api/search`, {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify(payload)
            });
        }

        const data = await res.json();
        hideLoading();
        if (data.success && data.answers && data.answers.length > 0) {
            localStorage.setItem('searchResults', JSON.stringify(data));
            redirect('results.html');
        } else {
            showToast(data.error || 'No answers found for this question', 'error');
        }
    } catch (err) {
        hideLoading();
        showToast('Failed to reach search service. Check network connection.', 'error');
    }
}

function quickSearch(q) {
    const input = document.getElementById('search-input');
    if (input) input.value = q;
    performSearch();
}

// ================= RESULTS PAGE DISPLAY =================
function displayResults() {
    const rawData = localStorage.getItem('searchResults');
    if (!rawData) {
        redirect('dashboard.html');
        return;
    }

    const data = JSON.parse(rawData);
    allResults = data;

    const qDisplay = document.getElementById('query-display');
    const tDisplay = document.getElementById('topic-display');
    const sDisplay = document.getElementById('sources-displayed');

    const topicMap = {
        'science': 'Science & Nature',
        'health_wellness': 'Health & Wellness',
        'finance_business': 'Finance & Business',
        'history_geography': 'History & World Events',
        'general_knowledge': 'General Knowledge',
        'html_css': 'Web Development & CSS',
        'python': 'Python Development',
        'javascript': 'JavaScript & Web',
        'database': 'Databases & SQL',
        'git': 'Version Control (Git)',
        'devops': 'DevOps & Infrastructure',
        'java': 'Java Programming',
        'cpp': 'C++ Programming',
        'technology_coding': 'Technology & Algorithms'
    };
    const friendlyTopic = topicMap[data.topic] || (data.topic ? data.topic.replace('_', ' ').toUpperCase() : 'General Knowledge');

    if (qDisplay) {
        if (data.file_name) {
            qDisplay.innerHTML = `${escapeHtml(data.query)} <span style="font-size:14px; font-weight:600; background:var(--bg-secondary); padding:4px 10px; border-radius:12px; border:1px solid var(--border); margin-left:8px; vertical-align:middle;">📄 ${escapeHtml(data.file_name)}</span>`;
        } else {
            qDisplay.textContent = data.query;
        }
    }
    if (tDisplay) tDisplay.textContent = `Category: ${friendlyTopic}`;
    if (sDisplay) sDisplay.textContent = (data.sources_searched || []).join(', ');

    renderFilterChips(data.answers || []);
    renderAnalysis(data.comparison, data);
    renderResults(data.answers);
    loadRelatedQuestions(data.query);
}

function renderFilterChips(answers) {
    const chipContainer = document.getElementById('filter-chips-container');
    if (!chipContainer) return;

    // Get unique sources in answers
    const sources = Array.from(new Set(answers.map(a => a.source))).filter(Boolean);

    chipContainer.innerHTML = `
        <span class="chip active-chip" onclick="filterResults('all')">All Sources (${answers.length})</span>
        <span class="chip" onclick="filterResults('best')" style="border-color:#F59E0B;color:#F59E0B;font-weight:600;">🏆 Top Real-World Pick</span>
        ${sources.map(s => `<span class="chip" onclick="filterResults('${escapeHtml(s)}')">${escapeHtml(s)}</span>`).join('')}
    `;
}

function renderAnalysis(comparison, data) {
    const searchPanel = document.getElementById('search-analysis-content');
    if (searchPanel && data) {
        searchPanel.innerHTML = `
            <p style="font-size:14px;margin-bottom:12px;">
                <strong>Sources Queried in Parallel:</strong><br>
                <span style="color:var(--accent);font-weight:700;font-size:32px;">${(data.sources_searched || []).length}</span>
            </p>
            <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px;">
                ${(data.sources_searched || []).map(s => `<span class="card-source">${escapeHtml(s)}</span>`).join('')}
            </div>
            <div style="margin-top:14px;padding-top:12px;border-top:1px solid var(--border);">
                <p style="font-size:13px;color:var(--text-secondary);margin-bottom:4px;">Domain Category: <strong>${escapeHtml(data.topic ? data.topic.replace('_', ' ').toUpperCase() : 'GENERAL')}</strong></p>
                ${data.file_name ? `<p style="font-size:13px;color:var(--accent);margin-bottom:4px;">Analyzed File: <strong>📄 ${escapeHtml(data.file_name)}</strong></p>` : ''}
                <p style="font-size:13px;color:var(--text-secondary);">Query ID: <code>${escapeHtml(data.query_id)}</code></p>
            </div>
        `;
    }

    const consensusPanel = document.getElementById('consensus-content');
    if (consensusPanel && comparison) {
        const confPercent = Math.round((comparison.avg_confidence || 0.7) * 100);
        const cls = confPercent >= 75 ? 'confidence-high' : confPercent >= 50 ? 'confidence-medium' : 'confidence-low';

        consensusPanel.innerHTML = `
            <div class="confidence-bar" style="margin-bottom:8px;">
                <div class="confidence-fill ${cls}" style="width:${confPercent}%;"></div>
            </div>
            <p style="font-size:13px;color:var(--text-muted);margin-bottom:14px;">
                Average System Confidence: <strong>${confPercent}%</strong>
            </p>
            ${(comparison.consensus && comparison.consensus.length > 0) ? `
                <div style="margin-bottom:10px;padding:10px 12px;background:var(--success-bg);border-radius:6px;">
                    <p style="font-size:12px;color:var(--success);font-weight:700;letter-spacing:0.04em;">CONSENSUS AGREEMENT (${comparison.consensus.length})</p>
                    <p style="font-size:13px;margin-top:4px;">${comparison.consensus.map(s => escapeHtml(s)).join(', ')}</p>
                </div>
            ` : ''}
            ${(comparison.minority && comparison.minority.length > 0) ? `
                <div style="margin-bottom:10px;padding:10px 12px;background:var(--warning-bg);border-radius:6px;">
                    <p style="font-size:12px;color:var(--warning);font-weight:700;letter-spacing:0.04em;">DIVERGENT / SECONDARY SOURCES (${comparison.minority.length})</p>
                    <p style="font-size:13px;margin-top:4px;">${comparison.minority.map(s => escapeHtml(s)).join(', ')}</p>
                </div>
            ` : ''}
            <div style="margin-top:12px;padding:10px 12px;background:var(--bg-secondary);border-radius:6px;border-left:3px solid var(--accent);">
                <p style="font-size:13px;line-height:1.5;">${escapeHtml(comparison.consensus_recommendation || comparison.recommendation)}</p>
            </div>
        `;
    }
}

function renderResults(answers) {
    const container = document.getElementById('results-container');
    const bestContainer = document.getElementById('featured-best-container');
    if (!container) return;
    if (!answers || answers.length === 0) {
        container.innerHTML = '<p style="color:var(--text-secondary);text-align:center;padding:50px;">No results found across sources.</p>';
        if (bestContainer) bestContainer.innerHTML = '';
        return;
    }

    // Reset lookup map
    window.currentAnswersMap = {};

    // 1. Render Featured Best Real-World Solution Card
    if (bestContainer) {
        const best = answers.find(a => a.is_best_answer) || answers[0];
        if (best) {
            const bestId = 'best-ans-featured';
            window.currentAnswersMap[bestId] = best;
            const conf = Math.round((best.confidence || 0.95) * 100);
            bestContainer.innerHTML = `
                <div class="best-answer-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:12px;">
                        <span class="best-answer-badge">🏆 #1 Most Relevant Real-World Solution</span>
                        <span class="card-source" style="font-weight:700;font-size:13px;">${escapeHtml(best.source)}</span>
                    </div>
                    <h3 style="font-size:20px;font-weight:700;margin-bottom:8px;">${escapeHtml(best.title || 'Recommended Production Approach')}</h3>
                    <div class="best-reason-box">
                        <strong>Why this source is selected for real-world use:</strong> ${escapeHtml(best.best_reason || 'Verified as the most practical, clear, and comprehensive answer.')}
                    </div>
                    <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                        <span style="font-size:12px;color:var(--text-muted);">Trust Score: <strong>${best.trust_score || 9}/10</strong></span>
                        <span style="font-size:12px;color:var(--text-muted);">Confidence: <strong>${conf}%</strong></span>
                    </div>
                    <div class="confidence-bar" style="margin-bottom:14px;"><div class="confidence-fill confidence-high" style="width:${conf}%;"></div></div>
                    <div class="card-body" style="font-family:inherit; line-height:1.65; background:var(--bg-secondary); padding:18px; border-radius:8px; border:1px solid var(--border); margin-bottom:16px;">
                        ${formatAnswerBody(best.body)}
                    </div>
                    <div class="card-actions">
                        ${best.url ? `<button onclick="window.open('${escapeHtml(best.url)}','_blank')">View Source</button>` : ''}
                        ${best.url ? `<button onclick="copyLink('${escapeHtml(best.url)}')">Copy Link</button>` : ''}
                        <button onclick="copyAnswerById('${bestId}')">📋 Copy Solution</button>
                        <button onclick="saveAnswerById('${bestId}')">⭐ Bookmark</button>
                    </div>
                </div>
            `;
        } else {
            bestContainer.innerHTML = '';
        }
    }

    // 2. Render All Results Grid
    container.innerHTML = `<div class="grid-2">` + answers.map((a, i) => {
        const answerId = `ans-${i}`;
        window.currentAnswersMap[answerId] = a;

        const conf = Math.round((a.confidence || 0.5) * 100);
        const cls = conf >= 75 ? 'confidence-high' : conf >= 50 ? 'confidence-medium' : 'confidence-low';
        const isAI = a.source === 'Gemini AI' || a.source === 'ChatGPT';
        const isBest = a.is_best_answer;
        const fullBody = a.body || '';
        const shortBody = fullBody.length > 250 ? fullBody.substring(0, 250) + '...' : fullBody;
        const isLong = fullBody.length > 250;

        return `
        <div class="card" style="${isBest ? 'border-color:#F59E0B;box-shadow:0 6px 20px rgba(245,158,11,0.15);' : isAI ? 'grid-column: 1 / -1; border-color: var(--accent);' : ''}">
            <div class="card-header">
                <div>
                    <span class="card-title">${escapeHtml(a.title || 'Source Answer ' + (i+1))}</span>
                    ${isBest ? `<span class="best-answer-badge" style="font-size:10px;padding:3px 8px;margin-left:8px;">★ Top Pick</span>` : ''}
                </div>
                <span class="card-source">${escapeHtml(a.source)}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span style="font-size:12px;color:var(--text-muted);">Trust Score: <strong>${a.trust_score || 7}/10</strong></span>
                ${a.date ? `<span style="font-size:12px;color:var(--text-muted);">${formatDate(a.date)}</span>` : ''}
            </div>
            <div class="confidence-bar"><div class="confidence-fill ${cls}" style="width:${conf}%;"></div></div>
            <div style="font-size:12px;color:var(--text-muted);margin-bottom:12px;">Confidence: ${conf}%</div>
            
            <div class="card-body" id="${answerId}-body" style="font-family: inherit; line-height: 1.6;">
                <div id="${answerId}-short">${formatAnswerBody(shortBody)}</div>
                <div id="${answerId}-full" style="display:none;">${formatAnswerBody(fullBody)}</div>
            </div>

            ${isLong ? `
                <button onclick="toggleAnswer('${answerId}')" style="font-size:12px;padding:6px 14px;background:transparent;border:1px solid var(--border);color:var(--accent);border-radius:4px;cursor:pointer;margin:10px 0;">
                    <span id="${answerId}-btn">Read More</span>
                </button>
            ` : ''}

            <div class="card-actions">
                ${a.url ? `<button onclick="window.open('${escapeHtml(a.url)}','_blank')">View Source</button>` : ''}
                ${a.url ? `<button onclick="copyLink('${escapeHtml(a.url)}')">Copy Link</button>` : ''}
                <button onclick="copyAnswerById('${answerId}')">Copy Content</button>
                <button onclick="saveAnswerById('${answerId}')">Save</button>
            </div>
        </div>`;
    }).join('') + `</div>`;
}

function toggleAnswer(id) {
    const shortEl = document.getElementById(`${id}-short`);
    const fullEl = document.getElementById(`${id}-full`);
    const btn = document.getElementById(`${id}-btn`);
    if (shortEl && fullEl && btn) {
        if (fullEl.style.display === 'none') {
            shortEl.style.display = 'none';
            fullEl.style.display = 'inline';
            btn.textContent = 'Show Less';
        } else {
            shortEl.style.display = 'inline';
            fullEl.style.display = 'none';
            btn.textContent = 'Read More';
        }
    }
}

function filterResults(source) {
    if (!allResults || !allResults.answers) return;
    if (source === 'all') {
        renderResults(allResults.answers);
        return;
    }
    if (source === 'best') {
        const best = allResults.answers.filter(a => a.is_best_answer);
        if (best.length > 0) renderResults(best);
        else renderResults(allResults.answers.slice(0, 1));
        return;
    }
    const filtered = allResults.answers.filter(a => a.source === source);
    if (filtered.length > 0) {
        renderResults(filtered);
    } else {
        const c = document.getElementById('results-container');
        if (c) c.innerHTML = `<p style="color:var(--text-secondary);text-align:center;padding:40px;">No results found from ${escapeHtml(source)}.</p>`;
    }
}

// Multiline-safe Copy & Save functions using in-memory registry
function copyLink(url) {
    if (!url) return;
    navigator.clipboard.writeText(url).then(() => showToast('Link copied to clipboard!'));
}

function copyAnswerById(answerId) {
    const a = window.currentAnswersMap[answerId];
    if (!a || !a.body) return;
    navigator.clipboard.writeText(a.body).then(() => showToast('Answer content copied!'));
}

function copyAllResults() {
    if (!allResults || !allResults.answers) return;
    let text = `TechHub Consensus Report\nQuery: ${allResults.query}\nTopic: ${allResults.topic}\nConfidence: ${Math.round((allResults.comparison?.avg_confidence || 0.7) * 100)}%\n\n`;
    allResults.answers.forEach((a, i) => {
        text += `[${i + 1}] [${a.source}] ${a.title}\n${a.body}\n${a.url ? 'Source: ' + a.url + '\n' : ''}Confidence: ${Math.round(a.confidence * 100)}%\n\n`;
    });
    navigator.clipboard.writeText(text).then(() => showToast('Full report copied to clipboard!'));
}

async function saveAnswerById(answerId) {
    if (!isLoggedIn()) {
        showToast('Please sign in to save answers', 'error');
        return;
    }
    const a = window.currentAnswersMap[answerId];
    if (!a) return;

    try {
        let res;
        try {
            res = await fetch(`${API_BASE}/api/history/save`, {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify({
                    query_id: allResults?.query_id || 'manual',
                    source: a.source,
                    answer: a.body,
                    url: a.url || '',
                    confidence: a.confidence || 0.5
                })
            });
        } catch {
            res = await fetch(`${REMOTE_FALLBACK_API}/api/history/save`, {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify({
                    query_id: allResults?.query_id || 'manual',
                    source: a.source,
                    answer: a.body,
                    url: a.url || '',
                    confidence: a.confidence || 0.5
                })
            });
        }
        const d = await res.json();
        if (d.success) showToast('Answer saved to your account!');
        else showToast(d.error || 'Failed to save', 'error');
    } catch {
        showToast('Server communication error', 'error');
    }
}

async function loadRelatedQuestions(query) {
    const container = document.getElementById('related-container');
    if (!container) return;
    try {
        let res;
        try {
            res = await fetch(`${API_BASE}/api/related`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
        } catch {
            res = await fetch(`${REMOTE_FALLBACK_API}/api/related`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
        }
        const data = await res.json();
        if (data.success && data.questions && data.questions.length > 0) {
            container.innerHTML = `
                <h3 style="margin-bottom:16px;font-size:18px;font-weight:600;">Related Technical Questions</h3>
                <div class="suggestions" style="justify-content:flex-start;">
                    ${data.questions.map(q => `<span class="chip" onclick="quickSearch('${escapeHtml(q).replace(/'/g, "\\'")}')">${escapeHtml(q)}</span>`).join('')}
                </div>
            `;
        }
    } catch {}
}

// ================= USER PAGES: HISTORY, SAVED, PROFILE =================
async function loadHistory() {
    if (!isLoggedIn()) { redirect('login.html'); return; }
    const container = document.getElementById('history-container');
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE}/api/history`, { headers: getHeaders() });
        const data = await res.json();
        if (data.success && data.history.length > 0) {
            container.innerHTML = data.history.map(h => `
                <div class="history-item" style="display:flex;justify-content:space-between;align-items:center;padding:16px;background:var(--bg-secondary);border:1px solid var(--border);border-radius:8px;margin-bottom:12px;">
                    <div>
                        <div class="history-query" style="font-weight:600;font-size:16px;cursor:pointer;color:var(--accent);" onclick="quickSearch('${escapeHtml(h.query).replace(/'/g, "\\'")}')">${escapeHtml(h.query)}</div>
                        <div class="history-meta" style="font-size:13px;color:var(--text-muted);margin-top:4px;">Domain: ${escapeHtml(h.topic || 'General')} | ${h.sources_count || 8} sources | ${formatDate(h.created_at)}</div>
                    </div>
                    <button class="btn-outline" style="padding:6px 14px;font-size:12px;" onclick="quickSearch('${escapeHtml(h.query).replace(/'/g, "\\'")}')">Search Again</button>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<p style="color:var(--text-secondary);text-align:center;padding:40px;">No search history recorded yet.</p>';
        }
    } catch {
        container.innerHTML = '<p style="color:var(--danger);text-align:center;padding:40px;">Error loading history.</p>';
    }
}

async function loadSaved() {
    if (!isLoggedIn()) { redirect('login.html'); return; }
    const container = document.getElementById('saved-container');
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE}/api/saved`, { headers: getHeaders() });
        const data = await res.json();
        if (data.success && data.saved.length > 0) {
            container.innerHTML = `<div class="grid-2">` + data.saved.map(s => `
                <div class="card">
                    <div class="card-header">
                        <span class="card-title">${escapeHtml(s.source)}</span>
                        <span class="card-source">${formatDate(s.saved_at)}</span>
                    </div>
                    <div class="card-body" style="white-space:pre-wrap;margin:12px 0;">${escapeHtml((s.answer || '').substring(0, 240))}${s.answer?.length > 240 ? '...' : ''}</div>
                    ${s.url ? `<a href="${escapeHtml(s.url)}" target="_blank" style="font-size:13px;color:var(--accent);display:inline-block;margin-top:6px;">View Original Source ↗</a>` : ''}
                </div>
            `).join('') + `</div>`;
        } else {
            container.innerHTML = '<p style="color:var(--text-secondary);text-align:center;padding:40px;">No saved solutions yet.</p>';
        }
    } catch {
        container.innerHTML = '<p style="color:var(--danger);text-align:center;padding:40px;">Error loading saved items.</p>';
    }
}

async function loadProfile() {
    if (!isLoggedIn()) { redirect('login.html'); return; }
    const container = document.getElementById('profile-container');
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE}/api/profile`, { headers: getHeaders() });
        const data = await res.json();
        if (data.success) {
            const u = data.user;
            container.innerHTML = `
                <div class="card" style="max-width:500px;margin:20px auto;padding:32px;">
                    <div class="card-header">
                        <span class="card-title" style="font-size:22px;">${escapeHtml(u.name)}</span>
                        <span class="card-source">${escapeHtml(u.role || 'Developer')}</span>
                    </div>
                    <div class="card-body" style="margin-top:16px;">
                        <p style="margin-bottom:8px;"><strong>Email:</strong> ${escapeHtml(u.email)}</p>
                        <p style="margin-bottom:8px;"><strong>Account ID:</strong> #${u.id}</p>
                        <p style="margin-bottom:8px;"><strong>Member Since:</strong> ${formatDate(u.created_at)}</p>
                    </div>
                    <div style="margin-top:24px;text-align:center;">
                        <button class="btn-outline" onclick="logout()" style="color:var(--danger);border-color:var(--danger);">Sign Out</button>
                    </div>
                </div>
            `;
        }
    } catch {}
}

// ================= DOM INITIALIZATION =================
document.addEventListener('DOMContentLoaded', function() {
    initTheme();

    const page = window.location.pathname.split('/').pop() || 'index.html';
    if (page === 'results.html') displayResults();
    else if (page === 'history.html') loadHistory();
    else if (page === 'saved.html') loadSaved();
    else if (page === 'profile.html') loadProfile();

    const input = document.getElementById('search-input');
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') performSearch();
        });
    }
});
