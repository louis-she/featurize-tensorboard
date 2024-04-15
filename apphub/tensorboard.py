import os

import gradio as gr

from apphub.app import App, AppOption


class Tensorboard(App):

    class TensorboardOption(AppOption):
        conda_env: str = "base"

    cfg: TensorboardOption

    @property
    def key(self):
        """key 是应用的唯一标识，用于在数据库中查找应用，所以这个值应该是唯一的"""
        return "tensorboard"

    @property
    def port(self):
        """应用的端口号"""
        return 20005

    def render_installation_page(self) -> "gr.Blocks":
        with gr.Blocks() as b:
            gr.Markdown(
                """# 安装 TensorBoard

TensorBoard 可视化面板
"""
            )
            install_location = self.render_install_location(allow_work=True)
            conda_env = self.render_conda_env_selector(info="尽量就直接用 base 环境安装 TensorBoard，除非你知道自己在做什么。")
            self.render_installation_button(
                inputs=[install_location, conda_env]
            )
            self.render_log()
        return b

    def installation(self, *args):
        super().installation(*args)
        with self.conda_activate(self.cfg.conda_env):
            self.execute_command("pip install tensorboard")
        self.save_app_config()
        self.app_installed()

    def render_start_page(self) -> "gr.Blocks":
        with gr.Blocks() as b:
            gr.Markdown("""# 启动 TensorBoard""")
            log_path = gr.Textbox("", label="log events 目录的绝对路径", info="TensorBoard 的 Log Events 的绝对路径，注意是指定的是目录不是文件，另外最好是绝对路径。如果是相对路径，会以家目录做为相对位置。")
            other_boot_command = gr.Textbox("", label="其他启动项", info="一般留空即可。注意：不要自己指定 --port 或 --ip。")
            self.render_start_button([log_path, other_boot_command])
        return b

    def start(self, log_path, other_boot_command):
        with self.conda_activate(self.cfg.conda_env):
            self.execute_command(f"tensorboard --logdir={log_path} --bind_all --port {self.port} {other_boot_command}", daemon=True)
        self.app_started()


def main():
    return Tensorboard()