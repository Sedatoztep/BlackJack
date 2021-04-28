import random

class Colour:
    BLACK = '\033[30m'
    RED = '\033[91m'
    GREEN = '\033[32m'
    END = '\033[0m'

suits = (Colour.RED +  'Kupa' + Colour.END, Colour.RED + 'Karo' + Colour.END, Colour.BLACK + 'Maça' + Colour.END, Colour.BLACK + 'Sinek' + Colour.END)
ranks = ('İki', 'Üç', 'Dört', 'Beş', 'Altı', 'Yedi', 'Sekiz', 'Dokuz', 'On', 'Bacak', 'Kız', 'Papaz', 'As')
values = {'İki': 2, 'Üç': 3, 'Dört': 4, 'Beş': 5, 'Altı': 6, 'Yedi': 7, 'Sekiz': 8,
          'Dokuz': 9, 'On': 10, 'Bacak': 10, 'Kız': 10, 'Papaz': 10, 'As': 11}

playing = True

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + '  ' + self.suit


class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'As':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('Kaç çip ile oynamak istersiniz? '))
        except ValueError:
            print('Bahsiniz tam sayı olmalıdır! Tekrar deneyin.')
        else:
            if chips.bet > chips.total or chips.bet <= 0:
                print(
                    "Bahsiniz bakiyenizi aşamaz ve pozitif bir bahis girmeniz gerekir! Geçerli bakiyeniz: ",
                    chips.total)
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input("Hit mi, Kalmak mı istersiniz? '1' veya '0' girin ")

        if x.lower() == '1':
            hit(deck, hand)

        elif x.lower() == '0':
            print("Kalmayı seçtiniz. Dealer hit attı.")
            playing = False

        else:
            print("Yanlış giriş, lütfen tekrar deneyin.")
            continue
        break


def show_some(player, dealer):
    print("\nDealer'in eli:")
    print(" { gizli kart }")
    print('', dealer.cards[1])
    print("\nEliniz:", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nDealer'in eli:", *dealer.cards, sep='\n ')
    print("Dealer'in eli =", dealer.value)
    print("\nEliniz:", *player.cards, sep='\n ')
    print("Eliniz =", player.value)


def player_busts(player, dealer, chips):
    print("ÇOK FAZLA !")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("KAZANDINIZ!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("Dealer patladı !")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("Dealer kazandı!")
    chips.lose_bet()


def push(player, dealer):
    print("El berabere !")


# GAMEPLAY
player_chips = Chips()

while True:

    print("\t              **********************************************************")
    print(
        "\t                      Python Casino oyununa Hoş geldiniz - BLACK JACK !                                                     ")
    print("\t              **********************************************************")
    print(Colour.BLACK + "\t                                   ***************")
    print("\t                                   * A           *")
    print("\t                                   *             *")
    print("\t                                   *      *      *")
    print("\t                                   *     ***     *")
    print("\t                                   *    *****    *")
    print("\t                                   *     ***     *")
    print("\t                                   *      *      *")
    print("\t                                   *             *")
    print("\t                                   *             *")
    print("\t                                   ***************" + Colour.END)

    print('\nKURALLAR: Olabildiğince 21 e yaklaşın, ancak 21 den fazla alırsanız kaybedersiniz!\n  Aslar 1 veya 11 olarak sayılır.')

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())


    take_bet(player_chips)

    show_some(player_hand, dealer_hand)

    while playing:

        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)

        else:
            push(player_hand, dealer_hand)

    print("\nMevcut bakiyeniz", player_chips.total)

    if player_chips.total > 0:
        new_game = input("Başka bir el oynamak ister misin? Giriş'1' or '0' ")
        if new_game.lower() == '1':
            playing = True
            continue
        else:
            print(
                "Oynadığınız için teşekkürler!\n" + Colour.GREEN + "\t$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n \t      Tebrikler! Kazandınız " + str(player_chips.total) + " çip!\n\t$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n " + Colour.END)
            break
    else:
        print(
            "Ops! Tüm çipleriniz ile bahse girdiniz ve daha fazla oynayamadığınız için üzgünüz.\nOynadığınız için teşekkürler! Python Casino BLACK JACK'e tekrar gelin!")
