import builtins
import importlib.util
from pathlib import Path

import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LinkedIn AI Writer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LOAD LANGGRAPH APP
# ============================================================

@st.cache_resource
def load_generator():
    """
    Loads the compiled LangGraph from 4_iterative_tools.py.

    The original file contains input() at the bottom.
    We temporarily override input() so importing the file
    doesn't start the CLI application.
    """

    file_path = Path(__file__).parent / "4_iterative_tools.py"

    if not file_path.exists():
        raise FileNotFoundError(
            "4_iterative_tools.py was not found in the same folder as app.py"
        )

    original_input = builtins.input

    # Prevent the CLI input() section from running
    builtins.input = lambda *args, **kwargs: ""

    try:
        spec = importlib.util.spec_from_file_location(
            "iterative_tools",
            file_path,
        )

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module.app

    finally:
        builtins.input = original_input


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(10, 102, 194, 0.08),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(124, 58, 237, 0.06),
                transparent 28%
            ),
            #f8fafc;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ---------- HERO ---------- */

    .hero {
        background: linear-gradient(
            135deg,
            #ffffff 0%,
            #f3f7ff 100%
        );

        border: 1px solid #e2e8f0;

        border-radius: 24px;

        padding: 2.2rem;

        margin-bottom: 1.5rem;

        box-shadow:
            0 10px 35px rgba(15, 23, 42, 0.06);
    }

    .hero-eyebrow {
        color: #0a66c2;

        font-size: 0.75rem;

        font-weight: 800;

        letter-spacing: 0.12em;

        text-transform: uppercase;

        margin-bottom: 0.5rem;
    }

    .hero-title {
        font-size: 2.6rem;

        font-weight: 800;

        line-height: 1.05;

        color: #111827;

        margin: 0;
    }

    .hero-description {
        color: #64748b;

        font-size: 1.05rem;

        line-height: 1.6;

        max-width: 750px;

        margin-top: 0.8rem;

        margin-bottom: 0;
    }


    /* ---------- SECTION HEADINGS ---------- */

    .section-title {
        font-size: 1.2rem;

        font-weight: 800;

        color: #111827;

        margin-top: 1rem;

        margin-bottom: 0.7rem;
    }


    /* ---------- POST CARD ---------- */

    .post-card {
        background: #ffffff;

        border: 1px solid #e5e7eb;

        border-radius: 20px;

        padding: 1.8rem;

        box-shadow:
            0 8px 30px rgba(15, 23, 42, 0.05);

        line-height: 1.75;

        color: #1f2937;

        font-size: 1.02rem;
    }

    .post-label {
        color: #0a66c2;

        font-size: 0.72rem;

        font-weight: 800;

        letter-spacing: 0.1em;

        text-transform: uppercase;

        margin-bottom: 1rem;
    }


    /* ---------- STATUS ---------- */

    .approved {
        background: #ecfdf5;

        border: 1px solid #a7f3d0;

        color: #047857;

        border-radius: 12px;

        padding: 0.85rem 1rem;

        font-weight: 700;
    }

    .rejected {
        background: #fff7ed;

        border: 1px solid #fed7aa;

        color: #c2410c;

        border-radius: 12px;

        padding: 0.85rem 1rem;

        font-weight: 700;
    }


    /* ---------- INFO CARD ---------- */

    .info-card {
        background: #eff6ff;

        border: 1px solid #dbeafe;

        border-radius: 14px;

        padding: 1rem;

        color: #334155;

        font-size: 0.9rem;

        line-height: 1.5;
    }


    /* ---------- BUTTONS ---------- */

    div.stButton > button {
        border-radius: 12px;

        font-weight: 700;

        min-height: 44px;
    }

    div.stButton > button[kind="primary"] {
        background: #0a66c2;

        border: none;
    }


    /* ---------- METRICS ---------- */

    div[data-testid="stMetric"] {
        background: white;

        border: 1px solid #e5e7eb;

        border-radius: 16px;

        padding: 0.8rem 1rem;
    }


    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #ffffff;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-eyebrow">
            ✦ AI Content Studio
        </div>

        <div class="hero-title">
            LinkedIn AI Writer
        </div>

        <p class="hero-description">
            Turn an idea into a publish-ready LinkedIn post.
            The AI researches when necessary, writes a draft,
            reviews it, and automatically improves it.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ✦ LinkedIn AI Writer")

    st.caption(
        "An iterative AI writing workflow powered by "
        "LangGraph, OpenAI, Groq and Tavily."
    )

    st.divider()

    st.markdown("### How it works")

    st.markdown(
        """
        **01 — Write**

        GPT creates the first draft.

        **02 — Research**

        Tavily searches the web when fresh
        information is needed.

        **03 — Review**

        A separate AI reviewer evaluates
        the post against your quality rules.

        **04 — Improve**

        If rejected, the writer receives
        the feedback and creates a better draft.
        """
    )

    st.divider()

    st.markdown("### Quality criteria")

    st.markdown(
        """
        ✓ Strong opening hook

        ✓ One clear takeaway

        ✓ Short paragraphs

        ✓ 150–200 words

        ✓ Engaging CTA/question

        ✓ Human professional tone

        ✓ No hashtags
        """
    )

    st.divider()

    st.caption("Maximum attempts: 3")


# ============================================================
# TOPIC INPUT
# ============================================================

