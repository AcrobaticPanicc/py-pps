# py-pps

**py-pps** (short for "pretty-ps") is a simple command-line tool used as an alternative for the `docker ps` command

## Motives
As an everyday Docker user, the `docker ps` command output always annoyed me. 
The output is very wide and not very readable.
I wanted to have a better alternative to it, so I created py-pps.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install py-pps.

1. Use the following pip command to install py-pps
```bash
pip install --target="$HOME/pypps/" py-pps
```

2. Install the [Docker SDK](https://docker-py.readthedocs.io/en/stable/) for Python and [Rich](https://rich.readthedocs.io/)
```bash
pip install docker rich
```

3. Add py-pps to your PATH (replace `.zshrc` with your shell's configuration file)
```bash
echo "PATH=$PATH:~/pypps/bin" >> ~/.zshrc
```

## Usage

Simply run `pps` in your terminal:
![ezgif com-gif-maker (1)](https://user-images.githubusercontent.com/10364402/170822616-85a3b392-8b12-4670-9a49-70d384416f89.gif)

## CLI Usage
```
$ pps --help
usage: pps [-h] [-j] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -j, --json     Print the conatiners' data in JSON format.
  -v, --version  Print the binary version information.
```

## Roadmap
- [ ] Add tests
- [ ] Add additional functionality (such as filtering)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact
✉️ [chaim.tomer@gmail.com](mailto:lunde@adobe.com?subject=[GitHub]%20Source%20Han%20Sans)



## License
[MIT](https://choosealicense.com/licenses/mit/)

