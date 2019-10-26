# Colorado Yeti Sim Tester

*by infinitempg*

This is the proprietary technology of the Colorado Yeti. Any unauthorized redistribution will be punished by the full extent of the law. Which is none at all.

## Quick Setup

1. Install Anaconda for Python 3.7 from [here](https://www.anaconda.com/distribution/).
2. Install DDSPF16.
3. Install an autoclicker of your choice (iseedoug has a good one [here](https://github.com/BenjaminDHorne/QuickKetchup)).
4. Download this repository to your computer and un-zip it if necessary.
5. ???
6. Profit.

How to use this will be detailed below.

## Detailed Setup

For this program to work you will need to install Anaconda (which should include an installation of Python3 and JupyterLab) and DDSPF16 (obviously). You will also need an auto-clicker.

I currently run this setup on a Windows 10 computer but using an Ubuntu bash kernel, but I'm writing these up for a standard Windows user. These instructions should also work just fine for a Mac user (though running DDSPF may be problematic for you).

### Installing Programs

A download for Anaconda can be found [here](https://www.anaconda.com/distribution/) - make sure you download the one for **Python 3.7**. This is a very big download, but if you ever want to do data science it'll have a ton of stuff :) For this program, I use `numpy`, `matplotlib`, `astropy`, and iPython widgets. (Arguably I could have used `pandas` instead of `astropy` but look I work in astronomy okay?)

For the auto-clicker, I personally hand-wrote a program in AutoHotkey, but I would recommend using iseedoug's auto-clicker (found [here](https://github.com/BenjaminDHorne/QuickKetchup)) as it's much easier to use.

I'm not going to tell you how to install DDSPF16 since it's technically illegal to now, so ask your GM :)

### Installing the Tester

Download this repository as a ZIP file (or git clone it, I'm not the police) and un-zip it if necessary to a proper directory in your filesystem. This is going to be your home-base for all testing.

## How to Use

### DDSPF16

iseedoug's write up on this is excellent, so I would suggest reading it [here](https://drive.google.com/file/d/14ZK78CGq_u7MXkGcFk3yPef3ChiOOOyF/view). But if you want my take on things...

First things first, make sure to replace the `Plays.xml` file, as certain plays such as CB Blitz have been outlawed. You will need to go to where your program is installed (most likely `C:\Program Files (x86)\Wolverine Studios\Draft Day Sports - Pro Football 2016\`) and paste the new file into the `Data` folder.

Load up DDSPF16 and open up your save file. I would recommend immediately saving it as a different file name to protect the integrity of your original file. You can then go into your team's page and edit things like the Strategy or Depth Charts (make sure to check with your local simmer to see what the sim rules are). Make sure to save after making changes!

Now we can actually run our tests. Go into `Tasks -> Sim Exhibition Game` and set your home and away teams as appropriate. Now you can use your auto-clicker of choice (see iseedoug's manual for how to set his up) and sim anywhere between 200-300 games, as that is when results begin to become reliable (see this [graph](https://cdn.discordapp.com/attachments/519595778239365120/558162217514696704/vAQAAAAAchMoeAAAAADgQYQ8AAAAAHIiwBwAAAAAORNgDAAAAAAci7AEAAACAAxH2AAAAAMCBCHsAAAAA4ECEPQAAAABwoP8BTx6.png)). Don't do too many though, as DDSPF has a fun memory leak issue and running anything more than 300 or so will cause the app to crash mid click.

Once the tests are done, go to `Configuration` and check `Enable Personalities`. Do not enable personalities before simming the exhibitions as it breaks things! Now you can go to `Export -> Generate Access and CSV Files` and export it. **Important:** Do NOT save this file afterwards - it will save the previous exhibition matches and skew your data.

Now that everything is exported, go to `Documents/DDSPF/Leagues` and copy the entire save file folder to the directory (or a subdirectory of) the folder where the tester is saved.

### JupyterLab

So in order to analyze these tests, we need to load up the tester, which is a JupyterLab Notebook (`simTester.ipynb`). If you installed it with the standard Windows installation, you should be able to search your programs for JupyterLab or Jupyter Notebook. I will be using the example of JupyterLab.

When you first open this up, you should be treated to a screen similar (but probably white) to this one:

![](/readme_images/jupyter_lab.png)

Use the sidebar on the left to navigate to the directory containing the file `simTester.ipynb` and then open it. Make sure that the file `simFns.py` is in the same directory as well, as it won't work with out it.

There are instructions in the file itself, but you can almost certainly get away with running `Kernel -> Restart and Run All Cells` and using the dropdowns provided in the widgets. Please read the instructions provided in the Jupyter notebook itself as they should be able to guide you from here on out.

Here's an example result of the tester:

![](/readme_images/sample_output.png)

## Final Thoughts

I think this tester should make a lot of lives much easier, as not only do you get visual graphs of your results but you can also easily and visually compare two different strategies/depth charts. It's important for testers to realize that any win percentage within 2% can be ruled out due to noise, so do not get overly stressed to increase your win percentage from 60% to 62%. Also make sure to remember that just because you tested an 80% win rate does not mean the game is a win - 20% of those exhibitions you lost! Do not get too hung up on your sim tests, as they only provide you with *likely* results rather than actual ones.

Have fun with this tester! Hopefully it helps out.
