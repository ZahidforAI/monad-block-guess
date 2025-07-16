import streamlit as st
import requests
import time
import random

# Page config
st.set_page_config(
    page_title="⨀ Guess Monad Block",
    page_icon="⨀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'games_played' not in st.session_state:
    st.session_state.games_played = 0
if 'current_block' not in st.session_state:
    st.session_state.current_block = None
if 'game_history' not in st.session_state:
    st.session_state.game_history = []
if 'selected_digit' not in st.session_state:
    st.session_state.selected_digit = None
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'waiting'  # 'waiting', 'guessing', 'result'

# Enhanced CSS - Fixed footer positioning and layout
st.markdown("""
<style>
    /* Fix white bottom space - Force full height purple background */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #1e1b4b, #312e81, #4c1d95) !important;
        height: 100vh !important;
        min-height: 100vh !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* More comprehensive header and toolbar removal */
    .main .block-container {
        padding: 0.5rem 1rem !important;
        max-width: 100% !important;
        padding-top: 0rem !important;
        padding-bottom: 2rem !important;
        display: flex !important;
        flex-direction: column !important;
        min-height: calc(100vh - 3rem) !important;
    }
    
    /* Hide all Streamlit UI elements */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {visibility: hidden !important;}
    .stDecoration {visibility: hidden !important;}
    .stToolbar {visibility: hidden !important;}
    
    /* Hide the top header area completely */
    .stApp > header {display: none !important;}
    .stApp > div[data-testid="stToolbar"] {display: none !important;}
    section[data-testid="stSidebar"] {display: none !important;}
    
    /* Remove top padding from main container and fix background */
    .stApp {
        margin-top: -80px !important;
        background: linear-gradient(135deg, #1e1b4b, #312e81, #4c1d95) !important;
        height: 100vh !important;
        min-height: 100vh !important;
    }
    
    /* Hide toolbar and reduce top spacing */
    div[data-testid="stToolbar"] {
        visibility: hidden !important;
        height: 0% !important;
        position: fixed !important;
    }
    
    div[data-testid="stDecoration"] {
        visibility: hidden !important;
        height: 0% !important;
        position: fixed !important;
    }
    
    div[data-testid="stStatusWidget"] {
        visibility: hidden !important;
        height: 0% !important;
        position: fixed !important;
    }
    
    /* Remove spacing from top */
    .main > div {
        padding-top: 0rem !important;
    }
    
    /* Remove default margins from streamlit elements */
    .element-container {
        margin: 0 !important;
    }
    
    /* Remove blank spaces */
    .stMarkdown {
        margin: 0 !important;
    }
    
    /* Fix spinner and loading elements to match background */
    .stSpinner > div {
        background: transparent !important;
    }
    
    .stSpinner {
        background: transparent !important;
    }
    
    /* Remove any white backgrounds from containers */
    [data-testid="stAppViewContainer"] > .main {
        background: transparent !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #1e1b4b, #312e81, #4c1d95) !important;
    }
    
    /* Force all containers to have transparent background */
    .stContainer, .stColumn, .stColumns {
        background: transparent !important;
    }
    
    /* Main container adjustments for single page */
    .main {
        background: transparent !important;
        display: flex !important;
        flex-direction: column !important;
        flex: 1 !important;
    }
    
    /* Fix any remaining white spaces */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #1e1b4b, #312e81, #4c1d95);
        z-index: -1;
    }
    
    /* Create a flex container for the main content */
    .main-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-height: 0;
    }
    
    /* Title - reduced size */
    .game-title {
        background: linear-gradient(45deg, #8B5CF6, #A855F7, #C084FC);
        color: white;
        text-align: center;
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 0.5rem;
        margin-top: 0rem;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4); }
        to { box-shadow: 0 12px 35px rgba(139, 92, 246, 0.6); }
    }
    
    .game-title h1 {
        font-size: 3rem;
        margin: 0;
        color: #fff;
        text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fff;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        animation: glow 0.5s ease-in-out infinite alternate, slideIn 0.8s ease-out;
    }

    @keyframes glow {
        0% { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fff; }
        100% { text-shadow: 0 0 20px #fff, 0 0 30px #fff, 0 0 40px #fff; }
    }

    @keyframes slideIn {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* Stats bar - reduced size */
    .stats-bar {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .stat-item {
        background: rgba(139, 92, 246, 0.3);
        padding: 0.8rem 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        text-align: center;
        backdrop-filter: blur(10px);
        min-width: 100px;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
    }
    
    .stat-number {
        font-size: 1.5rem;
        font-weight: bold;
        color: #C084FC;
        margin: 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #DDD6FE;
        margin: 0;
    }
    
    /* Game panels - reduced size */
    .game-panel {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.2rem;
        margin: 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        color: white;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.2);
        height: fit-content;
    }
    
    /* Guess display - positioned at top */
    .guess-display {
        background: linear-gradient(45deg, #10B981, #059669);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
        animation: fadeIn 0.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .block-display {
        background: linear-gradient(45deg, #8B5CF6, #6366F1);
        color: white;
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .block-number {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.3rem 0;
    }
    
    /* Main button styling - compact */
    .stButton > button {
        background: linear-gradient(45deg, #8B5CF6, #6366F1) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 15px rgba(139, 92, 246, 0.4) !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.6) !important;
        background: linear-gradient(45deg, #A855F7, #8B5CF6) !important;
    }
    
    /* Result display - compact */
    .result-display {
        background: linear-gradient(45deg, #06D6A0, #8B5CF6);
        color: white;
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        animation: resultPulse 1s ease-in-out;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5);
    }
    
    .result-display.lose {
        background: linear-gradient(45deg, #EF476F, #F77F00);
        animation: shake 0.5s ease-in-out;
    }
    
    @keyframes resultPulse {
        0% { transform: scale(0.95); opacity: 0.8; }
        50% { transform: scale(1.05); opacity: 1; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    /* History - compact */
    .history-item {
        background: rgba(139, 92, 246, 0.2);
        padding: 0.7rem;
        border-radius: 12px;
        margin: 0.4rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    
    .history-item:hover {
        background: rgba(139, 92, 246, 0.3);
        transform: translateX(5px);
    }
    
    /* Selection display - compact */
    .selection-display {
        background: rgba(139, 92, 246, 0.4);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.8rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        animation: selectionPulse 1s ease-in-out;
    }
    
    @keyframes selectionPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Center content */
    .center-content {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    
    /* Compact side panels */
    .side-panel {
        max-height: 70vh;
        overflow-y: auto;
    }
    
    .side-panel h3 {
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    .side-panel p {
        font-size: 0.9rem;
        line-height: 1.6;
        margin: 0.5rem 0;
    }
    
    /* Fix for spinner background */
    .stSpinner > div > div {
        background: transparent !important;
        border-color: #8B5CF6 !important;
    }
    
    /* Remove any potential white overlays */
    .stApp > div {
        background: transparent !important;
    }
    
    /* Fix column background */
    .stColumn > div {
        background: transparent !important;
    }
    
  /* Fixed Footer - positioned at bottom */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        text-align: center;
        color: #DDD6FE;
        padding: 1rem;
        font-size: 0.9rem;
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.9), rgba(49, 46, 129, 0.9));
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 1000;
        animation: slideInFromBottom 0.8s ease-out;
    }
    
    @keyframes fadeInUp {
        0% { 
            transform: translateY(20px); 
            opacity: 0; 
        }
        100% { 
            transform: translateY(0); 
            opacity: 1; 
        }
    }
    
    /* Main content wrapper - no bottom padding needed anymore */
    .main-content-wrapper {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
</style>
""", unsafe_allow_html=True)

# Monad RPC configuration
MONAD_RPC_URL = "https://rpc.ankr.com/monad_testnet"

def get_latest_block():
    """Fetch the latest block from Monad testnet"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": [],
            "id": 1
        }
        response = requests.post(MONAD_RPC_URL, json=payload, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            block_number = int(result.get('result', '0x0'), 16)
            return block_number
        else:
            return random.randint(1000000, 9999999)
    except:
        return random.randint(1000000, 9999999)

def reset_game():
    """Reset game to initial state"""
    st.session_state.current_block = None
    st.session_state.selected_digit = None
    st.session_state.show_result = False
    st.session_state.game_state = 'waiting'

# Wrap main content
st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)

# Title
st.markdown("""
<div class="game-title">
    <h1>⨀ Guess Monad Block </h1>
</div>
""", unsafe_allow_html=True)

# Stats bar
win_rate = (st.session_state.score/max(st.session_state.games_played,1)*100) if st.session_state.games_played > 0 else 0
st.markdown(f"""
<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-number">{st.session_state.score}</div>
        <div class="stat-label">Score</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">{st.session_state.games_played}</div>
        <div class="stat-label">Games</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">{win_rate:.0f}%</div>
        <div class="stat-label">Win Rate</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main game area
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("""
    <div class="game-panel side-panel">
        <h3 style="color: #C084FC; text-align: center; margin-bottom: 1rem;">How to Play</h3>
        <div>
            <p>1. Click "Get Block" to fetch current block</p>
            <p>2. Guess the last digit of the next block</p>
            <p>3. Click a digit (0-9) to make your guess</p>
            <p>4. See if you're right and earn points!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:    
    # Get current block button
    if st.session_state.game_state == 'waiting':
        if st.button("⨀ Get Block", key="fetch_block"):
            # Use a placeholder instead of spinner to avoid the diagonal box
            placeholder = st.empty()
            placeholder.markdown("""
            <div style="text-align: center; color: #C084FC; padding: 1rem;">
                <div style="font-size: 1.2rem;">⏳ Fetching latest block...</div>
            </div>
            """, unsafe_allow_html=True)
            
            current_block = get_latest_block()
            st.session_state.current_block = current_block
            st.session_state.game_state = 'guessing'
            st.session_state.show_result = False
            st.session_state.selected_digit = None
            
            time.sleep(1)
            placeholder.empty()
            st.rerun()
    
    # Display current block and game interface
    if st.session_state.current_block and st.session_state.game_state in ['guessing', 'result']:
        # Show "Pick the last digit" message at the top
        if st.session_state.game_state == 'guessing':
            st.markdown("""
            <div class="guess-display">
                <strong>🎯 Pick the last digit of the next block</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # Then show the current block
        st.markdown(f"""
        <div class="block-display">
            <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">Current Block</div>
            <div class="block-number">#{st.session_state.current_block:,}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.game_state == 'guessing':
            # Use Streamlit columns for digit selection
            cols = st.columns(5)
            for i in range(10):
                col_idx = i % 5
                if i == 5:
                    cols = st.columns(5)
                
                with cols[col_idx]:
                    if st.button(str(i), key=f"digit_{i}"):
                        st.session_state.selected_digit = i
                        
                        # Process the guess immediately
                        next_block = st.session_state.current_block + random.randint(1, 3)
                        actual_digit = next_block % 10
                        is_correct = st.session_state.selected_digit == actual_digit
                        
                        # Update stats
                        st.session_state.games_played += 1
                        if is_correct:
                            st.session_state.score += 1
                        
                        # Add to history
                        st.session_state.game_history.append({
                            'block': next_block,
                            'guess': st.session_state.selected_digit,
                            'actual': actual_digit,
                            'correct': is_correct
                        })
                        
                        # Store result for display
                        st.session_state.next_block = next_block
                        st.session_state.actual_digit = actual_digit
                        st.session_state.is_correct = is_correct
                        st.session_state.game_state = 'result'
                        st.rerun()
        
        elif st.session_state.game_state == 'result':
            # Show selection
            st.markdown(f"""
            <div class="selection-display">
                <strong>You picked: {st.session_state.selected_digit}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Show result
            result_class = "result-display" if st.session_state.is_correct else "result-display lose"
            result_text = "🎉 CORRECT!" if st.session_state.is_correct else "❌ Wrong!"
            
            st.markdown(f"""
            <div class="{result_class}">
                <h3>{result_text}</h3>
                <p>Block #{st.session_state.next_block:,} → Last digit: <strong>{st.session_state.actual_digit}</strong></p>
                <p>{"Perfect guess! +1 point" if st.session_state.is_correct else "Try again!"}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.is_correct:
                st.balloons()
            
            # Play Again button
            if st.button("🎮 Play Again", key="play_again"):
                reset_game()
                st.rerun()

with col3:
    st.markdown("""
    <div class="game-panel side-panel">
        <h3 style="color: #C084FC; text-align: center; margin-bottom: 1rem;">Recent Games</h3>
    """, unsafe_allow_html=True)
    
    if st.session_state.game_history:
        recent = st.session_state.game_history[-8:]  # Show last 8 games
        for game in reversed(recent):
            emoji = "✅" if game['correct'] else "❌"
            st.markdown(f"""
            <div class="history-item">
                <span>{emoji} {game['guess']}→{game['actual']}</span>
                <small>#{game['block'] % 1000}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; color: #94A3B8; margin-top: 1rem;">
            <p>No games yet!</p>
            <p style="font-size: 0.8rem;">Start playing to see your history</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer - Now positioned as normal content at bottom (not fixed)
st.markdown("""
<div class="footer">
    🔗 Powered by Monad Testnet | Made by <a href="https://x.com/zahidaliAI" target="_blank" style="color:#FFFFFF; text-decoration:none;"><b>ZAHID 💜</b></a>
</div>
""", unsafe_allow_html=True)


# Close main content wrapper
st.markdown('</div>', unsafe_allow_html=True)