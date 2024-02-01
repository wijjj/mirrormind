# Mirrormind Coach

Mirrormind Coach is a basic offline chat client designed to interact with a large language model via the `ollama` famework. It is built using the Kivy framework, providing a graphical user interface for engaging with language models in an interactive way.

## Description

Mirrormind Coach allows users to select and interact with various language models provided by the `ollama` service. This initial test version offers a user-friendly interface for sending queries and receiving responses from the chosen language model.

## Features

- Dynamic model selection through a drop-down menu, populated from the `ollama` service.
- An input field for sending text prompts to the selected language model.
- A display area for viewing the conversation history.
- Basic control elements like "topics" and "settings" buttons (with further functionalities planned for future updates).

## Warning

Please note that Mirrormind Coach is currently in its initial test phase. This version lacks comprehensive safety features and error handling, and is intended primarily for development and experimental use. Users should be aware of its limitations and exercise caution.

## Installation

To set up Mirrormind Coach, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the cloned directory.
3. Run the following command to install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

## Usage

Instructions on how to use Mirrormind Coach will be added in upcoming updates.

## Todo

- [ ] First check if there are any ollama models available at all!
- [ ] Async output
- [ ] Settings like parameters (temperature and so on)
- [ ] and so much more about the actual core logic of a coach, like
- [ ] RAG to store progress of coaching sessions



## License

Mirrormind Coach is licensed under the GNU General Public License (GPL). See the `LICENSE` file for more details.

## Acknowledgments

- Thanks to the Ollama team for the language model framework!
- Kudos to the developers of the Kivy framework for their incredible work in facilitating cross-platform application development.

Stay tuned for further developments and enhancements of Mirrormind Coach!

