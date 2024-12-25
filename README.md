# Bulk Renamer
A small python script to rename files in a directory in bulk.

## Usage

Get the latest release as an executable from the [releases page](https://github.com/appleplectic/BulkRenamer/releases).

Note that antivirus software may flag the executable as a false positive.

### Running from Source
1. Clone the repository
2. Setup the environment.
```bash
# Optionally, you can create a virtual environment
python3 -m venv .venv
pip install -r requirements.txt
```
3. Run the script.
```bash
python3 main.py
```

### Build Executable
You can build an executable using `pyinstaller` with the build script.
```bash
./build.sh
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Icons from Iconduck: [https://iconduck.com/icons/68113/rename](https://iconduck.com/icons/68113/rename), licensed under the MIT License - see the [LICENSE-Iconduck](LICENSE-Iconduck) file for details.
