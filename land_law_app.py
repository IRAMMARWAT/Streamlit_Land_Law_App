import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

# Set page configuration
st.set_page_config(
    page_title="Land Law Notes",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #264653;
        border-left: 5px solid #2A9D8F;
        padding-left: 15px;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .topic-button {
        width: 100%;
        margin: 5px 0;
        padding: 12px;
        font-size: 1.1rem;
        background-color: #2A9D8F;
        color: white;
        border: none;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .topic-button:hover {
        background-color: #21867A;
        transform: translateY(-2px);
    }
    .definition-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #E76F51;
        margin: 15px 0;
    }
    .important-note {
        background-color: #FFF3CD;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #FFEAA7;
        margin: 15px 0;
    }
    .diagram-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = None

# Land Law Data
land_law_data = {
    "ownership_concepts": {
        "title": "Ownership Concepts",
        "definition": "Ownership refers to the legal right to possess, use, and dispose of property. In land law, ownership can be absolute or qualified.",
        "key_points": [
            "Absolute ownership gives complete control over the property",
            "Qualified ownership has restrictions or conditions",
            "Ownership can be transferred through sale, gift, or inheritance",
            "The concept of 'bundle of rights' includes possession, control, exclusion, and disposition"
        ],
        "diagram_data": {
            "labels": ["Possession", "Control", "Exclusion", "Disposition", "Enjoyment"],
            "values": [30, 25, 20, 15, 10]
        }
    },
    "easements": {
        "title": "Easements",
        "definition": "An easement is a non-possessory right to use another person's land for a specific purpose without taking anything from the land.",
        "key_points": [
            "Right of way (most common type)",
            "Right to light",
            "Right of support",
            "Easements must be created by grant, prescription, or implication",
            "Dominant tenement (benefits) vs Servient tenement (burdened)"
        ],
        "diagram_data": {
            "types": ["Right of Way", "Right to Light", "Easement of Support", "Easement of Parking"],
            "frequency": [45, 25, 20, 10]
        }
    },
    "leasehold": {
        "title": "Leasehold Estate",
        "definition": "A leasehold estate gives the tenant (lessee) the right to possess and use the property for a fixed period of time, as specified in the lease agreement.",
        "key_points": [
            "Fixed-term tenancy",
            "Periodic tenancy",
            "Tenancy at will",
            "Tenancy at sufferance",
            "Essential requirements: parties, property description, term, rent"
        ],
        "diagram_data": {
            "categories": ["Fixed Term", "Periodic", "At Will", "At Sufferance"],
            "duration_years": [5, 2, 0.5, 0.25]
        }
    },
    "covenants": {
        "title": "Covenants in Land Law",
        "definition": "A covenant is a promise made in a deed or other instrument by one party to do or not do certain things concerning the use of land.",
        "key_points": [
            "Positive covenants (require action)",
            "Negative/restrictive covenants (prohibit action)",
            "Covenants run with the land",
            "Touch and concern requirement",
            "Privity of estate"
        ],
        "diagram_data": {
            "stages": ["Creation", "Enforcement", "Modification", "Termination"],
            "complexity": [8, 9, 7, 6]
        }
    },
    "adverse_possession": {
        "title": "Adverse Possession",
        "definition": "Adverse possession, also known as squatter's rights, allows a person to claim ownership of land by occupying it for a specified period without the owner's permission.",
        "key_points": [
            "Actual possession",
            "Open and notorious",
            "Hostile possession",
            "Exclusive possession",
            "Continuous possession for statutory period"
        ],
        "diagram_data": {
            "years": [1, 5, 10, 15, 20],
            "success_rate": [5, 20, 50, 80, 95]
        }
    },
    "mortgages": {
        "title": "Mortgages and Charges",
        "definition": "A mortgage is a security interest in real property held by a lender as security for a debt, usually a loan of money.",
        "key_points": [
            "Mortgagor (borrower) vs Mortgagee (lender)",
            "Equity of redemption",
            "Foreclosure proceedings",
            "Power of sale",
            "Registration requirements"
        ],
        "diagram_data": {
            "parties": ["Mortgagor Rights", "Mortgagee Rights", "Third Party Interests"],
            "priority": [40, 45, 15]
        }
    },
    "registration": {
        "title": "Land Registration Systems",
        "definition": "Land registration systems provide a public record of interests in land and their ownership, making conveyancing simpler and more secure.",
        "key_points": [
            "Torrens system (title by registration)",
            "Deeds registration system",
            "Indefeasibility of title",
            "Mirror principle",
            "Curtain principle"
        ],
        "diagram_data": {
            "systems": ["Torrens System", "Deeds System", "Title Insurance"],
            "adoption_rate": [70, 25, 5]
        }
    }
}

# Function to create diagrams
def create_diagram(topic_key):
    data = land_law_data[topic_key]["diagram_data"]
    
    if topic_key == "ownership_concepts":
        fig = go.Figure(data=[go.Pie(
            labels=data["labels"],
            values=data["values"],
            hole=0.3,
            marker_colors=px.colors.qualitative.Set3
        )])
        fig.update_layout(
            title="Bundle of Rights in Ownership",
            height=400
        )
        return fig
    
    elif topic_key == "easements":
        fig = px.bar(
            x=data["types"],
            y=data["frequency"],
            title="Types of Easements and Their Frequency",
            labels={'x': 'Easement Type', 'y': 'Frequency (%)'},
            color=data["types"],
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        return fig
    
    elif topic_key == "leasehold":
        fig = px.line(
            x=data["categories"],
            y=data["duration_years"],
            title="Typical Duration of Leasehold Types",
            markers=True,
            line_shape='spline'
        )
        fig.update_traces(line=dict(width=3))
        return fig
    
    elif topic_key == "covenants":
        fig = px.area(
            x=data["stages"],
            y=data["complexity"],
            title="Complexity at Different Stages of Covenant",
            line_shape='spline'
        )
        return fig
    
    elif topic_key == "adverse_possession":
        fig = px.scatter(
            x=data["years"],
            y=data["success_rate"],
            title="Success Rate of Adverse Possession Claims Over Time",
            trendline="ols",
            size=data["years"]
        )
        return fig
    
    elif topic_key == "mortgages":
        fig = px.pie(
            values=data["priority"],
            names=data["parties"],
            title="Priority of Interests in Mortgage Transactions",
            hole=0.4
        )
        return fig
    
    elif topic_key == "registration":
        fig = px.bar_polar(
            r=data["adoption_rate"],
            theta=data["systems"],
            title="Adoption Rate of Land Registration Systems",
            color=data["systems"],
            template="plotly_dark"
        )
        return fig

# Main App
def main():
    # Header
    st.markdown('<div class="main-header">🏛️ Land Law Notes & Study Guide</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2091/2091340.png", width=100)
        st.markdown("### 📚 Topics")
        st.markdown("---")
        
        # Create buttons for each topic
        for topic_key, topic_info in land_law_data.items():
            if st.button(f"📖 {topic_info['title']}", key=f"btn_{topic_key}", use_container_width=True):
                st.session_state.current_topic = topic_key
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        st.metric("Total Topics", len(land_law_data))
        st.metric("Key Concepts", sum(len(info['key_points']) for info in land_law_data.values()))
        
        st.markdown("---")
        st.markdown("### 📥 Export Options")
        if st.button("📄 Export Notes as Text"):
            export_notes()
        
        if st.button("📈 Export All Diagrams"):
            export_all_diagrams()
    
    # Main content area
    if st.session_state.current_topic:
        display_topic_content(st.session_state.current_topic)
    else:
        display_homepage()

def display_homepage():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## Welcome to Land Law Notes")
        st.markdown("""
        This comprehensive guide covers essential topics in Land Law. Use the sidebar to navigate 
        through different topics. Each topic includes:
        
        - **Clear Definitions** of key concepts
        - **Detailed Explanations** with examples
        - **Visual Diagrams** for better understanding
        - **Important Points** highlighted for study
        
        ### How to Use This Guide:
        1. Select a topic from the sidebar
        2. Study the definitions and key points
        3. Review the diagrams for visual understanding
        4. Use the export features to save your notes
        """)
        
        st.markdown("### 📈 Overview of Topics")
        topics_df = pd.DataFrame({
            'Topic': [info['title'] for info in land_law_data.values()],
            'Key Points': [len(info['key_points']) for info in land_law_data.values()],
            'Complexity': [3, 4, 2, 4, 5, 4, 3]  # Example complexity ratings
        })
        st.dataframe(topics_df, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Quick Navigation")
        
        # Quick topic buttons
        cols = st.columns(2)
        for idx, (topic_key, topic_info) in enumerate(land_law_data.items()):
            with cols[idx % 2]:
                if st.button(topic_info['title'], key=f"home_{topic_key}"):
                    st.session_state.current_topic = topic_key
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### 🔍 Search Notes")
        search_term = st.text_input("Enter search term:")
        if search_term:
            search_results = []
            for topic_key, topic_info in land_law_data.items():
                if (search_term.lower() in topic_info['definition'].lower() or 
                    any(search_term.lower() in point.lower() for point in topic_info['key_points'])):
                    search_results.append(topic_info['title'])
            
            if search_results:
                st.write("Found in:", ", ".join(search_results))
            else:
                st.write("No results found")

def display_topic_content(topic_key):
    topic = land_law_data[topic_key]
    
    # Header with back button
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(f'<div class="sub-header">{topic["title"]}</div>', unsafe_allow_html=True)
    with col2:
        if st.button("← Back"):
            st.session_state.current_topic = None
            st.rerun()
    
    # Definition
    st.markdown("### 📝 Definition")
    st.markdown(f'<div class="definition-box">{topic["definition"]}</div>', unsafe_allow_html=True)
    
    # Key Points
    st.markdown("### 🔑 Key Points")
    for point in topic["key_points"]:
        st.markdown(f"✅ {point}")
    
    # Diagram
    st.markdown("### 📊 Visual Representation")
    st.markdown('<div class="diagram-container">', unsafe_allow_html=True)
    fig = create_diagram(topic_key)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed Explanation
    st.markdown("### 📖 Detailed Explanation")
    
    # Different explanations for different topics
    explanations = {
        "ownership_concepts": """
        **Ownership Concepts in Detail:**
        
        Ownership in land law is often described as a "bundle of rights." This metaphor helps understand 
        that ownership isn't a single right but a collection of different rights:
        
        1. **Right to Possess**: Physical control over the property
        2. **Right to Use**: How the property can be utilized
        3. **Right to Exclude**: Ability to prevent others from entering
        4. **Right to Dispose**: Ability to sell, gift, or transfer
        5. **Right to Enjoy**: Freedom from interference
        
        **Types of Ownership:**
        - **Fee Simple Absolute**: Highest form of ownership
        - **Life Estate**: Ownership for duration of a person's life
        - **Fee Tail**: Restricted inheritance patterns
        - **Future Interests**: Rights that become possessory in the future
        """,
        
        "easements": """
        **Easements Explained:**
        
        An easement creates a non-possessory interest in another's land. Key characteristics:
        
        **Essential Elements:**
        1. There must be a dominant and servient tenement
        2. The easement must accommodate the dominant tenement
        3. The tenements must be owned/occupied by different persons
        4. The easement must be capable of forming the subject matter of a grant
        
        **Creation Methods:**
        - **Express Grant**: Written agreement between parties
        - **Prescription**: Long use without permission
        - **Implied Grant**: Necessity or common intention
        - **Statute**: Created by legislation
        
        **Termination:**
        - Release by the dominant owner
        - Unity of ownership
        - Abandonment
        - Expiration of purpose
        """,
        
        "leasehold": """
        **Leasehold Estate Details:**
        
        A leasehold is a contractual arrangement creating a landlord-tenant relationship.
        
        **Essential Requirements:**
        1. **Exclusive Possession**: Tenant must have exclusive control
        2. **Fixed Term**: Definite period or periodic arrangement
        3. **Rent**: Consideration (though not always required)
        
        **Types of Tenancies:**
        - **Fixed Term**: Specific end date
        - **Periodic**: Renews automatically (month-to-month)
        - **Tenancy at Will**: No fixed term, terminable by either party
        - **Tenancy at Sufferance**: Holdover after lease expires
        
        **Rights and Duties:**
        - **Landlord's duties**: Quiet enjoyment, repairs (in some cases)
        - **Tenant's duties**: Pay rent, avoid waste, return possession
        """,
        
        "covenants": """
        **Covenants in Depth:**
        
        Covenants can be either positive (requiring action) or negative (prohibiting action).
        
        **Requirements for Running with Land:**
        1. **Touch and Concern**: Must affect land value/use
        2. **Intent**: Original parties must intend it to run
        3. **Notice**: Subsequent purchasers must have notice
        4. **Privity**: Legal relationship between parties
        
        **Enforcement:**
        - **At Law**: Between original covenantor and covenantee
        - **In Equity**: Against subsequent owners with notice
        - **Defenses**: Changed circumstances, acquiescence, statutory modification
        
        **Common Examples:**
        - Building restrictions
        - Maintenance obligations
        - Use restrictions (residential only)
        - Architectural controls
        """,
        
        "adverse_possession": """
        **Adverse Possession Requirements:**
        
        To successfully claim adverse possession, all elements must be proven:
        
        1. **Actual Possession**: Physical occupation and control
        2. **Open and Notorious**: Visible and obvious to true owner
        3. **Hostile/Adverse**: Without owner's permission
        4. **Exclusive**: Not shared with true owner
        5. **Continuous**: Uninterrupted for statutory period
        
        **Statutory Periods Vary:**
        - Typically 10-20 years depending on jurisdiction
        - Some jurisdictions require payment of taxes
        - Color of title may reduce required period
        
        **Policy Justifications:**
        - Encourages land use
        - Resolves stale claims
        - Protects settled expectations
        - Quietens title
        """,
        
        "mortgages": """
        **Mortgage Law Principles:**
        
        A mortgage involves transferring an interest in land as security for debt.
        
        **Key Concepts:**
        - **Equity of Redemption**: Borrower's right to repay and reclaim property
        - **Foreclosure**: Court-ordered termination of redemption rights
        - **Power of Sale**: Lender's right to sell without court order
        - **Priority Rules**: Determine order of payment among creditors
        
        **Types of Mortgages:**
        - **First Mortgage**: Highest priority
        - **Second Mortgage**: Subordinate position
        - **Reverse Mortgage**: Payments to homeowner
        - **Chattel Mortgage**: On personal property
        
        **Default Remedies:**
        - Judicial foreclosure
        - Non-judicial foreclosure
        - Strict foreclosure
        - Deed in lieu of foreclosure
        """,
        
        "registration": """
        **Land Registration Systems:**
        
        Modern systems aim to simplify conveyancing and provide certainty.
        
        **Torrens System Features:**
        1. **Mirror Principle**: Register reflects all interests
        2. **Curtain Principle**: No need to investigate past transactions
        3. **Insurance Principle**: State guarantees title
        4. **Indefeasibility**: Registered title is secure
        
        **Registration Types:**
        - **Title Registration**: Registers ownership itself
        - **Deeds Registration**: Registers documents affecting title
        - **Plurality Systems**: Combine elements of both
        
        **Advantages:**
        - Security of title
        - Simplified transactions
        - Reduced investigation costs
        - Fraud prevention
        - Marketability improvement
        """
    }
    
    st.markdown(f'<div class="important-note">{explanations.get(topic_key, "Detailed explanation coming soon...")}</div>', unsafe_allow_html=True)
    
    # Case Examples (when applicable)
    if topic_key in ["easements", "covenants", "adverse_possession"]:
        st.markdown("### ⚖️ Case Examples")
        if topic_key == "easements":
            st.markdown("""
            **Famous Cases:**
            - *Re Ellenborough Park* (1956): Established requirements for valid easement
            - *Wheeldon v Burrows* (1879): Implied easements on severance
            - *Hill v Tupper* (1863): Commercial benefit doesn't create easement
            """)
        elif topic_key == "covenants":
            st.markdown("""
            **Landmark Cases:**
            - *Tulk v Moxhay* (1848): Established restrictive covenants in equity
            - *Austerberry v Corporation of Oldham* (1885): Positive covenants don't run at law
            - *Rhone v Stephens* (1994): Modern approach to covenant enforcement
            """)
    
    # Study Tips
    st.markdown("### 🎓 Study Tips")
    st.markdown("""
    1. Create flashcards for key definitions
    2. Draw diagrams to visualize relationships
    3. Practice applying concepts to hypotheticals
    4. Review landmark cases for each topic
    5. Understand policy reasons behind rules
    """)

def export_notes():
    """Export all notes as a text file"""
    notes_text = "LAND LAW NOTES - COMPREHENSIVE GUIDE\n"
    notes_text += "=" * 50 + "\n\n"
    
    for topic_key, topic_info in land_law_data.items():
        notes_text += f"TOPIC: {topic_info['title']}\n"
        notes_text += "-" * 30 + "\n"
        notes_text += f"Definition: {topic_info['definition']}\n\n"
        notes_text += "Key Points:\n"
        for point in topic_info['key_points']:
            notes_text += f"  • {point}\n"
        notes_text += "\n" + "=" * 50 + "\n\n"
    
    # Create download link
    b64 = base64.b64encode(notes_text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="land_law_notes.txt">Click to download notes</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

def export_all_diagrams():
    """Export all diagrams as HTML"""
    import plotly.io as pio
    
    html_content = "<html><head><title>Land Law Diagrams</title></head><body>"
    html_content += "<h1>Land Law - All Diagrams</h1>"
    
    for topic_key, topic_info in land_law_data.items():
        html_content += f"<h2>{topic_info['title']}</h2>"
        fig = create_diagram(topic_key)
        html_content += pio.to_html(fig, full_html=False)
        html_content += "<hr>"
    
    html_content += "</body></html>" 
    
    
    # Create download link
    b64 = base64.b64encode(html_content.encode()).decode()
    href = f'<a href="data:file/html;base64,{b64}" download="land_law_diagrams.html">Download all diagrams</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main() 
    
  