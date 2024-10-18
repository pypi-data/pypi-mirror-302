import os
import time
from base64 import b64encode

import requests
import streamlit as st
from logzero import logger
from simplesingletable import DynamoDbMemory

from supersullytools.llm.agent import AgentStates, ChatAgent
from supersullytools.llm.agent_tools.duckduckgo import get_ddg_tools
from supersullytools.llm.completions import CompletionHandler, ImagePromptMessage
from supersullytools.llm.trackers import CompletionTracker, DailyUsageTracking, GlobalUsageTracker, SessionUsageTracking
from supersullytools.streamlit.chat_agent_utils import ChatAgentUtils


@st.cache_resource
def get_memory() -> DynamoDbMemory:
    return DynamoDbMemory(logger=logger, table_name=os.environ.get("DYNAMODB_TABLE"))


@st.cache_resource
def get_completion_handler() -> CompletionHandler:
    memory = get_memory()
    trackers = get_trackers()
    completion_tracker = CompletionTracker(memory=memory, trackers=list(trackers))
    return CompletionHandler(
        logger=logger, debug_output_prompt_and_response=False, completion_tracker=completion_tracker
    )


@st.cache_resource
def get_session_usage_tracker() -> SessionUsageTracking:
    return SessionUsageTracking()


def get_trackers() -> tuple[GlobalUsageTracker, DailyUsageTracking, SessionUsageTracking]:
    memory = get_memory()
    global_tracker = GlobalUsageTracker.ensure_exists(memory)
    todays_tracker = DailyUsageTracking.get_for_today(memory)
    return global_tracker, todays_tracker, get_session_usage_tracker()


@st.cache_resource
def get_agent() -> ChatAgent:
    tool_profiles = {"all": [] + get_ddg_tools()}
    return ChatAgent(
        agent_description=(
            "You are playing the role of a magic mirror at a party; deliver a clever / witty response to the user "
            'as they chat with you. The "sessions" will always start with the famouse catch phrase. It is very important'
            "to keep your responses short, as they are being converted into sound via TTS and the experience is made "
            "worse if the responses are too long and take a while to beging playing. Similarly do not use markdown or "
            "fancy formatting in your responses, respond conversationally."
        ),
        logger=logger,
        completion_handler=get_completion_handler(),
        tool_profiles=tool_profiles,
    )


def get_photo_description(image) -> str:
    msg = (
        "You are part of a magic mirror AI system at a party; a user has just stepped up to "
        'your physical device and pressed the button to initiate a new "session"; provide a brief '
        "description of the user in the attached photo which will be given to the magic mirror chatbot AI "
        "as it chats with the user in the role of a magic mirror."
    )
    agent = get_agent()
    completion = agent.get_simple_completion(
        msg=ImagePromptMessage(
            content=msg,
            images=[b64encode(image.getvalue()).decode()],
            image_formats=["png"],
        ),
        # trying out Claude 3 Haiku, gpt-4o-mini
        model=agent.completion_handler.get_model_by_name_or_id("Claude 3 Haiku"),
    )
    return completion.content


