from unittest import TestCase
import testUtility
import Dominion


class FakeCard(Dominion.Action_card):
    def __init__(self, name, cost, actions, cards, buys, coins):
        Dominion.Action_card.__init__(self, name, cost, actions, cards, buys, coins)


class TestCard(TestCase):

    def setUp(self):
        # Data setup
        # Get player names
        self.player_names = testUtility.getPlayerNames()

        # number of curses and victory cards
        self.nV = testUtility.getNumberOfVictoryCards(self.player_names)
        self.nC = testUtility.getNumberOfCurseCards(self.player_names)

        # Define box
        self.box = testUtility.getBoxes(self.nV)

        self.supply_order = testUtility.getSupplyOrder()

        # Pick 10 random cards from box to be in the supply, then add the cards that are included in every game.
        self.supply = testUtility.getSupplyCards(self.box, self.player_names, self.nV, self.nC)

        # initialize the trash
        self.trash = testUtility.initializeTrash()
        self.player = Dominion.Player('Annie')

    def test_init(self):
        # initialize test data
        self.setUp()
        cost = 1
        buypower = 5

        # instantiate the card object
        card = Dominion.Coin_card(self.player.name, cost, buypower)

        # verify that the class variables have the expected values
        self.assertEqual('Annie', card.name)
        self.assertEqual(buypower, card.buypower)
        self.assertEqual(cost, card.cost)
        self.assertEqual("coin", card.category)
        self.assertEqual(0, card.vpoints)

    def test_react(self):
        pass


class TestAction_card(TestCase):
    def setUp(self):
        # Data setup
        # Get player names
        self.player_names = testUtility.getPlayerNames()

        # number of curses and victory cards
        self.nV = testUtility.getNumberOfVictoryCards(self.player_names)
        self.nC = testUtility.getNumberOfCurseCards(self.player_names)

        # Define box
        self.box = testUtility.getBoxes(self.nV)

        self.supply_order = testUtility.getSupplyOrder()

        # Pick 10 random cards from box to be in the supply, then add the cards that are included in every game.
        self.supply = testUtility.getSupplyCards(self.box, self.player_names, self.nV, self.nC)

        # initialize the trash
        self.trash = testUtility.initializeTrash()

    def test_init(self):
        actionCard = Dominion.Woodcutter()

        self.assertEqual(actionCard.name, 'Woodcutter')
        self.assertEqual(actionCard.cost, 3)
        self.assertEqual(actionCard.actions, 0)
        self.assertEqual(actionCard.cards, 0)
        self.assertEqual(actionCard.buys, 1)
        self.assertEqual(actionCard.coins, 2)

        actionCard = Dominion.Village()

        self.assertEqual(actionCard.name, 'Village')
        self.assertEqual(actionCard.cost, 3)
        self.assertEqual(actionCard.actions, 2)
        self.assertEqual(actionCard.cards, 1)
        self.assertEqual(actionCard.buys, 0)
        self.assertEqual(actionCard.coins, 0)

        actionCard = FakeCard("TotallyFake", -100, -50, -100, -100, -100)

        self.assertEqual(actionCard.name, 'TotallyFake')
        self.assertEqual(actionCard.cost, -100)
        self.assertEqual(actionCard.actions, -50)
        self.assertEqual(actionCard.cards, -100)
        self.assertEqual(actionCard.buys, -100)
        self.assertEqual(actionCard.coins, -100)

    def test_use(self):
        # All startup information
        self.setUp()
        self.player = Dominion.Player('Annie')
        actionCard = Dominion.Woodcutter()

        # Add the woodcutter to Annie's hand
        self.player.hand.append(actionCard)

        self.assertNotIn(actionCard, self.player.played)
        self.assertIn(actionCard, self.player.hand, "Action card is not in the hand list.")

        actionCard.use(self.player, self.trash)

        self.assertIn(actionCard, self.player.played, "Action card was not in the played list, but it should be.")
        self.assertNotIn(actionCard, self.player.hand, "Action card was in the hand, but it should not be.")

    def test_augment(self):
        # self.setUp()
        self.player = Dominion.Player('Annie')

        # The player should only have 5 cards in their hand at the start.
        handSize = 5
        self.assertEqual(len(self.player.hand), handSize)

        # The player normally only has actions, buys, and purse attributes when the turn player function is called.
        # The following values are the values that a player is given to start a turn.
        startingActions = self.player.actions = 1
        startingBuys = self.player.buys = 1
        startingPurse = self.player.purse = 0

        actionCard = FakeCard('Fake', 1, 1, 1, 1, 1)
        actionCard.augment(self.player)

        self.assertEqual(actionCard.cards + handSize, len(self.player.hand))
        self.assertEqual(actionCard.actions + startingActions, self.player.actions)
        self.assertEqual(actionCard.buys + startingBuys, self.player.buys)
        self.assertEqual(actionCard.coins + startingPurse, self.player.purse)

        self.player = Dominion.Player("Tom")

        startingActions = self.player.actions = 1
        startingBuys = self.player.buys = 1
        startingPurse = self.player.purse = 0

        actionCard = FakeCard('Fake', -1, -1, -1, -1, -1)
        actionCard.augment(self.player)

        # The hand size shouldn't change in the case of negative numbers.
        self.assertEqual(handSize, len(self.player.hand))
        self.assertEqual(actionCard.actions + startingActions, self.player.actions)
        self.assertEqual(actionCard.buys + startingBuys, self.player.buys)
        self.assertEqual(actionCard.coins + startingPurse, self.player.purse)

        self.player = Dominion.Player("Pam")

        startingActions = self.player.actions = 1
        startingBuys = self.player.buys = 1
        startingPurse = self.player.purse = 0

        actionCard = FakeCard('Fake', 0, 0, 0, 0, 0)
        actionCard.augment(self.player)

        self.assertEqual(handSize, len(self.player.hand))
        self.assertEqual(actionCard.actions + startingActions, self.player.actions)
        self.assertEqual(actionCard.buys + startingBuys, self.player.buys)
        self.assertEqual(actionCard.coins + startingPurse, self.player.purse)


