# Brailloku
Generate virtually unlimited amounts of braille sudoku puzzles in Braille Ready Format (BRF) and Portable Embosser Format (PEF)!

![Image Brailloku Braille BRF and PEF Sudoku Generator](https://github.com/LPBeaulieu/Braille-Sudoku-Brailloku/blob/main/Brailloku%20Braille%20%20BRF%20and%20PEF%20Sudoku%20Generator%20Thumbnail.jpg)
<h3 align="center">Brailloku</h3>
<div align="center">
  
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPLv3.0-brightgreen.svg)](https://github.com/LPBeaulieu/Braille-Sudoku-Brailloku/blob/main/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/LPBeaulieu/Braille-Sudoku-Brailloku)](https://github.com/LPBeaulieu/Braille-Sudoku-Brailloku)
[![GitHub issues](https://img.shields.io/github/issues/LPBeaulieu/Braille-Sudoku-Brailloku)](https://github.com/LPBeaulieu/Braille-Sudoku-Brailloku)

</div>

---

<p align="left"> <b>Brailloku</b> is an app that generates virtually unlimited amounts of braille sudoku puzzles in Braille Ready Format (BRF) and Portable Embosser Format (PEF)!</p>
<p align="left"> You can also <b>select the number of empty cells</b> in your puzzle (up to 46 inclusively) and the <b>number of puzzles</b> that you want it to create for you! 
     <br> 
     
![Image Brailloku In Action](https://github.com/LPBeaulieu/Braille-Sudoku-Brailloku/blob/main/Brailloku%20In%20Action%20Snapshot.jpg)<hr>
<b>Figure 1</b>: The image above shows how you could play directly on embossed sudoku puzzles, with the help of braille-labelled magnetic push pins. 
I recommend laying a placemat over the metallic magnetic board in order to decrease the strength of the neodymium-based magnets, which could 
otherwise crush the braille dots. As I don't have access to a braille embosser, I typed my sudoku on my Perkins Brailler, but it should print 
very nicely in portrait mode on 8 1/2 by 11" braille or cardstock paper.<br><br>
</p>

## 📝 Table of Contents
- [Dependencies / Limitations](#limitations)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Author](#author)
- [Acknowledgments](#acknowledgments)

## ⛓️ Dependencies / Limitations <a name = "limitations"></a>
- The sudoku puzzles generated by <b>Brailloku</b> are created such that <b>there is always a way to fill an empty cell by direct logical deductions, without resorting to pencil marks or complicated tactics</b>. This is an important factor for sudoku puzzles in braille format, as the player cannot annotate the sudoku grid with pencil marks and moreover doesn't have a broad view of the playing grid, which is required for more complex puzzle solving techniques. 
- The point described above entails that there is a limit to the number of empty braille cells that can be included in any given sudoku puzzle while meeting these requirements. As such, a maximum of 46 empty braille cells can be selected by the player, and the time required to generate a puzzle can exceed 5 seconds at this setting. Generally though, the puzzles are created within 2 seconds.
- Each BRF and PEF document consists of two pages (a sudoku puzzle and its solution on the next page), both of which take up to a maximum of <b>30 columns per line</b> and span <b>22 lines per page, inclusively</b>. These settings will help you set up the embosser so that you obtain optimal results when embossing the files on 8 1/2 by 11" braille paper or cardstock in portrait mode.

## 🏁 Getting Started <a name = "getting_started"></a>

The following instructions will be provided in great detail, as they are intended for a broad audience and will
allow to run a copy of <b>Brailloku</b> on a local computer. Here is a link to an instructional video explaining the steps described below: https://www.youtube.com/watch?v=cT8XWUTPtxw.

The paths included in the code are formatted for Unix (Linux) operating systems (OS), so the following instructions 
are for Linux OS environments.

<b>Step 1</b>- Head over to the main <b>Brailloku</b> github page, click on the <b>Code</b> button and then click on the <b>Download zip</b> button.
Extract the zipped folder into your desired location, and the "Braille-Sudoku-Brailloku-main" folder will now serve as your working folder, which contains the Python code you will later run in order to generate sudoku puzzles.   

![Download Code Screenshot](https://github.com/LPBeaulieu/Braille-Sudoku-Brailloku/blob/main/Download%20Code%20Screenshot.jpg)<hr>
<b>Figure 2</b>:The image above shows the steps to take in order to download the compressed folder containing the code.<br><br>

<b>Step 2</b>- In order to set up <b>Brailloku</b> on your computer, access your working folder in the file explorer, and click on the folder’s arrow in the window’s header. Then, simply click on "open in terminal" in order to open a windowed command line, with a correct path to your working folder, as shown in Figure 3.

![Open in Terminal Screenshot](https://github.com/LPBeaulieu/Braille-Sudoku-Brailloku/blob/main/Open%20in%20Terminal%20Screenshot.jpg)<hr>
<b>Figure 3</b>: The image above shows the steps to take in order to open the command line in your working folder.<br><br>

 Copy and paste (or write down) the following in the command line to install <b>alive-Progress</b> (Python module for a progress bar displayed in command line): 
```
pip install alive-progress
```

<b>Step 3</b>- You're now ready to use <b>Brailloku</b>! 🎉


## 🎈 Usage <a name="usage"></a>

To run the "brailloku.py" code, open a windowed command line in your working folder as shown in Figure 2 and enter the following: 
```
python3 brailloku.py
```

<b>Brailloku</b> by default generates sudoku puzzles with a number of empty cells between 26 and 46, inclusively. You can also manually select the number of empty braille cells to include in the puzzle (up to a maximum of 46, inclusively) by typing "e" for empty cells, followed by the desired number. For example, if you would like to have 35 empty cells in your sudoku puzzle, you would enter the following in command line:
```
python3 brailloku.py e35
```

Furthermore, you can have <b>Brailloku</b> generate multiple braille sudoku files (each containing one sudoku and its solution on the following page) which are numbered for easy reference, by typing "n" for number of puzzles, followed by the desired number. Please note that in some cases, a puzzle can take more than 5 seconds to generate, as there is a lot of computation being done to ensure that the puzzle will be solvable without resorting to pencil marks or complex tactics. For example, if you would like to generate 50 sudoku puzzles, you would enter the following in command line:
```
python3 brailloku.py n50
```

Finally, you can specify both the difficulty level and the number of puzzles to generate. Simply enter both arguments mentioned above in any order, after the Python code call. Please make sure to include a space in-between the Python code file name and any additional arguments. For example, to generate 50 sudoku puzzles each having 35 empty cells, you would enter the following in command line:
```
python3 brailloku.py n50 e35
```

The alternative order of the arguments after the Python code file name would be treated the same way by the code (50 puzzles generated, each having 35 empty sudoku cells):

```
python3 brailloku.py e35 n50
```

<b>Brailloku</b> automatically creates a folder named "Brailloku Sudoku Puzzles" within your working folder. It then generates the "Braille Ready Format (BRF)" and "Portable Embosser Format (PEF)" subfolders within the "Brailloku Sudoku Puzzles" folder, and stores the files there. It also uses the file numbers of the BRF or PEF files in the "Brailloku Sudoku Puzzles" subfolders in order to assign the new sudoku puzzle numbers, so it is important to leave the files in those folders and to avoid renaming them to ensure that the numbering remains accurate later on.

<br><b>And that's it!</b> You're now ready to solve as many braille sudoku puzzles as you like! If you are close to someone who is visually impaired and would like to help them find an accessible version of sudoku, or maybe if you are only sprucing up your braille reading skills in preparation for the Zombie Apocalypse (lol) then this app is for you! 🎉📖
  
  
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
