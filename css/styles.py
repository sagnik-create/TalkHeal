import streamlit as st

def apply_custom_css():
    """Applies custom CSS to the Streamlit application for enhanced styling."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Root variables for consistent theming */
        :root {
            --primary-color: #6366f1;
            --primary-light: #818cf8;
            --primary-dark: #4f46e5;
            --secondary-color: #ec4899;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --background: #f8fafc;
            --surface: #ffffff;
            --surface-alt: #f1f5f9;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --text-muted: #94a3b8;
            --border: #e2e8f0;
            --border-light: #f1f5f9;
            --shadow: rgba(15, 23, 42, 0.08);
            --shadow-lg: rgba(15, 23, 42, 0.15);
            --radius: 12px;
            --radius-lg: 16px;
        }

        /* Global styles */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            min-height: 100vh;
        }

        .main .block-container {
            padding-top: 0rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        /* Chat container with improved styling */
        .chat-container {
            background: var(--surface);
            border-radius: var(--radius-lg);
            padding: 24px;
            margin: 16px 0;
            box-shadow: 0 4px 24px var(--shadow-lg);
            min-height: 500px;
            max-height: 600px;
            overflow-y: auto;
            border: 1px solid var(--border-light);
            scroll-behavior: smooth;
            position: relative;
        }

        .chat-container::-webkit-scrollbar {
            width: 6px;
        }

        .chat-container::-webkit-scrollbar-track {
            background: var(--surface-alt);
            border-radius: 3px;
        }

        .chat-container::-webkit-scrollbar-thumb {
            background: var(--text-muted);
            border-radius: 3px;
        }

        .chat-container::-webkit-scrollbar-thumb:hover {
            background: var(--text-secondary);
            border-radius: 3px;
        }

        /* User message with better contrast */
        .user-message {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 16px 20px;
            border-radius: 20px 20px 8px 20px;
            margin: 12px 0 12px auto;
            max-width: 75%;
            word-wrap: break-word;
            box-shadow: 0 3px 12px rgba(99, 102, 241, 0.25);
            font-weight: 500;
            line-height: 1.5;
            position: relative;
        }

        /* Bot message with improved readability */
        .bot-message {
            background: var(--surface-alt);
            color: var(--text-primary);
            padding: 16px 20px;
            border-radius: 20px 20px 20px 8px;
            margin: 12px auto 12px 0;
            max-width: 75%;
            word-wrap: break-word;
            border: 1px solid var(--border);
            box-shadow: 0 2px 8px var(--shadow);
            line-height: 1.6;
            font-weight: 400;
        }

        /* Welcome message */
        .welcome-message {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 24px;
            border-radius: var(--radius-lg);
            margin: 24px auto;
            text-align: center;
            box-shadow: 0 8px 32px rgba(99, 102, 241, 0.3);
            font-weight: 500;
            line-height: 1.6;
        }

        /* Message time styling */
        .message-time {
            font-size: 0.75em;
            opacity: 0.8;
            margin-top: 8px;
            text-align: right;
            font-weight: 400;
        }

        /* Enhanced header */
        .main-header {
            text-align: center;
            padding: 32px 24px;
            background: var(--surface);
            color: var(--text-primary);
            border-radius: var(--radius-lg);
            margin-bottom: 24px;
            box-shadow: 0 8px 32px var(--shadow-lg);
            border: 1px solid var(--border-light);
            position: relative;
            overflow: hidden;
        }

        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        }

        .main-header h1 {
            margin: 0 0 8px 0;
            font-size: 2.5em;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .main-header p {
            margin: 0;
            font-size: 1.2em;
            color: var(--text-secondary);
            font-weight: 500;
        }

        /* Emergency button with better accessibility */
        .emergency-button {
            background: linear-gradient(135deg, var(--danger-color) 0%, #dc2626 100%);
            color: white;
            padding: 18px 24px;
            border-radius: var(--radius);
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3);
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 600;
            font-size: 1.1em;
            border: none;
        }

        .emergency-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(239, 68, 68, 0.4);
            background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        }

        /* Sidebar content styling */
        .sidebar-content {
            background: var(--surface);
            border-radius: var(--radius-lg);
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 16px var(--shadow);
            border: 1px solid var(--border-light);
        }

        /* Button improvements */
        .stButton > button {
            background: var(--surface);
            color: var(--text-primary);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 12px 16px;
            font-weight: 500;
            transition: all 0.2s ease;
            width: 100%;
            font-family: 'Inter', sans-serif;
        }

        .stButton > button:hover {
            background: var(--surface-alt);
            border-color: var(--primary-color);
            color: var(--primary-color);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px var(--shadow);
        }

        /* Target the specific sidebar toggle button by its key or a specific ancestor */
        /* This targets the button generated by st.button("☰", key="persistent_sidebar_toggle") */
        .stButton button[key="persistent_sidebar_toggle"] { /* Use data-testid or a more specific selector if "key" doesn't work directly on the button */
            background: var(--primary-color); /* Make it distinct */
            color: white;
            border: none;
            border-radius: 50%; /* Make it round */
            width: 40px; /* Smaller, round button */
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
            transition: all 0.3s ease;
            margin: 0; /* Remove default margin */
            padding: 0; /* Remove default padding */
            line-height: 1; /* Adjust line height for better centering of the icon */
        }

        .stButton button[key="persistent_sidebar_toggle"]:hover {
            background: var(--primary-dark);
            transform: scale(1.1);
            box-shadow: 0 6px 24px rgba(99, 102, 241, 0.4);
        }


        /* Form input styling */
        .stTextInput > div > div > input {
            background: var(--surface);
            border: 2px solid var(--border);
            border-radius: var(--radius);
            padding: 12px 16px;
            font-size: 1em;
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            transition: all 0.2s ease;
        }

        .stTextInput > div > div > input:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
            outline: none;
        }

        /* Select slider improvements */
        .stSelectSlider > div > div {
            background: var(--surface-alt);
            border-radius: var(--radius);
            padding: 8px;
        }

        /* Expander styling */
        .streamlit-expander {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            margin-bottom: 12px;
            box-shadow: 0 2px 8px var(--shadow);
        }

        .streamlit-expander > summary {
            background: var(--surface-alt);
            color: var(--text-primary);
            font-weight: 600;
            padding: 16px;
            border-radius: var(--radius);
        }

        /* Info and success message styling */
        .stInfo, .stSuccess, .stWarning {
            border-radius: var(--radius);
            border: none;
            font-weight: 500;
        }

        .stInfo {
            background: rgba(99, 102, 241, 0.1);
            color: var(--text-primary);
        }

        .stSuccess {
            background: rgba(16, 185, 129, 0.1);
            color: #047857;
        }

        .stWarning {
            background: rgba(245, 158, 11, 0.1);
            color: #92400e;
        }

        /* Typography improvements */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary);
            font-weight: 600;
            line-height: 1.3;
        }

        p {
            color: var(--text-primary);
            line-height: 1.6;
        }

        /* Loading spinner */
        .stSpinner > div {
            border-color: var(--primary-color) !important;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem;
            }

            .user-message, .bot-message {
                max-width: 90%;
                padding: 12px 16px;
            }

            .main-header h1 {
                font-size: 2em;
            }

            .chat-container {
                min-height: 400px;
                max-height: 500px;
                padding: 16px;
            }
        }

        /* Hide default Streamlit elements */
        .stApp > header {
            display: none !important;
        }

        div[data-testid="stToolbar"] {
            display: none !important;
        }

        /* Ensure sidebar styling applies to the actual Streamlit sidebar */
        .stApp [data-testid="stSidebar"] {
            background: var(--surface);
            border-right: 1px solid var(--border-light);
            box-shadow: 4px 0 24px var(--shadow-lg);
            /* Remove transform and visibility here */
        }
    </style>
    """, unsafe_allow_html=True)