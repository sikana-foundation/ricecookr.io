# ricecookr.io
Integration of Sikana's content into Learning Equality's [Kolibri Studio](https://contentworkshop.learningequality.org/).

Using [Ricecooker](https://github.com/learningequality/ricecooker) framework.

### Sikana's data structure
For each language, you'll find the content organized as follow:

```
Category
`-- Program
    `-- Chapter
        `-- Video
```

This script intends to create a Sikana channel per language ("Sikana EN", "Sikana FR", ...)

### Installation instructions
For this, you will need to have `python3` and [`virtualenv`](https://virtualenv.pypa.io/en/stable/) installed on your machine (please read the manual to understand basically how it works).

In the directory containing the code, run following commands:

- `virtualenv -p python3 venv`
- `source venv/bin/activate`
- `pip3 install -r requirements.txt`
- Then, copy-paste `parameters.yml.dist` to `parameters.yml` and fill it with your credentials to Sikana's API and Kolibri token.

### How to use it
Each time you want to use the script, you have to ensure the `virtualenv` you previously created is activated (it appears in your prompt).
If not, run the command `source venv/bin/activate`.

Run the following command to build a channel for the language of your choice:

`python3 -m ricecooker uploadchannel "ricecookr.py" --publish --token=<YOUR_TOKEN_HERE> language_code=<YOUR_LANGUAGE_CODE_HERE>`