st.markdown(
    '<div class="section-title">What do you want to write about?</div>',
    unsafe_allow_html=True,
)

# Example topics
examples = [
    "What I learned building my first AI agent",
    "Why data quality matters more than model size",
    "The hidden cost of AI data centers",
    "Lessons from automating a boring workflow",
]


# Session state for topic
if "topic" not in st.session_state:
    st.session_state.topic = ""


topic = st.text_area(
    "Topic",
    value=st.session_state.topic,
    placeholder=(
        "Enter a topic...\n\n"
        "Example: What I learned building my first AI agent"
    ),
    height=130,
    label_visibility="collapsed",
)


st.markdown("**Or try an example:**")

example_columns = st.columns(4)

for index, example in enumerate(examples):

    with example_columns[index]:

        if st.button(
            example,
            key=f"example_{index}",
            use_container_width=True,
        ):
            st.session_state.topic = example
            st.rerun()


# ============================================================
# GENERATE BUTTON
# ============================================================

st.write("")

generate_button = st.button(
    "✦ Generate LinkedIn Post",
    type="primary",
    use_container_width=True,
    disabled=not topic.strip(),
)


# ============================================================
# GENERATION
# ============================================================

if generate_button:

    # Save topic
    st.session_state.topic = topic.strip()

    try:

        generator = load_generator()

        initial_state = {
            "topic": topic.strip(),
            "messages": [],
            "draft": "",
            "review_feedback": "",
            "is_approved": False,
            "attempt": 0,
        }

        # Status UI
        with st.status(
            "Generating your LinkedIn post...",
            expanded=True,
        ) as status:

            st.write("✍️ Writer is creating a draft...")

            final_state = generator.invoke(initial_state)

            attempts = final_state.get("attempt", 0)

            approved = final_state.get(
                "is_approved",
                False,
            )

            if approved:

                status.update(
                    label="✓ Post approved and ready",
                    state="complete",
                    expanded=False,
                )

            else:

                status.update(
                    label=(
                        f"Generation finished after "
                        f"{attempts} attempt(s)"
                    ),
                    state="complete",
                    expanded=False,
                )


        # Store result
        st.session_state.result = final_state


    except Exception as error:

        st.error(
            "Something went wrong while generating the post."
        )

        with st.expander("Technical details"):

            st.exception(error)


# ============================================================
# DISPLAY RESULT
# ============================================================

if "result" in st.session_state:

    result = st.session_state.result

    draft = result.get(
        "draft",
        "",
    )

    feedback = result.get(
        "review_feedback",
        "",
    )

    approved = result.get(
        "is_approved",
        False,
    )

    attempts = result.get(
        "attempt",
        0,
    )


    st.divider()


    # ========================================================
    # RESULT LAYOUT
    # ========================================================

    post_column, review_column = st.columns(
        [2.2, 1],
        gap="large",
    )


    # ========================================================
    # POST
    # ========================================================

    with post_column:

        st.markdown(
            '<div class="section-title">Your LinkedIn Post</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="post-card">

                <div class="post-label">
                    Final Draft
                </div>

            """,
            unsafe_allow_html=True,
        )

        # Display the post
        st.markdown(draft)

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


        # Download
        if draft:

            st.write("")

            st.download_button(
                label="↓ Download Post",
                data=draft,
                file_name="linkedin_post.txt",
                mime="text/plain",
                use_container_width=True,
            )


    # ========================================================
    # REVIEW PANEL
    # ========================================================

    with review_column:

        st.markdown(
            '<div class="section-title">Quality Check</div>',
            unsafe_allow_html=True,
        )


        if approved:

            st.markdown(
                """
                <div class="approved">
                    ✓ Publish-ready
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                """
                <div class="rejected">
                    ↻ Needs improvement
                </div>
                """,
                unsafe_allow_html=True,
            )


        st.write("")


        # Metrics
        metric_1, metric_2 = st.columns(2)

        with metric_1:

            st.metric(
                "Attempts",
                attempts,
            )

        with metric_2:

            word_count = (
                len(draft.split())
                if draft
                else 0
            )

            st.metric(
                "Words",
                word_count,
            )


        # Reviewer feedback
        if feedback:

            st.write("")

            st.markdown("**Reviewer feedback**")

            st.info(feedback)


    # ========================================================
    # WORKFLOW SUMMARY
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">Generation Summary</div>',
        unsafe_allow_html=True,
    )

    summary_1, summary_2, summary_3 = st.columns(3)

    with summary_1:

        st.markdown(
            """
            <div class="info-card">
                <b>Writer</b><br>
                Generated and refined the LinkedIn post.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with summary_2:

        st.markdown(
            """
            <div class="info-card">
                <b>Reviewer</b><br>
                Evaluated the post against 7 quality criteria.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with summary_3:

        status_text = (
            "Approved ✓"
            if approved
            else "Maximum attempts reached"
        )

        st.markdown(
            f"""
            <div class="info-card">
                <b>Final Status</b><br>
                {status_text}
            </div>
            """,
            unsafe_allow_html=True,
        )


    # ========================================================
    # NEW POST
    # ========================================================

    st.write("")

    if st.button(
        "↻ Create Another Post",
        use_container_width=True,
    ):

        st.session_state.pop(
            "result",
            None,
        )

        st.session_state.topic = ""

        st.rerun()

