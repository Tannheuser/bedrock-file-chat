from pathlib import Path
import base64
import streamlit as st


class Layout:
    def __init__(
        self,
    ):
        assets_dir = Path(__file__).parents[1] / "assets"
        css_path = assets_dir / "styles/layout.css"

        self.custom_css = f"<style>{css_path.read_text()}</style>"
        self.favicon_path = assets_dir / "images/brain.svg"
        self.logo_path = assets_dir / "images/logo.png"

    @staticmethod
    def get_image_data_url(path: Path, content_type: str) -> str:
        with path.open("rb") as file:
            return f"data:image/{content_type};base64,{base64.b64encode(file.read()).decode()}"

    def init(self):
        st.set_page_config(
            page_icon=self.get_image_data_url(self.favicon_path, "svg+xml"),
            page_title="Bedrock File Chat",
        )
        st.write(self.custom_css, unsafe_allow_html=True)
        st.write(
            '<div class="header">'
            '<div class="logo">'
            f'<img src="{self.get_image_data_url(self.logo_path, "png")}" alt="Logo">'
            "</div>"
            '<div class="title">Bedrock File Chat</div>'
            "</div>",
            unsafe_allow_html=True,
        )