class TestPlayer(TestCase):

    def test_draw(self):
        self.player = Dominion.Player("Annie")

        # Clear the hand and deck completely
        self.player.hand = []
        self.player.deck = []

        # The draw condition should work on 1 card
        self.player.deck.append(Dominion.Estate())
        self.player.draw()

        # Our deck should now be empty, and our hand should have one card.
        self.assertEqual(len(self.player.deck), 0)
        self.assertEqual(len(self.player.hand), 1)

        # Drawing from an empty deck will cause the deck to be replaced with the discard pile.
        self.player.draw()

        # We didn't have a discard pile, so the deck should still be empty.
        self.assertEqual(len(self.player.deck), 0)

        self.player.discard.append(Dominion.Cellar())

        self.player.draw()

        # Now the deck and discard should have zero cards, but the hand should have 2 cards
        self.assertEqual(len(self.player.deck), 0)
        self.assertEqual(len(self.player.hand), 2)
        self.assertEqual(len(self.player.discard), 0)

    def test_action_balance(self):
        self.player = Dominion.Player("Annie")

        startingStackSize = len(self.player.stack())

        # No action cards should be in our stack at the start.
        self.assertEqual(self.player.action_balance(), 0)

        # Add an action card to the player's hand.
        actionCard = FakeCard("Fake", 1, 1, 1, 1, 1)
        self.player.hand.append(actionCard)

        # The balance will be equal to 0
        self.assertTrue(self.player.action_balance() == 0)

        # Removing the card should make the action balance go back to zero
        self.player.hand.remove(actionCard)
        self.assertEqual(self.player.action_balance(), 0)

        # LESS THAN ZERO TEST
        # Add an action card to the player's hand.
        actionCard = FakeCard("Fake", -1, -1, -1, -1, -1)
        self.player.hand.append(actionCard)

        # The balance will be equal to 0
        self.assertTrue(self.player.action_balance() < 0)

        # Removing the card should make the action balance go back to zero
        self.player.hand.remove(actionCard)
        self.assertEqual(self.player.action_balance(), 0)

        # GREAT THAN 1
        # Add an action card to the player's hand.
        actionCard = FakeCard("Fake", 2, 2, 2, 2, 2)
        self.player.hand.append(actionCard)

        # The balance will be equal to 0
        self.assertTrue(self.player.action_balance() > 0)

        # Removing the card should make the action balance go back to zero
        self.player.hand.remove(actionCard)
        self.assertEqual(self.player.action_balance(), 0)

    def test_cardsummary(self):
        self.player = Dominion.Player("Annie")

        # Clear the hand and deck completely
        self.player.hand = []
        self.player.deck = []

        # Deal with an empty summary
        summary = self.player.cardsummary()

        self.assertEqual(summary['VICTORY POINTS'], 0)

        card = Dominion.Woodcutter()
        self.player.hand.append(card)

        summary = self.player.cardsummary()

        # There's only one card inside the summary so far.
        self.assertEqual(len(summary), 2)
        self.assertIn(card.name, summary)

        self.player.hand.remove(card)

        summary = self.player.cardsummary()
        # Now the summary should only have the victory point entry again.
        self.assertNotIn(card.name, summary)

        newCard = Dominion.Cellar()
        self.player.hand.append(newCard)
        self.player.deck.append(card)

        summary = self.player.cardsummary()
        self.assertIn(card.name, summary)
        self.assertEqual(summary[card.name], 1)
        self.assertIn(newCard.name, summary)
        self.assertEqual(summary[newCard.name], 1)

        self.player.discard.append(card)

        summary = self.player.cardsummary()
        self.assertEqual(summary[card.name], 2)

    def test_calcpoints(self):
        self.player = Dominion.Player("Annie")

        # Clear the hand and deck completely
        self.player.hand = []
        self.player.deck = []

        self.assertEqual(self.player.calcpoints(), 0)
        # Estates are worth one point
        self.player.hand.append(Dominion.Estate())
        self.assertEqual(self.player.calcpoints(), 1)

        # Gardens count as a multiplier of points, but they are not relevant until you have at least 10 victory cards
        self.player.hand.append(Dominion.Gardens())
        self.assertEqual(self.player.calcpoints(), 1)

        # Add more gardens, to get to the boundary of 10 victory cards
        n = 0
        while n < 8:
            self.player.hand.append(Dominion.Gardens())
            n += 1

        # 1 point for the victory point + 1 point for (number of cards / 10) * 9 gardens = 10
        self.assertEqual(self.player.calcpoints(), 10)


