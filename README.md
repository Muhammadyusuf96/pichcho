## Pichcho
Pichcho is a Python entertainment program that records audio from your microphone, detects when you stop talking, and then pitches the recorded audio and plays it back to you using the `librosa` (optional, not tested yet) or `pydub`, `pyaudio`, `numpy`, `soundfile` library.

## Similar software
- Talking Tom Cat
- Talking Angela
- Dancing Cactus Toy

## Installation
Clone the repository or download the source code.
Install the required dependencies by running `pip install -r requirements.txt`.

## Usage
To use Pichcho, simply run the main.py script. The program will record audio from your microphone and automatically pitch shift the audio if there is a period of silence lasting more than 0.3 seconds and a total recording duration of more than 0.6 seconds.

You can adjust the pitch shift amount by changing the `octaves` variable in the main.py script. The default value is about half an octave.

## Contributing
If you find any issues with the program or have any suggestions for improvement, please feel free to open an issue or submit a pull request on GitHub.

## License
This program is licensed under the LGPLv3 License. See the LICENSE file for more information.
