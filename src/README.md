# Name of the project
    Battleship - BRALUX

## Name of group members
    - Oliver Jack
    - Matheus Rezende
    - Mauricio Orenbuch Hendel
    - Lucas Fernandes Martins
    - Lara Colognese de Almeida

Installation and requirements
    python3
        Sub-libraries of python3:
            arcade
            pytest
            random

## Run instructions

    1. Clone repository
    
    2. Install arcade & pytest if not already installed:
        - pip install arcade
        - pip install pytest

    2. Cd to src directory
    
    3. Run main.py file


## Description of the project
    Recreation of the battleship game, built with different difficulty levels which were implemented by ourselves

## Contribution recommendations:
    If you wish to contribute to this project please run the following command: 
    
    git clone git@gitlab-cw4.centralesupelec.fr:lucas.fernandes-martins/battleship.git
    
    All contributions are more than welcome, since our project is still a work in progress.


## Tutorial
    
    1.	To configure the initial setup of your grid, you will have to manually place 8 ships in total, 
    2 of sizes 2, 3, 4 and 1 of sizes 5, 7. 
    To place the boats you will always have to click the starting square, followed by its ending square. 
    You only have the option to place boats horizontally or vertically (not diagonally). 
    Please be aware that the ships are not allowed to overlap one another and are not allowed to partially leave the grid.
    

    2.	Once you have placed all 8 ships correctly, the fun can begin! 
    You will now take turns with the AI to shoot at each other’s grids. The user always gets to shoot first. 
    To shoot at the opponents grid, simply click on their grid (“Enemy Waters”). 
    After having shot at a certain square, its colour changes. 
    
    Here is the meaning of the different colours used in our game:
     * light blue: unshot square
     * dark blue: shot square with only water
     * light red: shot square where a ship has been hit
     * dark red: shot square where a ship has been sunk
    Please be aware that you can only shoot at every square once during the game.
    
    3.	The game ends once one of the players has been able to sink all their opponents ships successfully. 
    You then have the option to either play again (which we highly recommend) or close the game 
    by clicking on the “X” in the top right corner.