class Test(TestCase):
    def setUp(self):
        # Data setup
        # Get player names
        self.player_names = testUtility.getPlayerNames()

        # number of curses and victory cards
        self.nV = testUtility.getNumberOfVictoryCards(self.player_names)
        self.nC = testUtility.getNumberOfCurseCards(self.player_names)

        # Define box
        self.box = testUtility.getBoxes(self.nV)

        self.supply_order = testUtility.getSupplyOrder()

        # Pick 10 random cards from box to be in the supply, then add the cards that are included in every game.
        self.supply = testUtility.getSupplyCards(self.box, self.player_names, self.nV, self.nC)

        # initialize the trash
        self.trash = testUtility.initializeTrash()

    def test_gameover(self):
        self.setUp()

        # Remove all provinces
        self.supply["Province"] = []

        theGameIsOver = Dominion.gameover(self.supply)
        self.assertEqual(theGameIsOver, True)

        # Add the provinces back in.
        self.supply["Province"] = [Dominion.Province()] * 3

        theGameIsOver = Dominion.gameover(self.supply)
        self.assertEqual(theGameIsOver, False)

        # Remove two other cards.  Should not cause the game to be over.
        self.supply["Duchy"] = []
        self.supply["Estate"] = []

        theGameIsOver = Dominion.gameover(self.supply)
        self.assertEqual(theGameIsOver, False)

        # This is the third one to become empty, so it should end the game.
        self.supply["Gold"] = []

        theGameIsOver = Dominion.gameover(self.supply)
        self.assertEqual(theGameIsOver, True)

        # Fourth one to be removed.  Game should still end.
        self.supply["Silver"] = []

        theGameIsOver = Dominion.gameover(self.supply)
        self.assertEqual(theGameIsOver, True)
