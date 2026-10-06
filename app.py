import streamlit as st
from chatbot import get_answer
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()


# ============================================================
# PROCESS QUESTION
# ============================================================

def process_question(question):

    answer = get_answer(question)

    st.session_state.history.append({
        "question": question,
        "answer": answer
    })

    return answer


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚙️ Settings")

    # CLEAR CHAT
    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.history = []

        st.rerun()


    st.markdown("---")


    # QUICK HELP
    st.subheader("⚡ Quick Help")

    quick_questions = [
        (
            "📦 Track Order",
            "How can I track my order?"
        ),
        (
            "🔄 Return Product",
            "Can I return a product?"
        ),
        (
            "💳 Payment Methods",
            "What payment methods are available?"
        ),
        (
            "🚚 Delivery Time",
            "What is the standard delivery time?"
        )
    ]


    for button_name, question_text in quick_questions:

        if st.button(
            button_name,
            use_container_width=True
        ):

            process_question(question_text)

            st.rerun()


    st.markdown("---")


    # QUESTION COUNT
    st.subheader("💬 Questions")

    st.write(
        f"Total questions: {len(st.session_state.history)}"
    )


    st.markdown("---")


    # CHAT HISTORY
    st.subheader("💬 Chat History")


    if not st.session_state.history:

        st.caption(
            "No conversations yet."
        )

    else:

        for i, message in enumerate(
            st.session_state.history,
            start=1
        ):

            st.write(
                f"**{i}.** {message['question']}"
            )


    st.markdown("---")


    # START TIME
    st.caption(
        "Started: "
        + st.session_state.start_time.strftime(
            "%I:%M %p"
        )
    )


# ============================================================
# MAIN PAGE
# ============================================================

st.title(
    "🤖 AI Customer Support"
)

st.caption(
    "Your intelligent customer support assistant"
)


st.info(
    "📦 Orders   "
    "💳 Payments   "
    "🚚 Delivery   "
    "🔄 Returns   "
    "💰 Refunds   "
    "✈️ Travel   "
    "🍔 Food"
)


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.history:

    with st.chat_message("user"):

        st.write(
            message["question"]
        )


    with st.chat_message("assistant"):

        st.write(
            message["answer"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask your customer-support question..."
)


# ============================================================
# NEW QUESTION
# ============================================================

if question:

    process_question(question)

    st.rerun()