def main():
    if "just_generated_audio" not in st.session_state:
        st.session_state.just_generated_audio = False

    with st.sidebar:
        model = ChatAgentUtils.select_llm(get_completion_handler(), label="LLM to use")

    def _agent():
        agent = get_agent()
        agent.default_completion_model = model
        return agent

    agent = _agent()
    agent_utils = ChatAgentUtils(agent)

    agent.completion_handler.completion_tracker.fixup_trackers()

    if "image_key" not in st.session_state:
        st.session_state.image_key = 1
        st.session_state.upload_images = []

    if "cam_input" not in st.session_state:
        st.session_state.cam_input = None

    if "image_description" not in st.session_state:
        st.session_state.image_description = None

    if st.session_state.cam_input:
        st.image(st.session_state.cam_input)

        if agent.working:
            with st.spinner("Agent working..."):
                while agent.working:
                    agent.run_agent()
                    time.sleep(0.05)

        def gch():
            return _agent().get_chat_history(True, False)

        if not gch():
            image_description = get_photo_description(st.session_state.cam_input)
            st.session_state.image_description = image_description
            agent.force_add_chat_msg(
                msg=(
                    "User description follows, respond as if the user had said to you "
                    '"Mirror mirror on the wall, who\'s the fairest of them all"\n\n'
                    f"<user_description>{image_description}</user_description>"
                ),
                role="system",
            )
            agent.current_state = AgentStates.received_message
            time.sleep(0.05)
            st.rerun()

        if chat_history := gch():

            def _reset():
                st.session_state.cam_input = None
                get_agent.clear()

            st.button("Reset", type="primary", on_click=_reset, help=st.session_state.image_description)
            st.write(chat_history[-1].content)

            st.audio(
                get_audio(chat_history[-1].content), format="audio/mp3", autoplay=st.session_state.just_generated_audio
            )
            st.session_state.just_generated_audio = False

            if chat_msg := st.chat_input("Talk to the mirror"):
                if agent_utils.add_user_message(chat_msg, st.session_state.upload_images):
                    if st.session_state.upload_images:
                        # clearing out the upload_images immediately causes weird IO errors, so
                        # just push to another key and overwrite it later
                        st.session_state.uploaded_images = st.session_state.upload_images
                        st.session_state.upload_images = []
                    time.sleep(0.01)
                    st.rerun()

    else:
        if not (cam_input := st.camera_input("cam", label_visibility="collapsed")):
            image = st.sidebar.file_uploader(
                "Image", type=["png", "jpg"], key=f"image-upload-{st.session_state.image_key}"
            )
            if image and st.sidebar.button("Add image to msg"):
                st.session_state.image_key += 1
                st.session_state.upload_images.append(image)
                time.sleep(0.01)
                st.rerun()

            if st.session_state.upload_images:
                with st.sidebar.expander("Pending Images", expanded=True):
                    for image in st.session_state.upload_images:
                        st.image(image)
                cam_input = st.session_state.upload_images[0]

        if not cam_input:
            # st.header("Step up and let the mirror take a look")
            get_agent.clear()
            st.stop()
        # st.image(cam_input)

        def _set():
            st.session_state.cam_input = cam_input

        st.button(
            "✨ Mirror, mirror on the wall, who's the fairest of them all? 🌟",
            on_click=_set,
            use_container_width=True,
            type="primary",
        )

    global_tracker, daily_tracker, session_tracker = get_trackers()
    with st.sidebar.container(border=True):
        st.subheader("Total Usage")
        global_tracker.render_completion_cost_as_expander()
        st.subheader("Daily Usage")
        daily_tracker.render_completion_cost_as_expander()
        st.subheader("Session Usage")
        session_tracker.render_completion_cost_as_expander()


@st.cache_data()
def get_audio(content):
    voice_id = "nDJIICjR9zfJExIFeSCN"
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

    headers = {
        "Accept": "application/json",
        "xi-api-key": os.environ["ELEVEN_LABS_API_TOKEN"],
        # "Content-Type": "application/json",
    }

    # Construct the URL for the Text-to-Speech API request

    # Set up headers for the API request, including the API key for authentication

    # Set up the data payload for the API request, including the text and voice settings
    data = {
        "text": content,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.0, "use_speaker_boost": True},
    }

    # Make the POST request to the TTS API with headers and data, enabling streaming response
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    # Check if the request was successful
    CHUNK_SIZE = 1024  # Size of chunks to read/write at a time

    if response.ok:
        # Collect the chunks into a single bytes object
        audio_data = b"".join(response.iter_content(chunk_size=CHUNK_SIZE))
        st.session_state.just_generated_audio = True
        return audio_data
    else:
        # Print the error message if the request was not successful
        st.error(response.text)


if __name__ == "__main__":
    main()
