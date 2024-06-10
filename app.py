import gradio as gr
import subprocess
import shutil
import os

def unzip(filename):
    shutil.unpack_archive(filename, extract_dir="extracted")

def zip_folder(folder):
    shutil.make_archive("dist", 'zip', folder)

def build_project(os_dropdown, project_name, description, product_name, org_name, company_name, copyright, 
                  splash_color, splash_dark_color, no_web_splash, no_ios_splash, no_android_splash,
                  team_id, base_url, web_renderer, use_color_emoji, route_url_strategy, 
                  flutter_build_args, include_packages, build_number, build_version, 
                  module_name, template, template_dir, template_ref):
    
    dir_name = os.listdir("extracted")[0]

    if os_dropdown:
        command = ["flet", "build", os_dropdown, f"extracted/{dir_name}"]
    else:
        raise KeyError("Please choose operating system to compile.")
    if project_name:
        command.extend(["--project", project_name])
    if description:
        command.extend(["--description", description])
    if product_name:
        command.extend(["--product", product_name])
    if org_name:
        command.extend(["--org", org_name])
    if company_name:
        command.extend(["--company", company_name])
    if copyright:
        command.extend(["--copyright", copyright])
    if splash_color:
        command.extend(["--splash-color", splash_color])
    if splash_dark_color:
        command.extend(["--splash-dark-color", splash_dark_color])
    if no_web_splash:
        command.append("--no-web-splash")
    if no_ios_splash:
        command.append("--no-ios-splash")
    if no_android_splash:
        command.append("--no-android-splash")
    if team_id:
        command.extend(["--team", team_id])
    if base_url:
        command.extend(["--base-url", base_url])
    if web_renderer:
        command.extend(["--web-renderer", web_renderer])
    if use_color_emoji:
        command.append("--use-color-emoji")
    if route_url_strategy:
        command.extend(["--route-url-strategy", route_url_strategy])
    if flutter_build_args:
        command.extend(["--flutter-build-args"] + flutter_build_args.split())
    if include_packages:
        command.extend(["--include-packages"] + include_packages.split())
    if build_number:
        command.extend(["--build-number", build_number])
    if build_version:
        command.extend(["--build-version", build_version])
    if module_name:
        command.extend(["--module-name", module_name])
    if template:
        command.extend(["--template", template])
    if template_dir:
        command.extend(["--template-dir", template_dir])
    if template_ref:
        command.extend(["--template-ref", template_ref])

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        zip_folder(f"extracted/{dir_name}/dist/{os_dropdown.lower()}")
        return result.stdout, "dist.zip"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}", None

# Define the GUI layout
with gr.Blocks() as demo:
    with gr.Column():
        gr.Markdown("# FletBuild")

        def process_file(file):
            # file is a tempfile.NamedTemporaryFile object
            file_path = file.name
            unzip(filename=file_path)
        
        with gr.Row():
            file_input = gr.File(type="filepath", label="App File", file_types=[".zip", ".tar"])
            file_input.upload(process_file, inputs=file_input, outputs=[])

        with gr.Row():
            with gr.Column():
                gr.Markdown("## Operating System")
                os_dropdown = gr.Dropdown(
                    choices=["LINUX", "WEB", "APK", "AAB"],
                    label="OPTIONS"
                )

                gr.Markdown("## Infos")
                project_name = gr.Textbox(label="Project Name", info="Project name for executable or bundle")
                description = gr.Textbox(label="Description", info="The description to use for executable or bundle")
                product_name = gr.Textbox(label="Product Name", info="Project display name that is shown in window titles and about app dialogs")
                org_name = gr.Textbox(label="Organization Name", info="Org name in reverse domain name notation, e.g. 'com.mycompany' - combined with project name and used as an iOS and Android bundle ID")
                company_name = gr.Textbox(label="Company Name", info="Company name to display in about app dialogs")
                copyright = gr.Textbox(label="Copyright", info="Copyright text to display in about app dialogs")
                splash_color = gr.Textbox(label="Splash Color", info="Background color of app splash screen on iOS, Android and web")
                splash_dark_color = gr.Textbox(label="Splash Dark Color", info="Background color in dark mode of app splash screen on iOS, Android and web")
                no_web_splash = gr.Checkbox(label="Disable Web Splash", info="Disable web app splash screen")
                no_ios_splash = gr.Checkbox(label="Disable iOS Splash", info="Disable iOS app splash screen")
                no_android_splash = gr.Checkbox(label="Disable Android Splash", info="Disable Android app splash screen")
                team_id = gr.Textbox(label="Team ID", info="Team ID to sign iOS bundle (ipa only)")
                base_url = gr.Textbox(label="Base URL", info="Base URL for the app (web only)")
                web_renderer = gr.Dropdown(choices=["canvaskit", "html"], label="Web Renderer", info="Renderer to use (web only)")
                use_color_emoji = gr.Checkbox(label="Use Color Emoji", info="Enables color emojis with CanvasKit renderer (web only)")
                route_url_strategy = gr.Dropdown(choices=["path", "hash"], label="Route URL Strategy", info="URL routing strategy (web only)")
                flutter_build_args = gr.Textbox(label="Flutter Build Args", info="Additional arguments for flutter build command")
                include_packages = gr.Textbox(label="Include Packages", info="Include extra Flutter Flet packages, such as flet_video, flet_audio, etc.")
                build_number = gr.Textbox(label="Build Number", info="Build number - an identifier used as an internal version number")
                build_version = gr.Textbox(label="Build Version", info="Build version - a 'x.y.z' string used as the version number shown to users")
                module_name = gr.Textbox(label="Module Name", info="Python module name with an app entry point")
                template = gr.Textbox(label="Template", info="A directory containing Flutter bootstrap template, or a URL to a git repository template")
                template_dir = gr.Textbox(label="Template Directory", info="Relative path to a Flutter bootstrap template in a repository")
                template_ref = gr.Textbox(label="Template Reference", info="The branch, tag or commit ID to checkout after cloning the repository with Flutter bootstrap template")
                
        build_button = gr.Button("Build")
        
        build_output = gr.Textbox(label="Build Output")
        download_link = gr.File(label="Download ZIP")

        def build_and_get_zip(*args):
            build_output, zip_path = build_project(*args)
            return build_output, zip_path if zip_path else None

        build_button.click(
            build_and_get_zip,
            inputs=[
                os_dropdown, project_name, description, product_name, org_name, company_name, copyright, 
                splash_color, splash_dark_color, no_web_splash, no_ios_splash, no_android_splash,
                team_id, base_url, web_renderer, use_color_emoji, route_url_strategy, 
                flutter_build_args, include_packages, build_number, build_version, 
                module_name, template, template_dir, template_ref
            ],
            outputs=[build_output, download_link]
        )

# Launch the Gradio app
demo.launch()
