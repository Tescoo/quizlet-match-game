![image](https://github.com/Tescoo/quizlet-match-game/assets/66729830/a1ae21ba-96e2-4b5c-ad52-f99a151368fc)# quizlet-match-game
Get top score in a Quizlet match game with this little script.

# How to use?

### MUST BE ON PC/LAPTOP (windows)!
### MUST HAVE PYTHON INSTALLED >= 3.8

1. Download this repository, run `pip install -r requirements.txt`, then open `main.py`

Running main.py will look like this:

![image](https://i.imgur.com/zPlbRTu.png)

3. Go to your quizlet set and in your browser, do `CTRL + SHIFT + I` (or just open devtools/inspect element) and go to the `Network` tab.

![image](https://i.imgur.com/v2Xi6S6.png)

3. Start a quizlet match game. The time taken to finish the game is completely irrelevant.

So there, you finished the game. You should see this:

![image](https://i.imgur.com/0lu6kNP.png)

4. Find the request that simply and ONLY says "highscores". It is shown below. DO NOT pick the other one.

![image](https://i.imgur.com/y1lp20Z.png)

(You can find "highscores" easier by searching "highscores" in the filter, top left. Doesn't matter tho.)

5. Copy the request as POWERSHELL!

![image](https://i.imgur.com/bVqEioo.png)

As soon as you copy, go back to the console window and it will look like this:

![image](https://i.imgur.com/KGkEM4f.png)

6. Enter the time you want. Lowest is around 0.5 before the time fails to set.

![image](https://i.imgur.com/9QwIYUT.png)

7. Press enter and it will show the podium for that set.

![image](https://i.imgur.com/YdjxgTW.png)

8. Done!

# Thanks

@rambletrick - Will be making this type of thing for other gamemodes.
