import streamlit as st
import base64 # Import base64 to encode the image

def get_base64_of_bin_file(bin_file):
    """Encodes a binary file (like an image) to base64."""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def apply_custom_css():
    """Applies custom CSS to the Streamlit application for enhanced styling."""

    # Path to your background image (adjust this path if your image is in a different folder)
    background_image_path = "PeacePulseLogo.png" # Assuming 'images' folder in your root

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
            /* Update surface colors to be transparent with a slight tint */
            --surface: rgba(255, 255, 255, 0.2); /* Slightly transparent white */
            --surface-alt: rgba(255, 255, 255, 0.1); /* Even more transparent for subtle distinction */
            --text-primary: #1e293b; /* Keep text readable */
            --text-secondary: #64748b;
            --text-muted: #94a3b8;
            --border: rgba(255, 255, 255, 0.3); /* Transparent border */
            --border-light: rgba(255, 255, 255, 0.15); /* Lighter transparent border */
            --shadow: rgba(0, 0, 0, 0.1); /* Darker shadow for distinction */
            --shadow-lg: rgba(0, 0, 0, 0.2);
            --radius: 12px;
            --radius-lg: 16px;
        }}

        /* Global styles - Set the background image */
        .stApp {{
            background-image: url("data:image/jpeg;base64,{base64_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed; /* Keeps background fixed when scrolling */
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
            background: rgba(0, 0, 0, 0.3); /* Dark overlay, adjust opacity as needed */
            z-index: -1; /* Place behind content */
        }}


        .main .block-container {{
            padding-top: 0rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }}

        /* Chat container with improved styling - now transparent */
        .chat-container {{
            background: var(--surface); /* Use transparent surface color */
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
        }}

        .chat-container::-webkit-scrollbar {{
            width: 6px;
        }}

        .chat-container::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.1); /* Transparent scrollbar track */
            border-radius: 3px;
        }}

        .chat-container::-webkit-scrollbar-thumb {{
            background: rgba(255, 255, 255, 0.4); /* Transparent scrollbar thumb */
            border-radius: 3px;
        }}

        .chat-container::-webkit-scrollbar-thumb:hover {{
            background: rgba(255, 255, 255, 0.6);
            border-radius: 3px;
        }}

        /* User message with better contrast (can keep gradient or make transparent) */
        .user-message {{
            background: rgba(99, 102, 241, 0.7); /* Slightly transparent primary color */
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
        }}

        /* Bot message with improved readability - now transparent */
        .bot-message {{
            background: var(--surface-alt); /* Use transparent surface-alt */
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
        }}

        /* Welcome message - now transparent or with gradient */
        .welcome-message {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.7) 0%, rgba(236, 72, 153, 0.7) 100%); /* Transparent gradient */
            color: white;
            padding: 24px;
            border-radius: var(--radius-lg);
            margin: 24px auto;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            font-weight: 500;
            line-height: 1.6;
        }}

        /* Message time styling (ensure readability on image background) */
        .message-time {{
            font-size: 0.75em;
            opacity: 0.9; /* Make it a bit more opaque for readability */
            margin-top: 8px;
            text-align: right;
            font-weight: 400;
            color: rgba(255, 255, 255, 0.8); /* Lighter color for better contrast */
        }}

        /* Enhanced header - now transparent */
        .main-header {{
            text-align: center;
            padding: 32px 24px;
            background: var(--surface); /* Use transparent surface color */
            color: var(--text-primary);
            border-radius: var(--radius-lg);
            margin-bottom: 24px;
            box-shadow: 0 8px 32px var(--shadow-lg);
            border: 1px solid var(--border-light);
            position: relative;
            overflow: hidden;
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
            color: var(--text-primary); /* Keep text readable */
            font-weight: 500;
        }}

        /* Emergency button with better accessibility - can keep current or adjust opacity */
        .emergency-button {{
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.8) 0%, rgba(220, 38, 38, 0.8) 100%); /* Slightly transparent */
            color: white;
            padding: 18px 24px;
            border-radius: var(--radius);
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 600;
            font-size: 1.1em;
            border: none;
        }}

        .emergency-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            background: linear-gradient(135deg, rgba(220, 38, 38, 0.9) 0%, rgba(185, 28, 28, 0.9) 100%);
        }}

        /* Sidebar content styling - now transparent */
        .sidebar-content {{
            background: var(--surface); /* Use transparent surface color */
            border-radius: var(--radius-lg);
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 16px var(--shadow);
            border: 1px solid var(--border-light);
        }}

        /* Button improvements - now transparent */
        .stButton > button {{
            background: rgba(255, 255, 255, 0.1); /* Slightly transparent button background */
            color: var(--text-primary); /* Keep text readable */
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 12px 16px;
            font-weight: 500;
            transition: all 0.2s ease;
            width: 100%;
            font-family: 'Inter', sans-serif;
        }}

        .stButton > button:hover {{
            background: rgba(255, 255, 255, 0.2); /* Slightly more opaque on hover */
            border-color: var(--primary-color);
            color: var(--primary-color);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px var(--shadow);
        }}

        /* Target the specific sidebar toggle button by its key or a specific ancestor */
        .stButton button[key="persistent_sidebar_toggle"] {{
            background: rgba(99, 102, 241, 0.8); /* Transparent primary color */
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            margin: 0;
            padding: 0;
            line-height: 1;
        }}

        .stButton button[key="persistent_sidebar_toggle"]:hover {{
            background: rgba(79, 70, 229, 0.9); /* Slightly more opaque on hover */
            transform: scale(1.1);
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.4);
        }}


        /* Form input styling - now transparent */
        .stTextInput > div > div > input {{
            background: var(--surface); /* Transparent background for input */
            border: 2px solid var(--border);
            border-radius: var(--radius);
            padding: 12px 16px;
            font-size: 1em;
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            transition: all 0.2s ease;
        }}

        .stTextInput > div > div > input:focus {{
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
            outline: none;
        }}

        /* Select slider improvements - now transparent */
        .stSelectSlider > div > div {{
            background: var(--surface-alt); /* Transparent background */
            border-radius: var(--radius);
            padding: 8px;
        }}

        /* Expander styling - now transparent */
        .streamlit-expander {{
            background: var(--surface); /* Transparent background */
            border: 1px solid var(--border);
            border-radius: var(--radius);
            margin-bottom: 12px;
            box-shadow: 0 2px 8px var(--shadow);
        }}

        .streamlit-expander > summary {{
            background: var(--surface-alt); /* Transparent background for summary */
            color: var(--text-primary);
            font-weight: 600;
            padding: 16px;
            border-radius: var(--radius);
        }}

        /* Info and success message styling - now transparent */
        .stInfo, .stSuccess, .stWarning {{
            border-radius: var(--radius);
            border: none;
            font-weight: 500;
            /* Adjust transparency as needed */
        }}

        .stInfo {{
            background: rgba(99, 102, 241, 0.2); /* More transparent */
            color: var(--text-primary);
        }}

        .stSuccess {{
            background: rgba(16, 185, 129, 0.2); /* More transparent */
            color: #047857;
        }}

        .stWarning {{
            background: rgba(245, 158, 11, 0.2); /* More transparent */
            color: #92400e;
        }}

        /* Typography improvements - ensure readability on image background */
        h1, h2, h3, h4, h5, h6 {{
            color: white; /* Make headings white for contrast */
            font-weight: 600;
            line-height: 1.3;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5); /* Add subtle text shadow */
        }}

        p, label, .stMarkdown, .stText {{ /* Target common text elements */
            color: white; /* Make paragraphs white for contrast */
            line-height: 1.6;
            text-shadow: 0.5px 0.5px 1px rgba(0,0,0,0.3); /* Add subtle text shadow */
        }}

        /* Loading spinner */
        .stSpinner > div {{
            border-color: var(--primary-color) !important;
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

        /* Hide default Streamlit elements */
        .stApp > header {{
            display: none !important;
        }}

        div[data-testid="stToolbar"] {{
            display: none !important;
        }}

        /* Ensure sidebar styling applies to the actual Streamlit sidebar */
        .stApp [data-testid="stSidebar"] {{
            background: var(--surface); /* Use transparent surface color for sidebar */
            border-right: 1px solid var(--border-light);
            box-shadow: 4px 0 24px var(--shadow-lg);
        }}

    </style>
    """, unsafe_allow_html=True)