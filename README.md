# Brailloku
Generate virtually unlimited amounts of braille sudoku puzzles in Portable Embosser Format (PEF)!

![Image RTF basic mode](https://github.com/LPBeaulieu/Braille-Sudoku-Brailloku/blob/main/Brailloku%20Thumbnail.jpg)
<h3 align="center">Brailloku</h3>
<div align="center">
  
  [![License: AGPL-3.0](https://img.shields.io/badge/License-AGPLv3.0-brightgreen.svg)]([https://github.com/LPBeaulieu/Brailloku](https://github.com/LPBeaulieu/Braille-Sudoku-Brailloku)/blob/main/LICENSE)
  [![GitHub last commit](https://img.shields.io/github/last-commit/LPBeaulieu/Brailloku)]([https://github.com/LPBeaulieu/Brailloku](https://github.com/LPBeaulieu/Braille-Sudoku-Brailloku))
  [![GitHub issues](https://img.shields.io/github/issues/LPBeaulieu/TintypeText)]([https://github.com/LPBeaulieu/Brailloku](https://github.com/LPBeaulieu/Braille-Sudoku-Brailloku))
  
</div>

---

<p align="left"> <b>Brailloku</b> is a app that generates virtually unlimited braille sudoku puzzle Portable Embosser Format (PEF) files!</p>
<p align="left"> You can also <b>select the number of empty cells</b> in your puzzle (up to 46 inclusively) and the <b>number of puzzles</b> you want it to create!
     <br> 
</p>

## 📝 Table of Contents
- [Dependencies / Limitations](#limitations)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Author](#author)
- [Acknowledgments](#acknowledgments)

## ⛓️ Dependencies / Limitations <a name = "limitations"></a>
- The sudoku puzzles generated by Brailloku are created such that <b>there is always a way to fill an empty cell by direct logical deductions, without resorting to pencil marks or complicated tactics</b>. This is an important factor for sudoku puzzles in braille format, as the player cannot annotate the sudoku grid with pencil marks and moreover doesn't have a broad view of the playing grid, which is required for more complex puzzle solving techniques. 
- The point described above entails that there is a limit to the number of empty braille cells that can be included in any given sudoku puzzle while meeting these requirements. As such, a maximum of 46 empty braille cells can be selected by the player, and the time required to generate a puzzle can exceed 5 seconds at this setting. Generally though, the puzzles are created within 2 seconds.


## 🏁 Getting Started <a name = "getting_started"></a>

The following instructions will be provided in great detail, as they are intended for a broad audience and will
allow to run a copy of <b>Brailloku</b> on a local computer. Here is a link to an instructional video explaining the steps 1 through 8 described below: **The link will be included here once the Youtube video is posted**.

The paths included in the code are formatted for Unix (Linux) operating systems (OS), so the following instructions 
are for Linux OS environments.

<b>Step 1</b>- Head over to the main Brailloku github page, click on the <b>Code</b> button and then click on the <b>Download zip</b> button.
Extract the zipped folder into your desired location, and the "Braille-Sudoku-Brailloku-main" folder will now serve as your working folder, which contains the Python code you will later run in order to generate sudoku puzzles.   

![Download Coode Screenshot](https://github.com/LPBeaulieu/Braille-Sudoku-Brailloku/blob/main/Download%20Code%20Screenshot.jpg)<hr>
The image above shows the steps to take in order to download the compressed folder containing the code.

<b>Step 2</b>- In order to set up Brailloku on your computer, access your working folder in the file explorer, and click on the folder’s arrow in the window’s header. Then, simply click on "open in terminal" in order to open a windowed command line, with a correct path to your working folder. Copy and paste (or write down) the following in the command line to install <b>alive-Progress</b> (Python module for progress bar displayed in command line): 
```
pip install alive-progress
```

<b>Step 3</b>- You're now ready to use <b>Brailloku</b>! 🎉


## 🎈 Usage <a name="usage"></a>

In order to set up Brailloku on your computer, create a working folder, access it in the file explorer, and click on the folder’s arrow in the window’s header. Then, simply click on "open in terminal" in order to open a windowed command line, with a correct path to your working folder.
Then copy and paste (or type in) the following in the command line: 
```
python3 brailloku.py
```

You might need to <b>alter the values</b> of the variables "<b>character_width</b>" (default value of 55 pixels for 8 1/2" x 11" typewritten pages 
scanned at a resolution of 600 dpi) and "<b>spacer_between_characters</b>" (default value of 5 pixels), as your typewriter may have a different typeset than those of my typewriters (those two default parameters were suitable for both my <i>2021 Royal Epoch</i> and <i>1968 Olivetti Underwood Lettera 33</i> typewriters). Also, if your typewriter has a lot of ghosting (faint outline of the preceding character) or if the signal to noise ratio is elevated (because of high ink loading on the ribbon leading to lots of ink speckling on the page), the segmentation code might pick up the ghosting or noise as characters. As a result, you could then end up with staggered character rectangles. In the presence of dark typewritten text you should decrease the segmentation sensitivity (increase the number of non-white y pixels required for a given x coordinate in order for that x coordinate to be included in the segmentation). That is to say that on a fresh ribbon of ink, you should increase the value of 3 (illustrated below) to about 6 (results will vary based on your typewriter's signal to noise ratio) in the line 57 of "get_predictions.py" in order to avoid including unwanted noise in the character rectangles. 
```
x_pixels = np.where(line_image >= 3)[0] 
```
When your typewritten text gets fainter, change that digit back to 3 to make the segmentation more sensitive (to avoid omitting characters). These parameters ("character_width", "spacer_between_characters" and "line_image >= 3" should be adjusted in the same way in all the Python code files (except "train_model.py", where they are absent) to ensure consistent segmentation in all steps of the process.

![Image txt file processing](https://github.com/LPBeaulieu/TintypeText/blob/main/txt%20file%20example.jpg)<hr>
The image above illustrates the format of the ".txt" file listing all of the character rectangle labels. In the first line, you can note that four of the characters are labeled as "@", which maps to the category "to be deleted". The three letters (C, X and I) have significant ink splattering and will not be included in the training data, as they are not representative of these characters. The fourth "@" on the first line corresponds to an artifact (some noise was above the filtering threshold and was picked up as a character). We also do not want to include it in the training data. The "lesser than" symbol highlighted in yellow on line 11 in the ".txt" file corresponds to an "empty" rectangle, which is mapped to the "space" category in the "Dataset" folder. The very last line of the typewriter scan image contains two typos (two characters overlaid with a hashtag symbol). They are represented by a "~" symbol in the ".txt" file on line 19. All the other character rectangles are represented by their own characters in the ".txt" file. 
<br><br>
Importantly, <b>such ".txt" files should be created, modified and saved exclusively in basic text editors</b> (such as Text Editor in Ubuntu 20.04), as more elaborate word processors would include extra formatting information that would interfere with the correct mapping of the character rectangles to their labels in the ".txt" file.

<b>Furthermore, the ".txt" files in the "Training&Validation Data" folder must have identical names to their corresponding JPEG images (minus the file extensions).</b> For example, the file "my_text.txt" would contain the labels corresponding to the raw scanned typewritten page JPEG image (without the character rectangles) named "my_text.jpg". The presence of hyphens in the file name is only necessary for JPEG files intended for OCR predictions (see below, file 4 "get_predictions.py"), although you could include some hyphens in every file name just as well.

<br>
 <b>File 2: "create_dataset.py"</b>- This code will crop the individual characters in the same way as the "create_rectangles.py" code,
 and will then open the ".txt" file containing the labels in order to create the dataset. Each character image will be sorted in its
 label subfolder within the "Dataset" folder, which is created automatically by the code. <br><br>
 A good practice <b>when creating a dataset</b> is to make the ".txt" file and then run the "create_dataset.py" code <b>one page at a time</b> (only one JPEG image and its corresponding ".txt" file at a time in the "Training&Validation Data" folder) to validate that the labels in the ".txt" file line up with the character rectangles on the typewritten text image. Such a validation step involves opening every "Dataset" subfolder and ensuring that every image corresponds to its subfolder label (pro tip: select the icon display option in the folder in order to display the image thumbnails, which makes the validation a whole lot quicker). You will need to delete the "Dataset" folder in between every page, otherwise it will add the labels to the existing ones within the subfolders. This makes it more manageable to correct any mistakes in the writing of the ".txt" files. Of note, some of the spaces are picked up as characters and framed with rectangles. You need to label those spaces with a lesser-than sign ("<"). Here is the list of symbols present in the ".txt" files mapping to the different characters rectangles:
  
  - <b>"<"</b>: "blank" character rectangle, which corresponds to a space. These character images are stored in the "space" subfolder within the "Dataset" folder.
  - <b>"~"</b>: "typo" character rectangle (any character overlaid with "#"). These character images are stored in the "empty" subfolder within the "Dataset" folder. 
  - <b>"@"</b>: "to be deleted" character rectangle (any undesired artifact or typo that wasn't picked up while typing on the typewriter). The 
    "to be deleted" subfolder (within the "Dataset" folder) and all its contents is automatically deleted and the characters labeled with "@" in the ".txt" file will be absent
    from the dataset, to avoid training on this erroneous data.
  - All the other characters in the ".txt" files are the same as those that you typed on your typewriter. The character images are stored in subfolders within the "Dataset" folder bearing the character's name (e.g. "a" character images are stored in the subfolder named "a").
 
  <b>Once you're done validating</b> the individual ".txt" files, you can delete the "Dataset" folder once more, add <b>all of the ".txt" files along with their corresponding JPEG images</b> to the "Training&Validation Data" folder and run the "create_dataset.py" code to get your complete dataset! 
  
![Image folder tree structure](https://github.com/LPBeaulieu/Braille-Sudoku-Brailloku/blob/main/Download%20Code%20Screenshot.svg)<hr>
The image above shows the folder tree structure of your working folder (above), along with the label subfolders within the "Dataset" folder (below).
 
  <br><b>File 3: "train_model.py"</b>- This code will train a convoluted neural network deep learning model from the labeled character images 
  within the "Dataset" folder. It will also provide you with the accuracy of the model in making OCR predictions, which will be displayed
  in the command line for every epoch (run through the entire dataset). The default hypeparameters (number of epochs=3, batch size=64, 
  learning rate=0.005, kernel size=5) were optimal and consistently gave OCR accuracies above 99.8%, provided a good-sized dataset is used (above 25,000 characters).  
  In my experience with this project, varying the value of any hyperparameter other than the kernel size did not lead to significant variations in accuracy.
  As this is a simple deep learning task, the accuracy relies more heavily on having good quality segmentation and character images that 
  accurately reflect those that would be found in text. Ideally, some characters would be typed with a fresh typewriter ribbon and others with an old one,
  to yield character images of varying boldness, once again reflecting the irregularities normally observed when using a typewriter.
  
  When you obtain a model with good accuracy, you should rename it and do a backup of it along with the "Dataset" folder on which it was trained.
  If you do change the name of the model file, you also need to update its name in the line 174 of "get_predictions.py":
  ```
  learn = load_learner(cwd + '/your_model_name')
  ```
  <br><b>File 4: "get_predictions.py"</b>- This code will perform OCR on JPEG images of scanned typewritten text (at a resolution of 600 dpi)
  that you will place in the folder "OCR Raw Data". 
  
  <b>Please note that all of the JPEG file names in the "OCR Raw Data" folder must contain at least one hyphen ("-") in order for the code
  to properly create subfolders in the "OCR Predictions" folder. These subfolders will contain the rich text format (RTF) OCR conversion documents.</b> 
  
  The reason for this is that when you will scan a multi-page document in a multi-page scanner, you will provide your scanner with a file root name (e.g. "my_text-") and the scanner will number them automatically (e.g."my_text-.jpg", "my_text-0001.jpg", "my_text-0002.jpg", "my_text-"0003.jpg", etc.) and the code would then label the subfolder within the "OCR Predictions" folder as "my_text". The OCR prediction results for each page will be added in sequence to the "my_text.rtf" file within the "my_text" subfolder of the "OCR Predictions" folder. Should you ever want to repeat the OCR prediction for a set of JPEG images, it would then be important to remove the "my_text" subfolder before running the "get_predictions.py" code once more, in order to avoid appending more text to the existing "my_text.rtf" file.

If you changed the name of your deep learning model, or if you are using one of the models that I trained, you will to update the model name within the "get_predictions.py" code. That is to say that you will need to change "typewriter_OCR_cnn_model" for the name of your model in line 174 of "get_predictions.py":
               
```              
learn = load_learner(cwd + '/typewriter_OCR_cnn_model')
```
               
As mentioned above, since fresh typewriter ink ribbons lead to darker text and more ink speckling on the page, in the presence of dark typewritten text you should decrease the segmentation sensitivity (increase the number of non-white y pixels required for a given x coordinate in order for that x coordinate to be included in the segmentation). That is to say that on a fresh ribbon of ink, you should increase the value of 3 (illustrated below) to about 6 (results will vary based on your typewriter's signal to noise ratio) in the line 56 of "get_predictions.py" in order to avoid including unwanted noise in the character rectangles. 
```
x_pixels = np.where(line_image >= 3)[0] 
```
When your typewritten text gets fainter, change that digit back to 3 to make the segmentation more sensitive (to avoid omitting characters).

        
  <br><b>And that's it!</b> You're now ready to convert your typewritten manuscript into digital format! You can now type away at the cottage or in the park without worrying about your laptop's battery life 
  and still get your document polished up in digital form in the end! 🎉📖
  
  
## ✍️ Authors <a name = "author"></a>
- 👋 Hi, I’m Louis-Philippe!
- 👀 I’m interested in natural language processing (NLP) and anything to do with words, really! 📝
- 🌱 I’m currently reading about deep learning (and reviewing the underlying math involved in coding such applications 🧮😕)
- 📫 How to reach me: By e-mail! LPBeaulieu@gmail.com 💻


## 🎉 Acknowledgments <a name = "acknowledgments"></a>
- Hat tip to [@kylelobo](https://github.com/kylelobo) for the GitHub README template!




<!---
LPBeaulieu/LPBeaulieu is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
