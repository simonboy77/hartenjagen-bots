from tkinter import *
from tkinter import ttk

class HandOfCards:
    cardWidth = 2

    def __init__(self, frame, maxCards):
        self.frame = frame
        self.maxCards = maxCards
        self.cardButtons = []

        for cardId in range(0, self.maxCards):
            #btnWidth = self.frame.width / self.maxCards
            btnCmd = lambda i=cardId: self.play_card(i)
            cardButton = ttk.Button(self.frame, text=str(cardId), command=btnCmd)
            self.cardButtons.append(cardButton)

        resetBtnCmd = lambda: self.reset_hand()
        self.resetButton = ttk.Button(self.frame, text="New Cards", command=resetBtnCmd)
        self.reset_hand()

    def show_cards(self):
        print("showing " + str(self.playedCards))
        numCards = self.playedCards.count(False)

        if numCards > 0:
            cardsShown = 0
            for cardId in range(0, numCards):
                if self.playedCards[cardId] is False:
                    columnNum = cardsShown * 2
                    self.cardButtons[cardId].grid(column=columnNum, row=1, columnspan=self.cardWidth)
                    cardsShown += 1
        else:
            self.resetButton.grid(column=0,row=0)

    def play_card(self, id):
        print("played " + str(id))

        self.playedCards[id] = True
        self.cardButtons[id].grid_forget()

        self.show_cards()

    def reset_hand(self):
        print("Reseting hand")

        self.playedCards = [False] * self.maxCards
        self.resetButton.grid_forget()

        self.show_cards()