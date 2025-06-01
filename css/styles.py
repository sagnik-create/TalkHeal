import streamlit as st
import base64

def get_base64_of_bin_file(bin_file):
    """Encodes a binary file (like an image) to base64."""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def apply_custom_css():
    """Applies custom CSS to the Streamlit application for enhanced styling."""
    # Path to your background image
    background_image_path = "Background.jpg"
    
    # Encode the image to base64
    base64_image = get_base64_of_bin_file(background_image_path)
    
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Root variables for consistent theming */
        :root {{
            --primary-color: #6366f1;
            --primary-light: #818cf8;
            --primary-dark: #4f46e5;
            --secondary-color: #ec4899;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --surface: rgba(255, 255, 255, 0.15);
            --surface-alt: rgba(255, 255, 255, 0.25);
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --text-muted: #94a3b8;
            --border: rgba(255, 255, 255, 0.3);
            --border-light: rgba(255, 255, 255, 0.2);
            --shadow: rgba(0, 0, 0, 0.15);
            --shadow-lg: rgba(0, 0, 0, 0.25);
            --radius: 12px;
            --radius-lg: 16px;
            --light-transparent-bg: rgba(255, 255, 255, 0.4);
            --light-transparent-bg-hover: rgba(255, 255, 255, 0.6);
            --light-transparent-border: rgba(255, 255, 255, 0.5);
            --active-conversation-bg: linear-gradient(135deg, rgba(99, 102, 241, 0.9) 0%, rgba(129, 140, 248, 0.9) 100%);
            --active-conversation-border: rgba(99, 102, 241, 0.8);
            --active-conversation-shadow: rgba(99, 102, 241, 0.4);
        }}
        
        /* Global styles - Set the background image */
        .stApp {{
            background-image: url("data:image/jpeg;base64,{base64_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center center;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            min-height: 100vh;
        }}
        
        /* Apply an overlay to slightly fade the background image */
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.3);
            z-index: -1;
        }}
        
        .main .block-container {{
            padding-top: 0rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }}
        
        /* Main chat area styling - no container wrapper */
        .main .block-container {{
            scroll-behavior: smooth;
        }}
        
        /* User message styling */
        .user-message {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.8) 0%, rgba(129, 140, 248, 0.8) 100%);
            color: white;
            padding: 16px 20px;
            border-radius: 20px 20px 8px 20px;
            margin: 12px 0 12px auto;
            max-width: 75%;
            word-wrap: break-word;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.25);
            font-weight: 500;
            line-height: 1.5;
            position: relative;
            backdrop-filter: blur(5px);
            display: block;
            margin-left: auto;
            margin-right: 0;
        }}
        
        /* Bot message styling */
        .bot-message {{
            background: var(--surface-alt);
            color: var(--text-primary);
            padding: 16px 20px;
            border-radius: 20px 20px 20px 8px;
            margin: 12px 0;
            max-width: 75%;
            word-wrap: break-word;
            border: 1px solid var(--border);
            box-shadow: 0 2px 8px var(--shadow);
            line-height: 1.6;
            font-weight: 500;
            backdrop-filter: blur(10px);
            display: block;
            margin-left: 0;
            margin-right: auto;
        }}
        
        /* Welcome message */
        .welcome-message {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.8) 0%, rgba(236, 72, 153, 0.8) 100%);
            color: white;
            padding: 24px;
            border-radius: var(--radius-lg);
            margin: 24px auto;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            font-weight: 500;
            line-height: 1.6;
            backdrop-filter: blur(10px);
            display: block;
        }}
        
        /* Message time styling */
        .message-time {{
            font-size: 0.75em;
            opacity: 0.8;
            margin-top: 8px;
            text-align: right;
            font-weight: 400;
        }}
        
        .user-message .message-time {{
            color: rgba(255, 255, 255, 0.8);
        }}
        
        .bot-message .message-time {{
            color: var(--text-secondary);
        }}
        
        /* Banner */
        .banner {{
            text-align: center;
            background: var(--surface);
            color: white;
            border-radius: var(--radius-lg);
            margin-bottom: 16px;
            box-shadow: 0 8px 32px var(--shadow-lg);
            border: 1px solid var(--border-light);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }}
        
        .banner::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        }}
        
        .banner h3 {{
            margin: 0 0 0 0;
            font-size: 2em;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .banner p {{
            margin: 0;
            font-size: 0.85em;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 500;
        }}
        
        /* Enhanced header */
        .main-header {{
            text-align: center;
            padding: 32px 24px;
            background: var(--surface);
            color: white;
            border-radius: var(--radius-lg);
            margin-bottom: 24px;
            box-shadow: 0 8px 32px var(--shadow-lg);
            border: 1px solid var(--border-light);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }}
        
        .main-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        }}
        
        .main-header h1 {{
            margin: 0 0 8px 0;
            font-size: 2.5em;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .main-header p {{
            margin: 0;
            font-size: 1.2em;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 500;
        }}
        
        /* Emergency button */
        /* Emergency button - Targeted by data-testid from its key */
        .emergency_button {{ /* <-- CHANGE THIS LINE */
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.9) 0%, rgba(220, 38, 38, 0.9) 100%) !important;
            color: white !important;
            padding: 18px 24px;
            border-radius: var(--radius);
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 600;
            font-size: 1.1em;
            border: 1px solid rgba(239, 68, 68, 0.8) !important;
            backdrop-filter: blur(5px);
        }}

        .emergency_button:hover {{ /* <-- CHANGE THIS LINE for hover too */
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            background: linear-gradient(135deg, rgba(220, 38, 38, 1) 0%, rgba(185, 28, 28, 1) 100%) !important;
        }}
        
        /* Sidebar section styling */
        /* Note: Removed .sidebar-section class from Python, keeping styling for potential future use */
        .sidebar-section {{
            background: var(--light-transparent-bg) !important;
            border-radius: var(--radius-lg);
            padding: 16px !important;
            margin-bottom: 16px;
            border: 1px solid var(--light-transparent-border) !important;
            backdrop-filter: blur(10px);
        }}
        
        /* Button styling - comprehensive */
        button, 
        .stButton > button,
        .stDownloadButton > button,
        .stFormSubmitButton > button,
        [data-baseweb="button"] {{
            background: var(--light-transparent-bg) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--light-transparent-border) !important;
            border-radius: var(--radius) !important;
            padding: 12px 16px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            font-family: 'Inter', sans-serif !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
            backdrop-filter: blur(5px) !important;
        }}
        
        button:hover, 
        .stButton > button:hover,
        .stDownloadButton > button:hover,
        .stFormSubmitButton > button:hover,
        [data-baseweb="button"]:hover {{
            background: var(--light-transparent-bg-hover) !important;
            color: var(--primary-color) !important;
            border-color: var(--primary-color) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        }}
        
        /* Primary buttons */
        .stButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"] {{
            background: rgba(99, 102, 241, 0.7) !important;
            color: white !important;
            font-weight: 700 !important;
        }}
        
        .stButton > button[kind="primary"]:hover,
        .stFormSubmitButton > button[kind="primary"]:hover {{
            background: rgba(99, 102, 241, 0.9) !important;
            color: white !important;
        }}
        
        /* Active conversation styling */
        /* This targets primary buttons specifically within the sidebar */
        .stApp [data-testid="stSidebar"] .stButton button[data-testid*="stButton-primary"] {{
            background: var(--active-conversation-bg) !important;
            color: white !important;
            border: 2px solid var(--active-conversation-border) !important;
            box-shadow: 0 6px 20px var(--active-conversation-shadow) !important;
            font-weight: 700 !important;
            transform: translateX(8px) scale(1.02) !important;
        }}
        
        /* Sidebar toggle button */
        .stApp [data-testid="stSidebarToggleButton"] button,
        button[data-testid="stSidebarToggleButton"] {{
            background: var(--light-transparent-bg) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--light-transparent-border) !important;
            border-radius: 50% !important;
            width: 40px !important;
            height: 40px !important;
            font-size: 20px !important;
            font-weight: 900 !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
        }}
        
        /* Form input styling */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {{ /* Added textarea for mood journal */
            background: var(--surface) !important;
            border: 2px solid var(--border) !important;
            border-radius: var(--radius) !important;
            padding: 12px 16px !important;
            font-size: 1em !important;
            color: white; !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.2s ease !important;
            backdrop-filter: blur(5px) !important;
        }}
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
            outline: none !important;
        }}
        
        /* Sidebar styling */
        .stApp [data-testid="stSidebar"] {{
            background: var(--surface) !important;
            border-right: 1px solid var(--border-light) !important;
            box-shadow: 4px 0 24px var(--shadow-lg) !important;
            backdrop-filter: blur(10px) !important;
        }}
        
        /* Text in sidebar - dark for readability */
        .stApp [data-testid="stSidebar"] h1,
        .stApp [data-testid="stSidebar"] h2,
        .stApp [data-testid="stSidebar"] h3,
        .stApp [data-testid="stSidebar"] h4,
        .stApp [data-testid="stSidebar"] p,
        .stApp [data-testid="stSidebar"] label,
        .stApp [data-testid="stSidebar"] .stMarkdown {{
            color: var(--text-primary) !important;
            text-shadow: none !important;
        }}
        
        /* Main content text - white for contrast against background */
        .stApp .main h1,
        .stApp .main h2,
        .stApp .main h3,
        .stApp .main h4,
        .stApp .main p,
        .stApp .main .stMarkdown {{
            color: white !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
        }}
        
        /* Info messages */
        .stInfo {{
            background: rgba(99, 102, 241, 0.2) !important;
            color: var(--text-primary) !important;
            border-radius: var(--radius) !important;
        }}
        
        .stSuccess {{
            background: rgba(16, 185, 129, 0.2) !important;
            color: #047857 !important;
            border-radius: var(--radius) !important;
        }}
        
        .stWarning {{
            background: rgba(245, 158, 11, 0.2) !important;
            color: #92400e !important;
            border-radius: var(--radius) !important;
        }}
        
        /* Hide default Streamlit elements */
        .stApp > header {{
            display: none !important;
        }}
        
        div[data-testid="stToolbar"] {{
            display: none !important;
        }}
        
        /* Responsive adjustments */
        @media (max-width: 768px) {{
            .main .block-container {{
                padding: 1rem;
            }}
            
            .user-message, .bot-message {{
                max-width: 90%;
                padding: 12px 16px;
            }}
            
            .main-header h1 {{
                font-size: 2em;
            }}
            
            .chat-container {{
                min-height: 400px;
                max-height: 500px;
                padding: 16px;
            }}
        }}

        /* New Chat button animation */
        .stButton > button[key="new_chat"] {{
            animation: pulse-glow 2s infinite ease-in-out;
        }}

        @keyframes pulse-glow {{
            0% {{ box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }}
            50% {{ box-shadow: 0 0 0 10px rgba(99, 102, 241, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }}
        }}

        /* Mood Selector Styling (st.radio) */
        .stRadio > label {{
            padding-bottom: 0px !important; /* Remove space below label */
        }}
        .stRadio div[data-testid="stOptions"] {{
            display: flex; /* Make radio options horizontal */
            justify-content: space-around;
            gap: 5px; /* Adjust spacing between options */
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: var(--radius);
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(3px);
            margin-bottom: 15px; /* Space below the mood selector */
        }}

        /* Style for individual radio option containers */
        .stRadio div[data-testid="stOption"] {{
            flex: 1; /* Distribute space evenly */
            text-align: center;
            margin: 0 !important; /* Remove default margin */
            padding: 0 !important;
        }}

        /* Style for the radio button and label inside each option */
        .stRadio div[data-testid="stOption"] > label {{
            display: flex;
            flex-direction: column; /* Stack radio button and label */
            align-items: center;
            justify-content: center;
            height: 100%; /* Ensure full height for clickable area */
            padding: 8px 0px; /* Adjust padding */
            border-radius: var(--radius);
            transition: all 0.2s ease;
            cursor: pointer;
            background-color: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: var(--text-primary);
            font-weight: 500;
        }}

        .stRadio div[data-testid="stOption"] > label:hover {{
            background-color: rgba(255, 255, 255, 0.4);
            transform: translateY(-2px);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }}

        /* Style for the actual radio input (hide default circle) */
        .stRadio input[type="radio"] {{
            /* Hide the default radio circle */
            position: absolute;
            opacity: 0;
            width: 0;
            height: 0;
        }}

        /* Style for the label when the radio is checked */
        .stRadio input[type="radio"]:checked + div > span {{
            /* This span usually contains the text */
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border-color: var(--primary-color);
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            /* Reset specific properties applied by Streamlit to the span directly */
            -webkit-text-fill-color: unset !important;
        }}

        /* Target the parent label of the checked radio button for the background/border */
        .stRadio input[type="radio"]:checked + div > label {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white !important; /* Ensure text is white */
            border-color: var(--primary-color) !important;
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}

        /* Make the text inside the radio button visible when checked */
        .stRadio input[type="radio"]:checked + div > label > div > p {{
            color: white !important;
        }}


        /* Resource Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px; /* Space between tabs */
        }}

        .stTabs [data-baseweb="tab"] {{
            background: var(--light-transparent-bg) !important;
            border: 1px solid var(--light-transparent-border) !important;
            border-radius: var(--radius) !important;
            padding: 10px 15px !important;
            transition: all 0.2s ease;
            color: var(--text-primary) !important;
            font-weight: 600;
        }}

        .stTabs [data-baseweb="tab"]:hover {{
            background: var(--light-transparent-bg-hover) !important;
            transform: translateY(-2px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            background: var(--active-conversation-bg) !important;
            color: white !important;
            border-color: var(--active-conversation-border) !important;
            box-shadow: 0 4px 12px var(--active-conversation-shadow) !important;
            transform: scale(1.02);
        }}

        .stTabs [data-baseweb="tab-panel"] {{
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            padding: 15px !important;
            margin-top: 10px;
            backdrop-filter: blur(8px);
        }}

    </style>
    """, unsafe_allow_html=True)