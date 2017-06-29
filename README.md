# ricecookr.io
Integration of Sikana's content into Learning Equality's [Kolibri Studio](https://contentworkshop.learningequality.org/).

Using [Ricecooker](https://github.com/learningequality/ricecooker) framework.

### Kolibri's data structure
```
Node
`-- TreeNode
    |-- TopicNode
    `-- ContentNode
        |-- VideoNode
        |-- DocumentNode
        `-- ...

File
|-- DownloadFile
|   |-- VideoFile
|   `-- SubtitleFile
|-- WebVideoFile
|   `-- YouTubeVideoFile
|-- YouTubeSubtitleFile
`-- ...
```

### Sikana's data structure
```
Language
`--Category
    `-- Program
        `-- Chapter
            `-- Video
```

This script intends to create a Sikana channel per language ("Sikana EN", "Sikana FR", ...)

### How to use it
First, copy-paste `parameters.yml.dist` to `parameters.yml` and fill it with your credentials to Sikana's API and Kolibri token.

Then, run the following command to build a channel for the language of your choice:

`python3 -m ricecooker uploadchannel "ricecookr.py" --publish --token=<YOUR_TOKEN_HERE> language_code=<YOUR_LANGUAGE_CODE_HERE>`
